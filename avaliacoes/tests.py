from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from avaliacoes.models import Review
from catalogo.models import Cafe, Marca


class AvaliacaoBaseTestCase(TestCase):
    def setUp(self):
        self.autor = User.objects.create_user(username="autor", password="senha123")
        self.outro = User.objects.create_user(username="outro", password="senha123")
        marca = Marca.objects.create(nome="Marca Teste")
        self.cafe = Cafe.objects.create(nome="Café Teste", marca=marca, descricao="Teste")
        self.review = Review.objects.create(
            usuario=self.autor, cafe=self.cafe, nota=2, comentario="Original"
        )


class ReviewEditadaTests(AvaliacaoBaseTestCase):
    def test_recem_criada_nao_esta_editada(self):
        self.assertFalse(self.review.foi_editada)

    def test_sem_data_de_edicao_nao_esta_editada(self):
        Review.objects.filter(pk=self.review.pk).update(atualizado_em=None)
        self.review.refresh_from_db()
        self.assertFalse(self.review.foi_editada)

    def test_alterada_depois_de_um_minuto_esta_editada(self):
        Review.objects.filter(pk=self.review.pk).update(
            atualizado_em=timezone.now() + timedelta(minutes=5)
        )
        self.review.refresh_from_db()
        self.assertTrue(self.review.foi_editada)


class EditarAvaliacaoTests(AvaliacaoBaseTestCase):
    def url(self):
        return reverse("catalogo:editar_avaliacao", args=[self.review.id])

    def test_requer_login(self):
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.headers["Location"])

    def test_autor_ve_formulario_preenchido(self):
        self.client.force_login(self.autor)
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalogo/form_avaliacao.html")
        self.assertContains(response, "Original")

    def test_autor_edita_nota_e_comentario(self):
        self.client.force_login(self.autor)
        response = self.client.post(self.url(), {"nota": 5, "comentario": "Mudei de ideia"})
        self.assertRedirects(
            response, reverse("catalogo:detalhes_cafe", args=[self.cafe.id]),
            fetch_redirect_response=False,
        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.nota, 5)
        self.assertEqual(self.review.comentario, "Mudei de ideia")
        self.assertEqual(self.cafe.nota_media, 5.0)

    def test_outro_usuario_recebe_404(self):
        self.client.force_login(self.outro)
        self.assertEqual(self.client.get(self.url()).status_code, 404)
        response = self.client.post(self.url(), {"nota": 1, "comentario": "Hack"})
        self.assertEqual(response.status_code, 404)
        self.review.refresh_from_db()
        self.assertEqual(self.review.comentario, "Original")

    def test_nota_invalida_e_rejeitada(self):
        self.client.force_login(self.autor)
        response = self.client.post(self.url(), {"nota": 9, "comentario": "x"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.review.refresh_from_db()
        self.assertEqual(self.review.nota, 2)


class ExcluirAvaliacaoTests(AvaliacaoBaseTestCase):
    def url(self):
        return reverse("catalogo:excluir_avaliacao", args=[self.review.id])

    def test_requer_login(self):
        response = self.client.post(self.url())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())

    def test_get_mostra_confirmacao_sem_excluir(self):
        self.client.force_login(self.autor)
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalogo/excluir_avaliacao.html")
        self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())

    def test_autor_exclui_e_pode_avaliar_novamente(self):
        self.client.force_login(self.autor)
        self.client.post(self.url())
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())
        self.client.post(
            reverse("catalogo:detalhes_cafe", args=[self.cafe.id]),
            {"nota": 4, "comentario": "Nova avaliação"},
        )
        self.assertEqual(Review.objects.get(usuario=self.autor, cafe=self.cafe).nota, 4)

    def test_outro_usuario_recebe_404(self):
        self.client.force_login(self.outro)
        self.assertEqual(self.client.post(self.url()).status_code, 404)
        self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())


class BotoesAvaliacaoTests(AvaliacaoBaseTestCase):
    def test_botoes_aparecem_somente_para_o_autor(self):
        editar = reverse("catalogo:editar_avaliacao", args=[self.review.id])
        detalhes = reverse("catalogo:detalhes_cafe", args=[self.cafe.id])

        self.client.force_login(self.autor)
        self.assertContains(self.client.get(detalhes), editar)
        self.assertContains(self.client.get(reverse("usuarios:perfil")), editar)

        self.client.force_login(self.outro)
        self.assertNotContains(self.client.get(detalhes), editar)
