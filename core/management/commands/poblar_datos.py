from django.core.management.base import BaseCommand
from core.models import MetodoPago, Insumo

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos iniciales'

    def handle(self, *args, **options):
        # Crear métodos de pago por defecto
        metodos_pago = [
            {
                'nombre': 'Efectivo',
                'descripcion': 'Pago en efectivo al momento de la entrega',
                'activo': True
            },
            {
                'nombre': 'Tarjeta de Crédito',
                'descripcion': 'Pago con tarjeta de crédito',
                'activo': True
            },
            {
                'nombre': 'Tarjeta Débito',
                'descripcion': 'Pago con tarjeta débito',
                'activo': True
            },
            {
                'nombre': 'Transferencia Bancaria',
                'descripcion': 'Transferencia bancaria o PSE',
                'activo': True
            },
            {
                'nombre': 'Cheque',
                'descripcion': 'Pago con cheque',
                'activo': False
            }
        ]
        
        for metodo_data in metodos_pago:
            metodo, created = MetodoPago.objects.get_or_create(
                nombre=metodo_data['nombre'],
                defaults=metodo_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Creado método de pago: {metodo.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Método de pago ya existe: {metodo.nombre}')
                )
        
        # Crear algunos insumos de ejemplo
        insumos_ejemplo = [
            {
                'nombre': 'Aceite de Motor 10W-40',
                'descripcion': 'Aceite sintético para motores de motocicletas',
                'categoria': 'Lubricantes',
                'stock_actual': 50,
                'stock_minimo': 10,
                'precio_unitario': 25000.00,
                'proveedor': 'Castrol Colombia'
            },
            {
                'nombre': 'Filtro de Aire',
                'descripcion': 'Filtro de aire para motocicletas Yamaha',
                'categoria': 'Filtros',
                'stock_actual': 30,
                'stock_minimo': 5,
                'precio_unitario': 15000.00,
                'proveedor': 'Yamaha Parts'
            },
            {
                'nombre': 'Pastillas de Freno',
                'descripcion': 'Pastillas de freno delanteras y traseras',
                'categoria': 'Frenos',
                'stock_actual': 25,
                'stock_minimo': 8,
                'precio_unitario': 45000.00,
                'proveedor': 'Brembo Colombia'
            },
            {
                'nombre': 'Bujía NGK',
                'descripcion': 'Bujía de encendido para motores 4 tiempos',
                'categoria': 'Encendido',
                'stock_actual': 100,
                'stock_minimo': 20,
                'precio_unitario': 8000.00,
                'proveedor': 'NGK Colombia'
            }
        ]
        
        for insumo_data in insumos_ejemplo:
            insumo, created = Insumo.objects.get_or_create(
                nombre=insumo_data['nombre'],
                defaults=insumo_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Creado insumo: {insumo.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Insumo ya existe: {insumo.nombre}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Datos iniciales creados exitosamente!')
        )
