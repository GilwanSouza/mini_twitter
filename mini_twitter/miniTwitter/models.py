from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    data_nascimento = models.DateField(blank=True, null=True)
    nome = models.CharField(max_length=150, blank=True, null=True)
    seguindo = models.ManyToManyField('self', symmetrical=False, related_name='seguidores', blank=True)

    def __str__(self):
        return self.username

class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tweets')
    texto = models.CharField(max_length=280)
    criado_em = models.DateTimeField(auto_now_add=True)
    curtidas = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tweets_curtidos', blank=True)

    @property
    def total_curtidas(self):
        return self.curtidas.count()

    def __str__(self):
        return f'{self.user.username}: {self.texto[:50]} - {self.total_curtidas} curtidas'
