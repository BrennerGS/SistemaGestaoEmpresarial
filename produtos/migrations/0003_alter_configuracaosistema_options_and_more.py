# Generated by Django 5.0.2 on 2024-03-01 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0002_configuracaosistema_itemordemcompra_itemordemvenda_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='configuracaosistema',
            options={'verbose_name': 'Configuração de Sistema', 'verbose_name_plural': 'Configurações de Sistema'},
        ),
        migrations.AlterModelOptions(
            name='fornecedor',
            options={'verbose_name': 'Fornecedor', 'verbose_name_plural': 'Fornecedores'},
        ),
        migrations.AlterModelOptions(
            name='funcionario',
            options={'verbose_name': 'Funcionario', 'verbose_name_plural': 'Funcionarios'},
        ),
        migrations.AlterModelOptions(
            name='itemordemcompra',
            options={'verbose_name': 'Item Ordem de Compra', 'verbose_name_plural': 'Itens Ordem de Compra'},
        ),
        migrations.AlterModelOptions(
            name='itemordemvenda',
            options={'verbose_name': 'Item Ordem de Venda', 'verbose_name_plural': 'Itens Ordem de Venda'},
        ),
        migrations.AlterModelOptions(
            name='localizacao',
            options={'verbose_name': 'Localização', 'verbose_name_plural': 'Localizações'},
        ),
        migrations.AlterModelOptions(
            name='ordemcompra',
            options={'verbose_name': 'Ordem de Compra', 'verbose_name_plural': 'Ordens de Compra'},
        ),
        migrations.AlterModelOptions(
            name='ordemvenda',
            options={'verbose_name': 'Ordem de Venda', 'verbose_name_plural': 'Ordens de Venda'},
        ),
    ]
