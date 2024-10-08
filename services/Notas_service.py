import requests
from django.conf import settings

class NotasService:
    def __init__(self):
        self.base_url = settings.PLUGNOTAS_BASE_URL
        self.headers = {
            'X-API-KEY': settings.PLUGNOTAS_API_KEY,
            'Content-Type': 'application/json'
        }

    # Criar Nota Fiscal
    def criar_nota_fiscal(self, payload):
        url = f'{self.base_url}/nfe'  # Endpoint para emitir NFe
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def correcao_nota_fiscal(self, nota_id, correcao):
        url = f'{self.base_url}/nfe/{nota_id}/cce'  # Padrão conforme documentação
        payload = {'correcao': correcao}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    # Consultar Nota Fiscal pelo ID
    def consultar_cancelamento_status_nota_fiscal(self, nota_id):
        url = f'{self.base_url}/nfe/{nota_id}/cancelamento/status'  # Conforme documentação
        response = requests.get(url, headers=self.headers)
        return response.json()

    # Cancelar Nota Fiscal
    def cancelar_nota_fiscal(self, nota_id, motivo):
        url = f'{self.base_url}/nfe/{nota_id}/cancelamento'  # Padrão conforme documentação
        payload = {'justificativa': motivo}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    

    
    def baixar_xml_cancelamento(self, nota_id):
        url = f'{self.base_url}/nfe/{nota_id}/cancelamento/xml'
        response = requests.get(url, headers=self.headers)
        return response
    
    def baixar_pdf(self, nota_id):
        url = f'{self.base_url}/nfe/{nota_id}/pdf'
        response = requests.get(url, headers=self.headers)
        return response

    def baixar_xml(self, nota_id):
        url = f'{self.base_url}/nfe/{nota_id}/xml'
        response = requests.get(url, headers=self.headers)
        return response
    
    