from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from avaliacoes.models import Review
from catalogo.models import Cafe, Marca


class DashboardAnaliticoTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username="analista", email="analista@graoprosa.com", password="senha123"
        )
        self.marca = Marca.objects.create(
            nome="Marca Teste", pais_origem="Brasil", historia="História de teste."
        )
        self.cafe1 = Cafe.objects.create(
            nome="Café Especial 1",
            marca=self.marca,
            tipo_grao=Cafe.TipoGrao.ARABICA,
            tipo_torra=Cafe.TipoTorra.MEDIA,
            intensidade=7,
            descricao="Café de teste 1",
        )
        self.cafe2 = Cafe.objects.create(
            nome="Café Especial 2",
            marca=self.marca,
            tipo_grao=Cafe.TipoGrao.BLEND,
            tipo_torra=Cafe.TipoTorra.ESCURA,
            intensidade=9,
            descricao="Café de teste 2",
        )
        # Reviews
        Review.objects.create(
            usuario=self.usuario, cafe=self.cafe1, nota=5, comentario="Perfeito!"
        )

    def test_dashboard_requer_login(self):
        url = reverse("catalogo:dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.headers["Location"])

    def test_dashboard_acesso_autenticado(self):
        self.client.force_login(self.usuario)
        url = reverse("catalogo:dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalogo/dashboard.html")

    def test_dashboard_metricas_e_agregacoes(self):
        self.client.force_login(self.usuario)
        url = reverse("catalogo:dashboard")
        response = self.client.get(url)

        self.assertEqual(response.context["total_cafes"], 2)
        self.assertEqual(response.context["total_marcas"], 1)
        self.assertEqual(response.context["total_avaliacoes"], 1)
        self.assertEqual(response.context["media_geral"], 5.0)

        # Dados estruturados para o Chart.js
        dashboard_data = response.context["dashboard_data"]
        self.assertIn("torra", dashboard_data)
        self.assertIn("top_cafes", dashboard_data)
        self.assertIn("histograma", dashboard_data)
        self.assertIn("grao", dashboard_data)
