from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import Sum

# Create your models here.
#estas lineas lo que hace es crear ususarios personalizados por consola
class CustomUserManager(BaseUserManager):
    def create_user(self, correo, password=None, tipo='cliente', nombreCompleto=''):
        if not correo:
            raise ValueError('El Correo es obligatorio')
        if not nombreCompleto:
            raise ValueError('El Nombre de Usuario es Obligatorio')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, tipo=tipo, nombreCompleto=nombreCompleto)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password, nombreCompleto=''):
        user = self.create_user(correo, password, tipo='administrador', nombreCompleto=nombreCompleto)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Usuarios(AbstractBaseUser, PermissionsMixin):
    nombreCompleto = models.CharField(max_length=50, verbose_name='Nombre')
    apellido = models.CharField(max_length=50, verbose_name='Apellido', blank=True)
    correo = models.EmailField(unique=True, verbose_name='Correo Electronico')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, verbose_name='Es un Supervisor')
    tipo = models.CharField(max_length=16, default='cliente', verbose_name='Tipo de Usuario')
    direccion = models.CharField(max_length=60, default='', verbose_name='Dirrecion')
    ciudad = models.CharField(max_length=25, default='', verbose_name='Ciudad')
    telefono = models.CharField(max_length=25, default='', verbose_name='Telefono')
    notificaciones = models.BooleanField(default=False, verbose_name='Recibir notificaciones por correo')
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)
    groups = models.ManyToManyField('auth.Group', related_name='custom_usuario_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_usuario_permissions', blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombreCompleto']
    class Meta:
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'


categoria = [
    
    ('', ''),
    ('accesorios', 'accesorios'),
    ('equipamento', 'equipamento'),
    ('vehiculos', 'vehiculos'),
    ('repuestos', 'repuestos'),
    ('aditamenes', 'aditamenes'),
]
    

sub_categoria = [
    
    ('', ''),
    ('automatica','Automatica'),  
    ('enduro','Enduro'),  
    ('superdeportivas','Superdeportivas'),
    ('deportivas', 'Deportivas'),
    ('urbanas', 'Urbanas'),
    ('todoterreno','Todoterreno'),
    ('cuatrimotos','Cuatrimotos'),
]
    
class Inventario(models.Model):
    nombre = models.CharField(max_length=40, null=False, blank=False)
    descripcion = models.CharField(max_length=800, null=True, blank=True)
    cilindraje = models.CharField(max_length=40, null=True, blank=True)
    peso = models.CharField(max_length=40, null=True, blank=True)
    potenciaMaxima = models.CharField(max_length=40, null=True, blank=True)    
    torqueMaximo =  models.CharField(max_length=40, null=True, blank=True)
    tipoDeMotor =  models.CharField(max_length=180, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    photo = models.ImageField(upload_to='inventario/')
    categoria = models.CharField(max_length=32, default='', choices=categoria, blank=True)
    sub_categoria = models.CharField(max_length=32, default='', choices=sub_categoria, blank=True)

    def __str__(self):
        return f'{self.categoria} - {self.sub_categoria} - {self.nombre}'


class contacto(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    apellido = models.CharField(max_length=50, verbose_name='Apellido', blank=True)
    correo = models.EmailField(unique=True, verbose_name='Correo Electronico')
    direccion = models.CharField(max_length=60, default='', verbose_name='Dirrecion')
    ciudad = models.CharField(max_length=25, default='', verbose_name='Ciudad')
    telefono = models.CharField(max_length=25, default='', verbose_name='Telefono')
    objeto = models.ForeignKey(Inventario,null=True,blank=True,on_delete=models.SET_NULL)
    mensaje=models.TextField()

    def __str__(self):
        return f'{self.nombre} - {self.apellido} - {self.objeto}'

    REQUIRED_FIELDS = ['nombre','apellido','correo','direccion','ciudad','telefono','objeto','mensaje']
    class Meta:
        verbose_name='contacto'
        verbose_name_plural='contactos'


class CarritoItem(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Item del Carrito'
        verbose_name_plural = 'Items del Carrito'
        unique_together = ('usuario', 'producto')

class MetodoPago(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre del Método')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Método de Pago'
        verbose_name_plural = 'Métodos de Pago'
    
    def __str__(self):
        return self.nombre


class Venta(models.Model):
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada')
    ], default='pendiente')
    cliente = models.ForeignKey(Usuarios, on_delete=models.CASCADE, 
                               related_name='compras_realizadas', blank=True, null=True)
    vendedor = models.ForeignKey(Usuarios, on_delete=models.CASCADE, 
                                related_name='ventas_realizadas')
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, 
                                   null=True, blank=True, verbose_name='Método de Pago')
    numero_factura = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
    
    def save(self, *args, **kwargs):
        if not self.numero_factura:
            # Generar número de factura único
            import uuid
            self.numero_factura = f"FAC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'

    def save(self, *args, **kwargs):
        # Calcular subtotal antes de guardar
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

        # Actualizar total de la venta
        total = self.venta.detalles.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
        self.venta.total = total
        self.venta.save(update_fields=['total'])

    def delete(self, *args, **kwargs):
        venta = self.venta
        super().delete(*args, **kwargs)

        # Recalcular el total después de eliminar el detalle
        total = venta.detalles.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
        venta.total = total
        venta.save(update_fields=['total'])



class Insumo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Insumo')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    categoria = models.CharField(max_length=50, verbose_name='Categoría')
    stock_actual = models.PositiveIntegerField(default=0, verbose_name='Stock Actual')
    stock_minimo = models.PositiveIntegerField(default=5, verbose_name='Stock Mínimo')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio Unitario')
    proveedor = models.CharField(max_length=100, blank=True, verbose_name='Proveedor')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'


class Notificacion(models.Model):
    titulo = models.CharField(max_length=100)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=20, choices=[
        ('info', 'Informativa'),
        ('promocion', 'Promoción'),
        ('stock', 'Stock Bajo'),
        ('venta', 'Nueva Venta'),
        ('registro', 'Registro de Usuario'),
        ('bienvenida', 'Bienvenida')
    ], default='info')
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'




