from django.contrib import admin
from django.urls import path,include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('',include('core.urls')),
    path('admin/', admin.site.urls),
    #secreto de toda la implementacion del login
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,  
    })
]
