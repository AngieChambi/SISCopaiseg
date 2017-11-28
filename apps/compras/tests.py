from django.test import TestCase
from apps.ventas.models.Producto import Producto
from apps.ventas.models.Departamento import Departamento
from apps.ventas.models.Categoria import Categoria
from apps.ventas.models.UnidadMedida import UnidadMedidaC
from apps.ventas.models.UnidadMedida import UnidadMedidaV
from apps.compras.models.Proveedor import Proveedor

# Create your tests here.


class ProductoTestCase(TestCase):

    def setUp(self):

        departamento = Departamento.objects.create(
            descripcion="departamentoprueba")
        categoria = Categoria.objects.create(
            descripcion="Categoriatest", departamento=departamento)
        uv = UnidadMedidaV.objects.create(
            nombre="kilogramosprueba", simbolo="kg")
        uc = UnidadMedidaC.objects.create(
            nombre="arobas", simbolo="@",
            cant_equivalencia=12,
            unidad_medida_venta=uv)

        Producto.objects.create(
            nombre="Producto00000001",
            codigo="0001test",
            categoria=categoria,
            fechaVencimiento='2026-12-12',
            unidad_medida=uc,
            precioV=2.20,
            precioC=2.00,
            existencia=0.00,
            MontoReal=0.00,
            igv=0.00)
        Producto.objects.create(
            nombre="Producto00000002",
            codigo="0002test",
            categoria=categoria,
            fechaVencimiento='2016-12-12',
            unidad_medida=uc, precioV=2.20,
            precioC=2.00, existencia=0.00,
            MontoReal=0.00, igv=0.00)

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        producto01 = Producto.objects.get(
            nombre="Producto00000001")
        producto02 = Producto.objects.get(
            nombre="Producto00000002")
        self.assertEqual(producto01.codigo, '0001test')
        self.assertEqual(producto02.codigo, '0002test')


class ProveedorTestCase(TestCase):

    def setUp(self):

        Proveedor.objects.create(
            tipodoc="RUC",
            numdoc=73447121,
            razon_social='Sapatitos sac',
            representante_legal='Juan mamani ',
            direccion='Jr. puno',
            telefono=946883323,
            email='proveedor@gmail.com',
            enti_bancaria='interbanck',
            num_cuenta='202020202220',
            estado=True)

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        numero = Proveedor.objects.get(
            numdoc=73447121)
        tel = Proveedor.objects.get(
            telefono=946883323)
        self.assertEqual(tel.telefono, 946883323)
        self.assertEqual(numero.numdoc, 73447121)
