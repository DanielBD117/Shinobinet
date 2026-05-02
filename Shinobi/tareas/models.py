from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

# 🏋️ ACTIVIDADES
class Actividad(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    f_completada = models.DateTimeField(null=True, blank=True)
    importante = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + " - por " + self.user.username


# 👤 PERFIL (UNO SOLO)
class Perfil(models.Model):
    PLANES = [
        ('basico', 'Básico'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero = models.CharField(max_length=15)
    documento = models.CharField(max_length=20)
    plan = models.CharField(max_length=10, choices=PLANES, default='basico')

    def __str__(self):
        return self.user.username