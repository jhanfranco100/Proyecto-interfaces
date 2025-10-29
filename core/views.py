
from django.conf import settings
import os
from django.db.models import F, FloatField
from django.db.models.functions import Cast

from django.db.models import Sum
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from .forms import *
from django.shortcuts import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from decimal import Decimal, InvalidOperation
from .models import *
from .email_notifications import enviar_notificacion_compra, enviar_notificacion_cotizacion, enviar_notificacion_bienvenida, notificar_admin_nuevo_usuario
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.utils import timezone

import re

def procesar_precio(precio_str):
   
    if not precio_str:
        return 0

    try:
        # Eliminar símbolos de moneda y espacios
        precio_limpio = str(precio_str).replace('$', '').replace(' ', '')

        # Remover los puntos de miles
        precio_limpio = precio_limpio.replace('.', '')

        # Quitar la coma y todo lo que viene después
        if ',' in precio_limpio:
            precio_limpio = precio_limpio.split(',')[0]

        # Convertir a entero
        precio_final = int(precio_limpio)
        return precio_final

    except (ValueError, AttributeError):
        return 0


def home(request):
    context = {
        'page_title': 'Inicio',
    }
    return render(request, 'core/principales/home.html', context)

def redireccionar_usuario(request):
    """
    Redirige al usuario a su perfil correspondiente según su tipo
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    tipo_usuario = request.user.tipo.lower()
    
    if tipo_usuario in ['administrador', 'admin']:
        return redirect('admin_dashboard')
    elif tipo_usuario == 'vendedor':
        return redirect('vendedor')
    else:  # cliente
        return redirect('home')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('redireccionar_usuario')
    
    if request.method == 'POST':
        form = UsuarioAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡HOLA,MUCHAS GRACIAS POR INICIAR SESION, {user.nombreCompleto .upper()}!')
                return redirect('redireccionar_usuario')
            else:
                messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = UsuarioAuthenticationForm()
    
    return render(request, 'core/principales/login.html', {'form': form})
def register_view(request):
    """
    Registro público: usa UsuariosCreationFormUsuarios.
    Asegura que el tipo guardado sea 'cliente'.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UsuariosCreationFormUsuarios(request.POST)
        if form.is_valid():
            # Guardar con commit=False para forzar tipo cliente por seguridad
            usuario = form.save(commit=False)
            usuario.tipo = 'cliente'
            usuario.save()
            # Enviar notificación de bienvenida por correo
            try:
                enviar_notificacion_bienvenida(usuario)
            except Exception:
                # No detener el flujo si falla el envío de correo
                pass
            # Notificar a administradores sobre el nuevo usuario
            try:
                notificar_admin_nuevo_usuario(usuario)
            except Exception:
                pass

            messages.success(request, f'¡Registro exitoso como {usuario.tipo}! Ya puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = UsuariosCreationFormUsuarios()

    return render(request, 'core/principales/registro.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        user_name = request.user.nombreCompleto
        logout(request)
        messages.success(request, f'¡Hasta luego, {user_name}! Has cerrado sesión exitosamente.')
        return redirect('home')
    else:
        # Mostrar página de confirmación
        return render(request, 'core/principales/home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UsuariosCreationFormUsuarios(request.POST)
        if form.is_valid():
            user = form.save()
            # El tipo de usuario ya se establece desde el formulario
            
            # Enviar notificación de bienvenida por correo
            enviar_notificacion_bienvenida(user)
            
            # Notificar a administradores sobre el nuevo usuario
            notificar_admin_nuevo_usuario(user)
            
            messages.success(request, f'¡Registro exitoso como {user.tipo}! Ya puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = UsuariosCreationFormUsuarios()
    
    return render(request, 'core/principales/registro.html', {'form': form})

def motocicletas(request):
    query = request.GET.get('search')
    inventario = Inventario.objects.filter(sub_categoria__icontains='automatica')

    if query:
        inventario = inventario.filter(nombre__icontains=query)

    context = {
        'filter': 'motocicletas',
        'inventario': inventario,
        'query': query,
    }
    return render(request, 'core/motos/motocicletas.html', context)

def enduro(request):
    query = request.GET.get('search')
    inventario = Inventario.objects.filter(sub_categoria__icontains='enduro')

    if query:
        inventario = inventario.filter(sub_categoria__icontains='enduro')

    context = {
        'filter': 'enduro',
        'inventario': inventario,
        'query': query,
    }
    return render(request, 'core/motos/enduro.html', context)

def todoterreno(request):
    query = request.GET.get('search')
    inventario = Inventario.objects.filter(sub_categoria__icontains='todoterreno')

    if query:
        inventario = inventario.filter(sub_categoria__icontains='todoterreno')

    context = {
        'filter': 'todoterreno',
        'inventario': inventario,
        'query': query,
    }
    return render(request, 'core/motos/todoterreno.html', context)
def automaticas(request):
    query = request.GET.get('search')
    inventario = Inventario.objects.filter(sub_categoria__icontains='automatica')

    if query:
        inventario = inventario.filter(sub_categoria__icontains='automatica')

    context = {
        'filter': 'automatica',
        'inventario': inventario,
        'query': query,
    }
    return render(request, 'core/motos/automatica.html', context)
def urbanas(request):
    query = request.GET.get('search')
    inventario = Inventario.objects.filter(sub_categoria__icontains='urbanas')

    if query:
        inventario = inventario.filter(sub_categoria__icontains='urbanas')

    context = {
        'filter': 'urbanas',
        'inventario': inventario,
        'query': query,
    }
    return render(request, 'core/motos/urbanas.html', context)
def deportivas(request):
    query = request.GET.get('search')
    inventario = Inventario.objects.filter(sub_categoria__icontains='deportivas')

    if query:
        inventario = inventario.filter(sub_categoria__icontains='deportivas')

    context = {
        'filter': 'deportivas',
        'inventario': inventario,
        'query': query,
    }
    return render(request, 'core/motos/deportivas.html', context)

def superdeportivas(request):
    query = request.GET.get('search')
    inventario = Inventario.objects.filter(sub_categoria__icontains='superdeportivas')

    if query:
        inventario = inventario.filter(sub_categoria__icontains='superdeportivas')

    context = {
        'filter': 'superdeportivas',
        'inventario': inventario,
        'query': query,
    }
    return render(request, 'core/motos/superdeportivas.html', context)

def cuatrimotos(request):
    query = request.GET.get('search')
    inventario = Inventario.objects.filter(sub_categoria__icontains='cuatrimotos')

    if query:
        inventario = inventario.filter(sub_categoria__icontains='cuatrimotos')

    context = {
        'filter': 'cuatrimotos',
        'inventario': inventario,
        'query': query,
    }
    return render(request, 'core/motos/cuatrimotos.html', context)

def equipamentos(request):
    inventario = Inventario.objects.filter(categoria__icontains='equipamento')

    context ={
        'filter': 'equipamento',
        'inventario': inventario,
    }
    return render(request, 'core/accesorios/equipamentos.html', context)

def aditamenes(request):
    inventario = Inventario.objects.filter(categoria__icontains='aditamenes')

    context ={
        'filter': 'aditamenes',
        'inventario': inventario,
    }
    return render(request, 'core/accesorios/aditamenes.html', context)


def accesorios(request):
    inventario = Inventario.objects.filter(categoria__icontains='accesorios')

    context ={
        'filter': 'accesorios',
        'inventario': inventario,
    }
    return render(request, 'core/accesorios/accesorios.html', context)

def repuestos(request):
    inventario = Inventario.objects.filter(categoria__icontains='Repuestos')
    
    context = {
        'filter': 'repuestos',
        'inventario': inventario,
    }
    return render(request, 'core/accesorios/repuestos.html', context)



def search(request):
    inventario = Inventario.objects.all()
    if 'search' in request.GET:
        producto = request.GET['search']
        if producto:
            articulos = Inventario.objects.filter(Q(nombre__icontains = producto)).distinct()
            if articulos.exists(): 
                context = {
                    'page_title': 'Accesorios',
                    'inventario': inventario,
                    'articulos': articulos,
                    'query': producto,
                    
                }
                return render(request, 'core/principales/search.html', context)
            else:
                msj = 'Artículo no encontrado'
                return render(request, 'core/principales/search.html', {'msj': msj, 'query': producto})
        else:
            msj = 'No has ingresado ningún producto'
            return render(request, 'core/principales/search.html', {'msj': msj})
    else:
        msj = 'No has buscado ningún producto'
        return render(request, 'core/principales/search.html', {'msj': msj})
        
def vermas(request, pk_object):
    
    objeto = Inventario.objects.get(pk=pk_object)
    metodos_pago = MetodoPago.objects.filter(activo=True)
    data={
        'objeto': objeto,
        'metodos_pago': metodos_pago,
    }
    return render(request, 'core/principales/VerMas.html', data)
    

def contacto(request):
    formulario = contactoForm()
    

    context ={
        'form':formulario,
        'filter': 'contactar',
    }
    if request.method == 'POST':
        formulario = contactoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            context['mensaje'] = 'Nos contactaremos contigo lo mas pronto posible'
        else:
            context['form'] = formulario
    return render(request, 'core/principales/contactar.html', context)


@login_required
def perfil(request):
    usuario = request.user
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=usuario)
    return render(request, 'core/cliente/perfil.html', {'form': form})

@login_required
def notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'core/principales/notificaciones.html', {'notificaciones': notificaciones})


def agregar_al_carrito(request, producto_id):
    
   
    messages.success(request, "Producto añadido correctamente")
    return redirect('ver_carrito', producto_id=producto_id)
@login_required
def carrito(request):
    
    return redirect('ver_carrito')

@login_required
def comprar(request, pk_object):
    try:
        objeto = Inventario.objects.get(pk=pk_object)
        
        if request.method == 'POST':
            metodo_pago_id = request.POST.get('metodo_pago')
            
            if not metodo_pago_id:
                messages.error(request, 'Debes seleccionar un método de pago.')
                return redirect('vermas', pk_object=pk_object)
            
            try:
                metodo_pago = MetodoPago.objects.get(id=metodo_pago_id, activo=True)
            except MetodoPago.DoesNotExist:
                messages.error(request, 'Método de pago no válido.')
                return redirect('vermas', pk_object=pk_object)
        else:
            # Si no es POST, redirigir al producto
            return redirect('vermas', pk_object=pk_object)
        
        # Procesar el precio usando la función helper
        precio_unitario = procesar_precio(objeto.precio)
        
        # Crear la venta
        venta = Venta.objects.create(
            cliente=request.user,
            vendedor=request.user,  # Por ahora el mismo usuario, después se puede cambiar
            total=precio_unitario,
            metodo_pago=metodo_pago,
            estado='completada'
        )
        
        # Crear el detalle de venta
        DetalleVenta.objects.create(
            venta=venta,
            producto=objeto,
            cantidad=1,
            precio_unitario=precio_unitario,
            subtotal=precio_unitario
        )
        
        # Enviar notificación por correo
        enviar_notificacion_compra(request.user, objeto, precio_unitario)
        
        if precio_unitario > 0:
            messages.success(request, f'¡Compra realizada exitosamente! Has comprado {objeto.nombre} por ${precio_unitario:,.2f}')
        else:
            messages.warning(request, f'¡Compra realizada! Has comprado {objeto.nombre}, pero el precio no se pudo procesar correctamente. Precio original: "{objeto.precio}"')
        
        # Mostrar mensaje de compra exitosa en lugar de redirigir
        return render(request, 'core/compra_exitosa.html', {
            'total': precio_unitario,
            'numero_factura': venta.numero_factura,
            'fecha_compra': venta.fecha_venta,
             'metodo_pago': venta.metodo_pago.nombre if venta.metodo_pago else 'N/A'
        })

        
    except Exception as e:
        messages.error(request, f'Error al procesar la compra: {str(e)}')
        return redirect('compra_exitosa.html')


def compra_exitosa(request):
    return render(request, 'compra_exitosa.html')

@login_required
def cotizar(request, pk_object):
    try:
        objeto = Inventario.objects.get(pk=pk_object)
        
        # Enviar notificación por correo
        enviar_notificacion_cotizacion(request.user, objeto)
        
        messages.info(request, f'Se ha enviado una solicitud de cotización para {objeto.nombre}. Te contactaremos pronto.')
        return redirect('contactar')
        
    except Exception as e:
        messages.error(request, f'Error al procesar la solicitud de cotización: {str(e)}')
        return redirect('vermas', pk_object=pk_object)

def es_vendedor(user):
    tipo = getattr(user, 'tipo', '').lower()
    return tipo in ['vendedor']

def es_admin(user):
    tipo = getattr(user, 'tipo', '').lower()
    return tipo in ['administrador', 'admin']

@login_required
@user_passes_test(es_vendedor)
def vendedor(request):
    inventario = Inventario.objects.all()
    ventas_recientes = Venta.objects.filter(vendedor=request.user).order_by('-fecha_venta')[:10]
    return render(request, 'core/vendedor/vendedor_dashboard.html', {
        'inventario': inventario,
        'ventas_recientes': ventas_recientes
    })

@login_required
@user_passes_test(es_vendedor)
def vendedor_venta(request):
    if request.method == 'POST':
        form = VendedorVentaForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            metodo_pago = form.cleaned_data['metodo_pago']
            cliente = form.cleaned_data['cliente']
            
            # Calcular precio usando la función helper
            precio_unitario = procesar_precio(producto.precio)
            total = precio_unitario * cantidad
            
            # Crear la venta
            venta = Venta.objects.create(
                cliente=cliente,
                vendedor=request.user,
                total=total,
                metodo_pago=metodo_pago,
                estado='completada'
            )
            
            # Crear el detalle de venta
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=total
            )
            
            # Enviar notificación por correo
            enviar_notificacion_compra(cliente, producto, total)
            
            messages.success(request, f'Venta realizada exitosamente! Total: ${total:,.2f}')
            return redirect('vendedor')
    else:
        form = VendedorVentaForm()
    
    return render(request, 'core/vendedor_venta.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def admin_dashboard(request):
    
    total_productos = Inventario.objects.count()
    total_usuarios = Usuarios.objects.count()
    total_ventas = Venta.objects.count()
    
    total_ingresos = (
    Venta.objects.annotate(total_float=Cast('total', FloatField()))
    .aggregate(suma=Sum('total_float'))['suma'] or 0
)

    context = {
        'total_productos': total_productos,
        'total_usuarios': total_usuarios,
        'total_ventas': total_ventas,
        'total_ingresos': f"{float(total_ingresos):,.2f}"
    }

    return render(request, 'core/admin/admin_dashboard.html', context)

@login_required
@user_passes_test(es_admin)
def admin_inventario(request):
    inventario = Inventario.objects.all()
    return render(request, 'core/admin/inventario_list.html', {'inventario': inventario})

@login_required
@user_passes_test(es_admin)
def admin_usuarios(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'core/admin/usuarios_list_admin.html', {'usuarios': usuarios})

@login_required
@user_passes_test(es_admin)
def reportes_pdf(request):
    # Calcular estadísticas
    total_productos = Inventario.objects.count()
    total_usuarios = Usuarios.objects.count()
    total_ventas = Venta.objects.count()
    
    # Calcular ingresos totales
    total_ingresos = 0
    for venta in Venta.objects.all():
        total_ingresos += float(venta.total)
    
    context = {
        'total_productos': total_productos,
        'total_usuarios': total_usuarios,
        'total_ventas': total_ventas,
        'total_ingresos': f"{total_ingresos:,.2f}"
    }
    
    return render(request, 'core/admin/reportes_admin.html', context)

@login_required
@user_passes_test(es_admin)
def generar_reporte_ventas_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'img', 'logo.png')

# Verifica si el archivo existe
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=120, height=60)
        logo.hAlign = 'CENTER'
        # Hacer el logo más opaco (transparencia)
        logo._opacity = 0.10 # 0.7 = 70% de opacidad (30% transparente)
        elements.append(logo)
    elements.append(Spacer(1, 15))

    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Centrado
    )
    
    # Título
    elements.append(Paragraph("REPORTE DE VENTAS - kronomotos", title_style))
    elements.append(Spacer(1, 20))
    
    # Fecha del reporte
    fecha_actual = timezone.now().strftime("%d/%m/%Y %H:%M")
    elements.append(Paragraph(f"Fecha de generación: {fecha_actual}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Estadísticas generales
    total_ventas = Venta.objects.count()
    total_ingresos = sum(float(venta.total) for venta in Venta.objects.all())
    ventas_completadas = Venta.objects.filter(estado='completada').count()
    
    stats_data = [
        ['Total de Ventas', str(total_ventas)],
        ['Ventas Completadas', str(ventas_completadas)],
        ['Ingresos Totales', f"${total_ingresos:,.2f}"]
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 30))
    
    # Detalle de ventas recientes
    elements.append(Paragraph("VENTAS RECIENTES", styles['Heading2']))
    elements.append(Spacer(1, 10))
    
    ventas_recientes = Venta.objects.all().order_by('-fecha_venta')[:20]
    
    if ventas_recientes:
        ventas_data = [['Fecha', 'Cliente', 'Vendedor', 'Total', 'Estado', 'Método Pago']]
        
        for venta in ventas_recientes:
            ventas_data.append([
                venta.fecha_venta.strftime("%d/%m/%Y"),
                venta.cliente.nombreCompleto if venta.cliente else 'N/A',
                venta.vendedor.nombreCompleto,
                f"${float(venta.total):,.2f}",
                venta.estado.title(),
                venta.metodo_pago.nombre if venta.metodo_pago else 'N/A'
            ])
        
        ventas_table = Table(ventas_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
        ventas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        elements.append(ventas_table)
    else:
        elements.append(Paragraph("No hay ventas registradas.", styles['Normal']))

    messages.success(request, "Reporte de ventas generado correctamente.")
    # Construir el PDF
    doc.build(elements)
    return response


@login_required
@user_passes_test(es_admin)
def generar_reporte_inventario_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Centrado
    )
    
    # Título
    elements.append(Paragraph("REPORTE DE INVENTARIO - KRONOMOTOS", title_style))
    elements.append(Spacer(1, 20))
    
    # Fecha del reporte
    fecha_actual = timezone.now().strftime("%d/%m/%Y %H:%M")
    elements.append(Paragraph(f"Fecha de generación: {fecha_actual}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Estadísticas generales
    total_productos = Inventario.objects.count()
    categorias = Inventario.objects.values_list('categoria', flat=True).distinct()
    
    stats_data = [
        ['Total de Productos', str(total_productos)],
        ['Categorías', str(len(categorias))]
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 30))
    
    # Lista de productos
    elements.append(Paragraph("INVENTARIO DE PRODUCTOS", styles['Heading2']))
    elements.append(Spacer(1, 10))
    
    productos = Inventario.objects.all().order_by('categoria', 'nombre')
    
    if productos:
        productos_data = [['Nombre', 'Categoría', 'Subcategoría', 'Precio']]
        
        for producto in productos:
            productos_data.append([
                producto.nombre[:30] + '...' if len(producto.nombre) > 30 else producto.nombre,
                producto.categoria.title() if producto.categoria else 'N/A',
                producto.sub_categoria.title() if producto.sub_categoria else 'N/A',
                f"${producto.precio}" if producto.precio else 'N/A'
            ])
        
        productos_table = Table(productos_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
        productos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        elements.append(productos_table)
    else:
        elements.append(Paragraph("No hay productos en el inventario.", styles['Normal']))
    
    # Construir el PDF
    doc.build(elements)
    return response

@login_required
@user_passes_test(es_admin)
def inventario_crear(request):
    if request.method == 'POST':
        form = InventarioAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado')
            return redirect('admin_inventario')
    else:
        form = InventarioAdminForm()
    return render(request, 'core/admin/inventario_form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def inventario_editar(request, pk):
    obj = Inventario.objects.get(pk=pk)
    if request.method == 'POST':
        form = InventarioAdminForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado')
            return redirect('admin_inventario')
    else:
        form = InventarioAdminForm(instance=obj)
    return render(request, 'core/admin/inventario_form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def inventario_eliminar(request, pk):
    obj = Inventario.objects.get(pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Producto eliminado')
        return redirect('admin_inventario')
    return render(request, 'core/admin/confirm_delete.html', {'obj': obj, 'tipo': 'producto'})

@login_required
@user_passes_test(es_admin)
def usuario_crear(request):
    if request.method == 'POST':
        form = UsuariosAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado')
            return redirect('admin_usuarios')
    else:
        form = UsuariosAdminForm()
    return render(request, 'core/admin/usuario_form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def usuario_editar(request, pk):
    obj = Usuarios.objects.get(pk=pk)
    if request.method == 'POST':
        form = UsuariosAdminForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado')
            return redirect('admin_usuarios')
    else:
        form = UsuariosAdminForm(instance=obj)
    return render(request, 'core/admin/usuario_form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def usuario_eliminar(request, pk):
    obj = Usuarios.objects.get(pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Usuario eliminado')
        return redirect('admin_usuarios')
    return render(request, 'core/admin/confirm_delete.html', {'obj': obj, 'tipo': 'usuario'})

# ------------------ Gestión de Insumos ------------------
@login_required
@user_passes_test(es_admin)
def admin_insumos(request):
    insumos = Insumo.objects.all()
    return render(request, 'core/admin/insumos_list_admin.html', {'insumos': insumos})

@login_required
@user_passes_test(es_admin)
def insumo_crear(request):
    if request.method == 'POST':
        form = InsumoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insumo creado')
            return redirect('admin_insumos')
    else:
        form = InsumoForm()
    return render(request, 'core/admin/insumo_form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def insumo_editar(request, pk):
    obj = Insumo.objects.get(pk=pk)
    if request.method == 'POST':
        form = InsumoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insumo actualizado')
            return redirect('admin_insumos')
    else:
        form = InsumoForm(instance=obj)
    return render(request, 'core/admin/insumo_form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def insumo_eliminar(request, pk):
    obj = Insumo.objects.get(pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Insumo eliminado')
        return redirect('admin_insumos')
    return render(request, 'core/admin/confirm_delete.html', {'obj': obj, 'tipo': 'insumo'})

# ------------------ Gestión de Métodos de Pago ------------------
@login_required
@user_passes_test(es_admin)
def admin_metodos_pago(request):
    metodos = MetodoPago.objects.all()
    return render(request, 'core/admin/metodos_pago_list.html', {'metodos': metodos})

@login_required
@user_passes_test(es_admin)
def metodo_pago_crear(request):
    if request.method == 'POST':
        form = MetodoPagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Método de pago creado')
            return redirect('admin_metodos_pago')
    else:
        form = MetodoPagoForm()
    return render(request, 'core/admin/metodo_pago_form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def metodo_pago_editar(request, pk):
    obj = MetodoPago.objects.get(pk=pk)
    if request.method == 'POST':
        form = MetodoPagoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Método de pago actualizado')
            return redirect('admin_metodos_pago')
    else:
        form = MetodoPagoForm(instance=obj)
    return render(request, 'core/admin/metodo_pago_form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def metodo_pago_eliminar(request, pk):
    obj = MetodoPago.objects.get(pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Método de pago eliminado')
        return redirect('admin_metodos_pago')
    return render(request, 'core/admin/confirm_delete.html', {'obj': obj, 'tipo': 'método de pago'})

# ------------------ Carrito con modelo ------------------
@login_required
def agregar_al_carrito(request, pk_object):
    try:
        producto = Inventario.objects.get(pk=pk_object)
        carrito_item, created = CarritoItem.objects.get_or_create(
            usuario=request.user,
            producto=producto,
            defaults={'cantidad': 1}
        )
        
        if not created:
            carrito_item.cantidad += 1
            carrito_item.save()
            
        messages.success(request, f"Añadido al carrito: {producto.nombre}")
        return redirect('vermas', pk_object=pk_object)
        
    except Exception as e:
        messages.error(request, f'Error al agregar al carrito: {str(e)}')
        return redirect('vermas', pk_object=pk_object)

@login_required
def quitar_del_carrito(request, pk_object):
    try:
        carrito_item = CarritoItem.objects.get(
            usuario=request.user,
            producto_id=pk_object
        )
        carrito_item.delete()
        messages.info(request, 'Producto eliminado del carrito')
    except CarritoItem.DoesNotExist:
        messages.warning(request, 'El producto no estaba en tu carrito')
    except Exception as e:
        messages.error(request, f'Error al quitar del carrito: {str(e)}')
    
    return redirect('ver_carrito')

@login_required
def actualizar_cantidad_carrito(request, pk_object):
    try:
        carrito_item = CarritoItem.objects.get(
            usuario=request.user,
            producto_id=pk_object
        )
        
        if request.method == 'POST':
            nueva_cantidad = int(request.POST.get('cantidad', 1))
            
            if nueva_cantidad <= 0:
                carrito_item.delete()
                messages.info(request, 'Producto eliminado del carrito')
            else:
                carrito_item.cantidad = nueva_cantidad
                carrito_item.save()
                messages.success(request, f'Cantidad actualizada a {nueva_cantidad}')
        
        return redirect('ver_carrito')
        
    except CarritoItem.DoesNotExist:
        messages.warning(request, 'El producto no estaba en tu carrito')
        return redirect('ver_carrito')
    except Exception as e:
        messages.error(request, f'Error al actualizar cantidad: {str(e)}')
        return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito_items = CarritoItem.objects.filter(usuario=request.user)
    listado = []
    total = Decimal('0')
    
    for item in carrito_items:
        # Usar la función helper para procesar precios
        precio_num = Decimal(str(procesar_precio(item.producto.precio)))
        subtotal = precio_num * item.cantidad
        total += subtotal
        listado.append({
            'obj': item.producto, 
            'cantidad': item.cantidad, 
            'precio': precio_num, 
            'subtotal': subtotal
        })
    
    return render(request, 'core/carrito.html', {'items': listado, 'total': total})

@login_required
def finalizar_compra(request):
    carrito_items = CarritoItem.objects.filter(usuario=request.user)
    
    if not carrito_items.exists():
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('ver_carrito')
    
    total = Decimal('0')
    items_con_subtotal = []
    
    # Calcular el total antes de cualquier cosa
    for item in carrito_items:
        try:
            precio_num = Decimal(str(procesar_precio(item.producto.precio)))
        except (ValueError, AttributeError, InvalidOperation):
            precio_num = Decimal('0')
        
        subtotal = precio_num * item.cantidad
        total += subtotal
        
        items_con_subtotal.append({
            'producto': item.producto,
            'cantidad': item.cantidad,
            'precio': precio_num,
            'subtotal': subtotal
        })
    
    # Si es un POST, procesamos la venta
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            try:
                metodo_pago = form.cleaned_data['metodo_pago']
                
                # Crear la venta
                venta = Venta.objects.create(
                    cliente=request.user,
                    vendedor=request.user,  # Si luego tienes un modelo de vendedor, se cambia
                    total=total,
                    metodo_pago=metodo_pago,
                    estado='completada'
                )
                
                # Crear los detalles de venta
                for item in carrito_items:
                    precio_unitario = Decimal(str(procesar_precio(item.producto.precio)))
                    DetalleVenta.objects.create(
                        venta=venta,
                        producto=item.producto,
                        cantidad=item.cantidad,
                        precio_unitario=precio_unitario,
                        subtotal=precio_unitario * item.cantidad
                    )
                
                # Enviar notificación
                enviar_notificacion_compra(request.user, None, total)
                
                # Vaciar carrito
                carrito_items.delete()
                
                messages.success(request, f'¡Compra realizada exitosamente! Total: ${total:,.2f}')
                
                return render(request, 'core/compra_exitosa.html', {
                    'total': total,
                    'numero_factura': venta.numero_factura,
                    'fecha_compra': venta.fecha_venta,
                    'metodo_pago': venta.metodo_pago.nombre if venta.metodo_pago else 'N/A'
                })
            except Exception as e:
                messages.error(request, f'Error al procesar la compra: {str(e)}')
                return redirect('ver_carrito')
    else:
        form = VentaForm()
    
    # GET → mostrar resumen de compra
    return render(request, 'core/finalizar_compra.html', {
        'form': form,
        'items': items_con_subtotal,
        'total': total
    })