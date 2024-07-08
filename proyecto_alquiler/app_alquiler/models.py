from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from datetime import date


class Usuario(AbstractUser):
    """Modelo de los usuarios, hereda de el modelo default dde Django"""
    celular = models.CharField(max_length=25, blank=True, default="Sin numero registrado")

    class Meta:
        db_table = "Usuarios"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    groups = models.ManyToManyField(
        Group,
        related_name='usuario_groups' 
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_permissions'  
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

Usuario.groups.related_name = 'user_groups'
Usuario.user_permissions.related_name = 'user_permissions'

class PerfilUsuario(models.Model):
    """Modelo usado para almacenar el numero de celular vinculado al id del usuario"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    celular = models.CharField(max_length=30, blank=True, default="Sin número registrado")

class Cancha(models.Model):
    """Modelo para creacion canchas"""
    TIPO_CHOICES = (
        ('futbol_5', 'Fútbol 5'),
        ('futbol_7', 'Fútbol 7'),
        ('futbol_11', 'Fútbol 11'),
    )
    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    precio_hora=models.IntegerField(default=1800)

    class Meta:
        db_table = "Canchas"
        verbose_name = "Cancha"
        verbose_name_plural = "Canchas"

    def __str__(self):
        return self.nombre

class Salon(models.Model):
    """Modelo para creacion de salones"""
    nombre = models.CharField(max_length=100)
    invitados = models.IntegerField(default=0)
    precio_persona= models.IntegerField(default=750)

    class Meta:
        db_table = "Salones"
        verbose_name = "Salón"
        verbose_name_plural = "Salones"

    def __str__(self):
        return self.nombre

class Alquiler(models.Model):
    """Modelo para la creacion de alquileres"""
    TURNO_CHOICES = (
        ('manana', 'Mañana'),
        ('tarde', 'Tarde'),
        ('noche', 'Noche'),
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, null=True, blank=True)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, null=True, blank=True)
    fecha_alquiler = models.DateField()
    turno = models.CharField(max_length=10, choices=TURNO_CHOICES)
    cantidad_personas = models.PositiveBigIntegerField(null=True, blank=True)
    horas_alquiler = models.PositiveBigIntegerField(null=True, blank=True)
    pago = models.BooleanField(default=False)
 
    class Meta:
        db_table = "Alquileres"
        verbose_name = "Alquiler"
        verbose_name_plural = "Alquileres"

    def clean(self):
        """Verifica que los datos esten completos antes de guardar el alquiler"""
        from django.core.exceptions import ValidationError
        if not self.cancha and not self.salon:
            raise ValidationError('Debe seleccionar una cancha o un salón.')
        if self.cancha and self.salon:
            raise ValidationError('No puede seleccionar ambos, cancha y salón.')
        if self.cancha and not self.horas_alquiler:
            raise ValidationError('Debe especificar la cantidad de horas para el alquiler de la cancha.')
        if self.salon and not self.cantidad_personas:
            raise ValidationError('Debe especificar la cantidad de personas para el alquiler del salón.')
        
    def is_vigente(self):
        """Segun la fecha actual evalua si el alquiler esta vigente o no"""
        return self.fecha_alquiler >= date.today()
    
    def costo(self):
        """Toma las horas del alquiler y lo multiplica por el costo para calcular el total"""
        if self.cancha:
            return self.cancha.precio_hora * self.horas_alquiler
        if self.salon:
            return self.salon.precio_persona * self.cantidad_personas
        return 0

    def __str__(self):
        return f"Alquiler por {self.usuario} el {self.fecha_alquiler} para {self.turno}"
    
    
class Contacto(models.Model):
    """Modelo de contactos para las consultas"""
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    celular = models.CharField(max_length=20)
    consulta = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Contactos"
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"

    def __str__(self):
        return self.nombre