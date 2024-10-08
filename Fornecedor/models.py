from django.db import models

# Create your models here.
class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
    
    def __str__(self):
        return f"{self.nome}"