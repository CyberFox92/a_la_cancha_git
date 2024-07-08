from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Cancha, Salon, Alquiler, Contacto

# Register your models here.
class CustomUserAdmin(UserAdmin):
    """Usuario para la vista admin de Django"""
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'celular')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'celular', 'is_staff')


class CanchaAdmin(admin.ModelAdmin):
    """Cancha para la vista admin de Django"""
    fields = ['nombre', 'capacidad', 'tipo']
    list_display = ['nombre', 'capacidad', 'tipo']
    
admin.site.register(Cancha, CanchaAdmin)

class SalonAdmin(admin.ModelAdmin):
    """Salon para la vista admin de Django"""
    fields = ['nombre', 'invitados', 'precio_persona']
    list_display = ['nombre', 'invitados', 'precio_persona']
    
admin.site.register(Salon, SalonAdmin)

class AlquilerAdmin(admin.ModelAdmin):
    """Alquiler para la vista admin de Django"""
    fields = ['usuario', 'cancha', 'salon', 'fecha_alquiler', 'turno']
    list_display = ['usuario', 'cancha', 'salon', 'fecha_alquiler', 'turno']
    
admin.site.register(Alquiler, AlquilerAdmin)

class ContactoAdmin(admin.ModelAdmin):
    """Contacto para la vista admin de Django"""
    fields = ['nombre', 'email', 'consulta']
    list_display = ['nombre', 'email', 'consulta']
    
admin.site.register(Contacto, ContactoAdmin)
