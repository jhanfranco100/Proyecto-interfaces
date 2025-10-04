from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from .models import Usuarios, Notificacion
import logging

# Configurar logging para correos
logger = logging.getLogger(__name__)


def enviar_notificacion_correo(usuario, titulo, mensaje, tipo='info'):
    """
    Envía una notificación por correo al usuario
    """
    try:
        # Solo enviar si el usuario tiene habilitadas las notificaciones
        if not usuario.notificaciones:
            logger.info(f'Usuario {usuario.correo} tiene notificaciones deshabilitadas')
            return False
            
        # Crear la notificación en la base de datos
        Notificacion.objects.create(
            usuario=usuario,
            titulo=titulo,
            mensaje=mensaje,
            tipo=tipo
        )
        
        # Preparar el contenido del correo
        subject = f"🏍️ Yamaha - {titulo}"
        
        # Crear el contenido HTML del correo
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background-color: #d32f2f; color: white; padding: 20px; text-align: center;">
                    <h1 style="margin: 0;">🏍️ Yamaha</h1>
                </div>
                
                <div style="padding: 20px; background-color: #f9f9f9;">
                    <h2 style="color: #d32f2f;">{titulo}</h2>
                    <p>{mensaje}</p>
                    
                    <div style="margin-top: 30px; padding: 15px; background-color: #e8f5e8; border-left: 4px solid #4caf50;">
                        <p style="margin: 0;"><strong>Gracias por confiar en Yamaha</strong></p>
                        <p style="margin: 5px 0 0 0;">Tu tienda oficial de motocicletas y accesorios</p>
                    </div>
                </div>
                
                <div style="text-align: center; padding: 20px; background-color: #f5f5f5; font-size: 12px; color: #666;">
                    <p>Este es un correo automático, por favor no responder.</p>
                    <p>Si no deseas recibir más notificaciones, puedes desactivarlas en tu perfil.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Crear versión de texto plano
        plain_message = f"""
        Yamaha - {titulo}
        
        {mensaje}
        
        Gracias por confiar en Yamaha
        Tu tienda oficial de motocicletas y accesorios
        
        Este es un correo automático, por favor no responder.
        Si no deseas recibir más notificaciones, puedes desactivarlas en tu perfil.
        """
        
        # Enviar el correo usando EmailMultiAlternatives para mejor compatibilidad
        msg = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[usuario.correo]
        )
        msg.attach_alternative(html_message, "text/html")
        
        # Enviar el correo
        result = msg.send(fail_silently=False)
        
        if result:
            logger.info(f'Correo enviado exitosamente a {usuario.correo}')
            return True
        else:
            logger.error(f'Error al enviar correo a {usuario.correo}')
            return False
        
    except Exception as e:
        logger.error(f'Error enviando correo a {usuario.correo}: {str(e)}')
        return False


def enviar_notificacion_compra(usuario, producto, total):
    """
    Envía notificación de compra realizada
    """
    titulo = "Compra realizada exitosamente"
    
    if producto:
        mensaje = f"""
        ¡Hola {usuario.nombreCompleto}!
        
        Tu compra ha sido procesada exitosamente:
        
        Producto: {producto.nombre}
        Precio: ${total:,.2f}
        
        Gracias por tu compra. Te contactaremos pronto para coordinar la entrega.
        
        Saludos,
        Equipo Yamaha
        """
    else:
        mensaje = f"""
        ¡Hola {usuario.nombreCompleto}!
        
        Tu compra ha sido procesada exitosamente:
        
        Total: ${total:,.2f}
        
        Gracias por tu compra. Te contactaremos pronto para coordinar la entrega.
        
        Saludos,
        Equipo Yamaha
        """
    
    return enviar_notificacion_correo(usuario, titulo, mensaje, 'venta')


def enviar_notificacion_cotizacion(usuario, producto):
    """
    Envía notificación de solicitud de cotización
    """
    titulo = "Solicitud de cotización recibida"
    mensaje = f"""
    ¡Hola {usuario.nombreCompleto}!
    
    Hemos recibido tu solicitud de cotización para:
    
    Producto: {producto.nombre}
    
    Nuestro equipo de ventas se pondrá en contacto contigo pronto para brindarte la mejor oferta.
    
    Saludos,
    Equipo Yamaha
    """
    
    return enviar_notificacion_correo(usuario, titulo, mensaje, 'info')


def enviar_notificacion_bienvenida(usuario):
    """
    Envía notificación de bienvenida a nuevos usuarios
    """
    titulo = "¡Bienvenido a Yamaha!"
    mensaje = f"""
    ¡Hola {usuario.nombreCompleto}!
    
    ¡Bienvenido a nuestra tienda oficial de Yamaha!
    
    Ahora puedes:
    - Explorar nuestra amplia gama de motocicletas
    - Solicitar cotizaciones personalizadas
    - Realizar compras online
    - Recibir notificaciones sobre promociones especiales
    
    ¡Gracias por unirte a la familia Yamaha!
    
    Saludos,
    Equipo Yamaha
    """
    
    return enviar_notificacion_correo(usuario, titulo, mensaje, 'info')


def notificar_admin_nuevo_usuario(usuario):
    """
    Notifica a los administradores sobre un nuevo registro de usuario
    """
    try:
        # Obtener todos los administradores
        administradores = Usuarios.objects.filter(tipo__in=['administrador', 'admin'])
        
        for admin in administradores:
            if admin.notificaciones:  # Solo si el admin tiene notificaciones habilitadas
                titulo = "Nuevo usuario registrado"
                mensaje = f"""
                Se ha registrado un nuevo usuario en el sistema:
                
                Nombre: {usuario.nombreCompleto}
                Correo: {usuario.correo}
                Tipo: {usuario.tipo.title()}
                Fecha: {usuario.fecha_registro.strftime('%d/%m/%Y %H:%M')}
                
                Puedes gestionar este usuario desde el panel de administración.
                """
                
                enviar_notificacion_correo(admin, titulo, mensaje, 'registro')
                
    except Exception as e:
        logger.error(f'Error notificando a administradores sobre nuevo usuario: {str(e)}')
