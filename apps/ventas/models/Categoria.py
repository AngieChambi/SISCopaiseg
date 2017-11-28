from django.db import models
from ..models.Departamento import Departamento


class Categoria(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)
    departamento = models.ForeignKey(Departamento)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.descripcion
