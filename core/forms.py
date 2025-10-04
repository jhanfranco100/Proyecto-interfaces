from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Opciones para el tipo de usuario
TIPO_CHOICES = (
    ('cliente', 'Cliente'),
    ('vendedor', 'Vendedor'),
    ('administrador', 'Administrador'),
)

# Registro propio de usuarios
class UsuariosCreationFormUsuarios(UserCreationForm):
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Tipo de Usuario',
        initial='cliente'
    )
    notificaciones = forms.BooleanField(required=False, label='Recibir notificaciones por correo')
    
    class Meta:
        model = Usuarios
        fields = ['nombreCompleto', 'correo', 'tipo', 'direccion', 'ciudad', 'telefono', 'notificaciones', 'password1', 'password2']
        widgets = {
            'nombreCompleto': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

# Registro de administrador y supervisor (Solo los administradores pueden hacerlo)
class UsuariosCreationFormAll(UserCreationForm):
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, widget=forms.Select)
    
    class Meta:
        model = Usuarios
        fields = ['nombreCompleto', 'correo', 'tipo', 'is_staff', 'is_superuser', 'direccion', 'ciudad', 'telefono', 'notificaciones', 'password1', 'password2']

class UsuarioAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Correo', 
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu correo electrónico'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'})
    )

    class Meta:
        model = Usuarios
        fields = ['correo', 'password']
    
class PerfilForm(forms.ModelForm):
    notificaciones = forms.BooleanField(required=False, label='Recibir notificaciones por correo')
    class Meta:
        model = Usuarios
        fields = ['nombreCompleto', 'correo', 'direccion', 'ciudad', 'telefono', 'notificaciones']
        widgets = {
            'nombreCompleto': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

class InventarioForms(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre', 'descripcion', 'precio', 'photo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class InventarioAdminForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre', 'descripcion', 'cilindraje', 'peso', 'potenciaMaxima', 'torqueMaximo', 'tipoDeMotor', 'precio', 'photo', 'categoria', 'sub_categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'cilindraje': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.TextInput(attrs={'class': 'form-control'}),
            'potenciaMaxima': forms.TextInput(attrs={'class': 'form-control'}),
            'torqueMaximo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipoDeMotor': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'sub_categoria': forms.Select(attrs={'class': 'form-select'}),
        }

class UsuariosAdminForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['nombreCompleto', 'correo', 'tipo', 'is_staff', 'is_superuser', 'direccion', 'ciudad', 'telefono', 'notificaciones', 'is_active']
        widgets = {
            'nombreCompleto': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}, choices=TIPO_CHOICES),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }


class contactoForm(forms.ModelForm):
    class Meta:
        model=contacto
        fields=['nombre','apellido','correo','direccion','ciudad','telefono','mensaje']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'CF_nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'CF_apellido'}),
            'correo': forms.EmailInput(attrs={'class': 'CF_correo'}),
            'direccion': forms.TextInput(attrs={'class': 'CF_direccion'}),
            'ciudad': forms.TextInput(attrs={'class': 'CF_ciudad'}),
            'telefono': forms.TextInput(attrs={'class': 'CF_telefono'}),
            'mensaje': forms.Textarea(attrs={'class': 'CF_mensaje'}),
            
            
        }
        
        def __init__(self, *args, **kwargs):
            super(contactoForm, self).__init__(*args, **kwargs)
            self.fields['mensaje'].widget.attrs.update({
                'class': 'texter',
        })


class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'descripcion', 'categoria', 'stock_actual', 'stock_minimo', 'precio_unitario', 'proveedor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MetodoPagoForm(forms.ModelForm):
    class Meta:
        model = MetodoPago
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['metodo_pago']
        widgets = {
            'metodo_pago': forms.Select(attrs={'class': 'form-select'}),
        }


class VendedorVentaForm(forms.Form):
    producto = forms.ModelChoiceField(
        queryset=Inventario.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Producto'
    )
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Cantidad'
    )
    metodo_pago = forms.ModelChoiceField(
        queryset=MetodoPago.objects.filter(activo=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Método de Pago'
    )
    cliente = forms.ModelChoiceField(
        queryset=Usuarios.objects.filter(tipo='cliente'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Cliente'
    )
