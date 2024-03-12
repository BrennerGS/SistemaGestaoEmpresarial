from django.test import TestCase
from .models import ConfiguracaoSistema
from django.urls import reverse

class ConfiguracaoSistemaTests(TestCase):
    def setUp(self):
        self.configuracao_sistema = ConfiguracaoSistema.objects.create(
            informacoes_contato='Informações de Contato',
            termos_de_uso='Termos de Uso',
            politicas_privacidade='Políticas de Privacidade'
        )

    def test_configuracao_sistema_str(self):
        self.assertEqual(str(self.configuracao_sistema), 'Informações de Contato')

    def test_configuracao_sistema_detail_view_status_code(self):
        url = reverse('configuracao_sistema_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)