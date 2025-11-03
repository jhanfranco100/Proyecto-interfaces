from django.core.mail import send_mail

def enviar_notificacion_compra(usuario, producto, total):
    """
    Envía un correo al usuario cuando realiza una compra.
    """
    asunto = "Confirmación de compra - Kronomotos"
    mensaje = f"""
Hola {usuario.nombreCompleto},

Gracias por tu compra en Kronomotos.

Detalles de la transacción:
- Total: ${total:,.2f}

Nos comunicaremos contigo cuando tu pedido esté en camino.

Atentamente,
El equipo de Kronomotos
"""
    destinatario = [usuario.correo]
    send_mail(asunto, mensaje, None, destinatario, fail_silently=False)
