from django.db import models


class Usuario(models.Model):
    nome = models.CharField(max_length=150)
    sobrenome = models.CharField(max_length=150)
    email = models.EmailField()
    senha = models.CharField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    # local_favorito = models.ForeignKey()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
