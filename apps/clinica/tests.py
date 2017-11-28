# coding: utf-8 _*_
from django.test import TestCase
from apps.clinica.models.mascota import Mascota
from apps.clinica.models.colamedica import ColaMedica
from apps.clinica.models.historia import Historial
from apps.clivet.models.cliente import Cliente
from apps.params.models import Person
from apps.sad.models import User

import datetime
# Create your tests here.

class MascotaTestCase(TestCase):
    def setUp(self):
        a1 = Person.objects.create(first_name="J.K. Rowling")
        a2 = Cliente.objects.create(persona=a1)
        md1 = User.objects.create(username="Neftali")
        vet1 = User.objects.create(username="Washinton")
        m1 = Mascota.objects.create(nombre="tarzan", color="negro", dueño=a2)
        m2 = Mascota.objects.create(nombre="golen", color="blanco", dueño=a2)
        h1 = Historial.objects.create(mascota = m1, veterinario=vet1, num_historia="00001")
        ColaMedica.objects.create(historia = h1, medico = md1, descripcion="probando el test")

    def test_create_mascota(self):
        """Animals that can speak are correctly identified"""
        tarzan = Mascota.objects.get(nombre="tarzan")
        golen = Mascota.objects.get(nombre="golen")
        self.assertEqual(tarzan.color, 'negro')
        self.assertEqual(golen.color, 'blanco')

    def test_update_mascota(self):
        Mascota.objects.filter(nombre = "golen", color="blanco").update(nombre="Roky", color="grys")
        mascota = Mascota.objects.get(nombre="Roky")
        self.assertEqual(mascota.nombre, 'golen')

    def test_delete_mascota(self):
        Mascota.objects.get(nombre="golen").delete()

    def test_create_historia(self):
        """Animals that can speak are correctly identified"""
        historia = Historial.objects.get(mascota__nombre="tarzan")
        self.assertEqual(historia.num_historia, '00001')

    def test_asignacion_historia(self):
        tarzan = ColaMedica.objects.get(descripcion="probando el test")
        self.assertEqual(tarzan.descripcion, 'probando el test')

    def test_filter_asignaciones(self):
        asignacion = ColaMedica.objects.filter(fecha=datetime.date.today())
        cantidad = ColaMedica.objects.all().count()
