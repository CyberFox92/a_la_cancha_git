from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Alquiler

class UsuarioRegistro(UserCreationForm):
    """Usa el formulario de usuario estandar de Django agregando tambien el celular a la tabla relacionada"""
    celular = forms.CharField(max_length=20, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['celular'].initial = 'Sin número registrado'
    
    def clean_celular(self):
        """Al guardar el formulario vincula el celular al usuario"""
        celular = self.cleaned_data['celular']
        if not celular:
            return 'Sin número registrado'
        return celular
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'celular', 'email', 'password1', 'password2']


class AlquilerCanchaForm(forms.ModelForm):
    """Formulario para el alquiler de cancha"""
    class Meta:
        model = Alquiler
        fields = ['usuario', 'cancha', 'fecha_alquiler', 'turno', 'horas_alquiler', "pago"]
        widgets = {
            'fecha_alquiler': forms.DateInput(attrs={'type': 'date'}),
            'usuario':forms.HiddenInput(),
            'pago': forms.RadioSelect(choices=((1, 'Pago'), (0, 'Pendiente'))),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['usuario'].initial = user
        self.fields['usuario'].disabled = True
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Alquilar Cancha'))

    def clean(self):
        cleaned_data = super().clean()
        cancha = cleaned_data.get('cancha')
        horas_alquiler = cleaned_data.get('horas_alquiler')

        if not cancha:
            raise forms.ValidationError('Debe seleccionar una cancha.')
        if not horas_alquiler:
            raise forms.ValidationError('Debe especificar la cantidad de horas para el alquiler de la cancha.')
        return cleaned_data

class AlquilerSalonForm(forms.ModelForm):
    """Formulario para el alquiler de salon"""        
    class Meta:
        
        model = Alquiler
        fields = ['usuario', 'salon', 'fecha_alquiler', 'turno', 'cantidad_personas', 'pago']
        widgets = {
            'fecha_alquiler': forms.DateInput(attrs={'type': 'date'}),
            'usuario': forms.HiddenInput(),
            'pago': forms.RadioSelect(choices=((1, 'Pago'), (0, 'Pendiente'))),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        self.fields['usuario'].initial = user
        self.fields['usuario'].disabled = True
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Alquilar Salón'))

    def clean(self):
        cleaned_data = super().clean()
        salon = cleaned_data.get('salon')
        cantidad_personas = cleaned_data.get('cantidad_personas')

        if not salon:
            raise forms.ValidationError('Debe seleccionar un salón.')
        if not cantidad_personas:
            raise forms.ValidationError('Debe especificar la cantidad de personas para el alquiler del salón.')
        
        return cleaned_data
    
