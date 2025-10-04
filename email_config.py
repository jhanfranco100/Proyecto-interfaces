# Configuración de correo para Yamaha
# Este archivo contiene las credenciales para enviar correos

# IMPORTANTE: Para usar Gmail, necesitas:
# 1. Habilitar la verificación en 2 pasos en tu cuenta de Gmail
# 2. Generar una "Contraseña de aplicación" específica para esta aplicación
# 3. Usar esa contraseña de aplicación aquí, NO tu contraseña normal

# Configuración de Gmail SMTP
GMAIL_USER = 'tu_correo@gmail.com'  # Cambiar por tu correo de Gmail
GMAIL_PASSWORD = 'tu_contraseña_de_aplicacion'  # Contraseña de aplicación de Gmail

# Configuración alternativa para otros proveedores:
# Outlook/Hotmail:
# EMAIL_HOST = 'smtp-mail.outlook.com'
# EMAIL_PORT = 587

# Yahoo:
# EMAIL_HOST = 'smtp.mail.yahoo.com'
# EMAIL_PORT = 587

# Para desarrollo local (solo mostrar en consola):
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

