from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginRedirectTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="degustador", email="degustador@graoeprosa.com", password="senha123"
        )
        self.url = reverse("usuarios:login")

    def _login(self, next_url):
        return self.client.post(
            self.url, {"email": "degustador@graoeprosa.com", "senha": "senha123", "next": next_url}
        )

    def test_redireciona_para_next_interno(self):
        response = self._login("/catalogo/dashboard/")
        self.assertRedirects(response, "/catalogo/dashboard/", fetch_redirect_response=False)

    def test_bloqueia_next_externo(self):
        for url in ("https://malicioso.com/", "//malicioso.com/", "/\\malicioso.com"):
            with self.subTest(url=url):
                self.client.logout()
                response = self._login(url)
                self.assertRedirects(response, reverse("home"), fetch_redirect_response=False)

    def test_sem_next_vai_para_home(self):
        response = self._login("")
        self.assertRedirects(response, reverse("home"), fetch_redirect_response=False)
