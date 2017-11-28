# coding: utf-8 _*_
from django.test import TestCase
from apps.ventas.models.Producto import Producto
from apps.ventas.models.Departamento import Departamento
from apps.ventas.models.Categoria import Categoria
from apps.ventas.models.UnidadMedida import UnidadMedidaC
from apps.ventas.models.UnidadMedida import UnidadMedidaV
from apps.ventas.models.Venta import Venta
from apps.ventas.models.Venta_Detalle import Detalle_Venta
from apps.clivet.models.cliente import Cliente
from backengo.sad.models import User
from apps.params.models import Person

# Create your tests here.


class ProductoTestCase(TestCase):

    def setUp(self):

        a1 = Departamento.objects.create(descripcion="departamentoprueba")
        a2 = Categoria.objects.create(
            descripcion="Categoriatest", departamento=a1)
        a3 = UnidadMedidaV.objects.create(
            nombre="kilogramosprueba", simbolo="kg")
        a4 = UnidadMedidaC.objects.create(
            nombre="arobas", simbolo="@", cant_equivalencia=12, unidad_medida_venta=a3)
        Producto.objects.create(
            nombre="productoTests00000001", codigo="0001test", categoria=a2, fechaVencimiento='2026-12-12', unidad_medida=a4, precioV=2.20, precioC=2.00, existencia=0.00, MontoReal=0.00, igv=0.00)
        Producto.objects.create(
            nombre="productoTests00000002", codigo="0002test", categoria=a2, fechaVencimiento='2016-12-12', unidad_medida=a4, precioV=2.20, precioC=2.00, existencia=0.00, MontoReal=0.00, igv=0.00)

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        productoTests00000001 = Producto.objects.get(
            nombre="productoTests00000001")
        productoTests00000002 = Producto.objects.get(
            nombre="productoTests00000002")
        self.assertEqual(productoTests00000001.codigo, '0001test')
        self.assertEqual(productoTests00000002.codigo, '0002test')


class VentaTestCase(TestCase):

    def setUp(self):

        persona = Person.objects.create(first_name="German")
        cliente = Cliente.objects.create(persona=persona)
        usuario = User.objects.create(username="germancastrovilchez")
        departamento = Departamento.objects.create(
            descripcion="departamentoprueba")
        categoria = Categoria.objects.create(
            descripcion="Categoriatest",
            departamento=departamento)
        unidadV = UnidadMedidaV.objects.create(
            nombre="kilogramosprueba", simbolo="kg")
        unidadC = UnidadMedidaC.objects.create(
            nombre="arobas",
            simbolo="@",
            cant_equivalencia=12,
            unidad_medida_venta=unidadV)
        p1 = Producto.objects.create(
            nombre="productoTests00000001",
            codigo="0001test",
            categoria=categoria,
            fechaVencimiento='2026-12-12',
            unidad_medida=unidadC,
            precioV=2.00,
            precioC=2.00,
            existencia=0.00,
            MontoReal=0.00,
            igv=0.00)
        p2 = Producto.objects.create(
            nombre="productoTests00000002",
            codigo="0002test",
            categoria=categoria,
            fechaVencimiento='2016-12-12',
            unidad_medida=unidadC,
            precioV=2.00, precioC=2.00,
            existencia=0.00,
            MontoReal=0.00,
                   igv=0.00)
        p3 = Producto.objects.create(
            nombre="productoTests00000003",
            codigo="0003test",
            categoria=categoria,
            fechaVencimiento='2016-12-12',
            unidad_medida=unidadC,
            precioV=2.00, precioC=2.00,
            existencia=0.00,
            MontoReal=0.00,
            igv=0.00)
        p4 = Producto.objects.create(
            nombre="productoTests00000004",
            codigo="0004test",
            categoria=categoria,
            fechaVencimiento='2016-12-12',
            unidad_medida=unidadC,
            precioV=2.00, precioC=2.00,
            existencia=0.00,
            MontoReal=0.00,
            igv=0.00)
        p5 = Producto.objects.create(
            nombre="productoTests00000005",
            codigo="0005test",
            categoria=categoria,
            fechaVencimiento='2016-12-12',
            unidad_medida=unidadC,
            precioV=2.00,
            precioC=2.00,
            existencia=0.00,
            MontoReal=0.00,
            igv=0.00)
        p6 = Producto.objects.create(
            nombre="productoTests00000006",
            codigo="0006test",
            categoria=categoria,
            fechaVencimiento='2016-12-12',
            unidad_medida=unidadC,
            precioV=2.00,
            precioC=2.00,
            existencia=0.00,
            MontoReal=0.00,
            igv=0.00)
        venta = Venta.objects.create(
            fechav='2016-12-12',
            total=18,
            cliente=cliente,
            user=usuario,
            igv=3.24)
        Detalle_Venta.objects.create(
            producto=p1,
            venta=venta,
            importe=4.00,
            cantidad=2.00)
        Detalle_Venta.objects.create(
            producto=p2,
            venta=venta,
            importe=4.00,
            cantidad=2.00)
        Detalle_Venta.objects.create(
            producto=p3,
            venta=venta,
            importe=4.00,
            cantidad=2.00)
        Detalle_Venta.objects.create(
            producto=p4,
            venta=venta,
            importe=4.00,
            cantidad=2.00)
        Detalle_Venta.objects.create(
            producto=p5,
            venta=venta,
            importe=4.00,
            cantidad=2.00)
        Detalle_Venta.objects.create(
            producto=p6,
            venta=venta,
            importe=4.00,
            cantidad=2.00)

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        productoTests00000001 = Producto.objects.get(
            nombre="productoTests00000001")
        productoTests00000002 = Producto.objects.get(
            nombre="productoTests00000002")
        productoTests00000003 = Producto.objects.get(
            nombre="productoTests00000003")
        productoTests00000004 = Producto.objects.get(
            nombre="productoTests00000004")
        productoTests00000005 = Producto.objects.get(
            nombre="productoTests00000005")
        productoTests00000006 = Producto.objects.get(
            nombre="productoTests00000006")
        CantidadP = Detalle_Venta.objects.filter(venta=1)
        self.assertEqual(CantidadP.count(), 6)
        self.assertEqual(productoTests00000001.nombre, 'productoTests00000001')
        self.assertEqual(productoTests00000002.nombre, 'productoTests00000002')
        self.assertEqual(productoTests00000003.nombre, 'productoTests00000003')
        self.assertEqual(productoTests00000004.nombre, 'productoTests00000004')
        self.assertEqual(productoTests00000005.nombre, 'productoTests00000005')
        self.assertEqual(productoTests00000006.nombre, 'productoTests00000006')
