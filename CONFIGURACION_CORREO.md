# 📧 Configuración de Correo Electrónico - Yamaha

## Configuración para Gmail

### Paso 1: Preparar tu cuenta de Gmail

1. **Habilitar verificación en 2 pasos:**
   - Ve a tu cuenta de Google
   - Seguridad → Verificación en 2 pasos
   - Actívala si no está activada

2. **Generar contraseña de aplicación:**
   - Ve a Seguridad → Contraseñas de aplicaciones
   - Selecciona "Correo" y "Otro (nombre personalizado)"
   - Escribe "Yamaha Notifications"
   - Copia la contraseña generada (16 caracteres)

### Paso 2: Configurar el proyecto

1. **Editar `yamaha/settings.py`:**
   ```python
   EMAIL_HOST_USER = 'tu_correo@gmail.com'  # Tu correo de Gmail
   EMAIL_HOST_PASSWORD = 'tu_contraseña_de_aplicacion'  # La contraseña de 16 caracteres
   DEFAULT_FROM_EMAIL = 'tu_correo@gmail.com'  # Tu correo de Gmail
   ```

2. **Probar la configuración:**
   ```bash
   python manage.py test_email --email tu_correo@gmail.com
   ```

### Paso 3: Configuración alternativa para otros proveedores

#### Outlook/Hotmail:
```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_correo@outlook.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña'
```

#### Yahoo:
```python
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_correo@yahoo.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña_de_aplicacion'
```

## Comandos de Prueba

### Enviar correo de prueba a un usuario específico:
```bash
python manage.py test_email --email usuario@ejemplo.com
```

### Enviar correo de prueba a todos los usuarios:
```bash
python manage.py test_email --todos
```

## Tipos de Notificaciones

El sistema envía automáticamente correos para:

1. **Bienvenida** - Al registrarse
2. **Compra realizada** - Al comprar un producto
3. **Solicitud de cotización** - Al solicitar una cotización
4. **Promociones** - Notificaciones especiales (futuro)

## Solución de Problemas

### Error: "Authentication failed"
- Verifica que la verificación en 2 pasos esté activada
- Usa la contraseña de aplicación, no tu contraseña normal
- Verifica que el correo esté correcto

### Error: "Connection refused"
- Verifica tu conexión a internet
- Verifica que el puerto 587 no esté bloqueado
- Prueba con otro proveedor de correo

### Los correos van a spam
- Agrega el correo remitente a tus contactos
- Verifica la configuración de spam de tu proveedor
- Usa un correo con buena reputación

## Para Desarrollo Local

Si quieres ver los correos en la consola en lugar de enviarlos:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Los correos aparecerán en la terminal donde ejecutas `python manage.py runserver`.

