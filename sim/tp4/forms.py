from django.forms import IntegerField, TextInput, Select, Form, CharField, ModelChoiceField, Textarea, PasswordInput, \
    SelectMultiple, ModelMultipleChoiceField, BooleanField, CheckboxInput, FloatField


class Tp4Form(Form):
    cantidad_simulaciones = IntegerField(label='Cantidad de ciclos de simulaciones', widget=TextInput(attrs={'class': 'form-control'}))
    mostrar_desde = IntegerField(label='Desde que dia de simulación mostrar', widget=TextInput(attrs={'class': 'form-control'}))
    cuantas_mostrar = IntegerField(label='Cuántos días mostrar?', widget=TextInput(attrs={'class': 'form-control'}))
    media = FloatField(label="Media", widget=TextInput(attrs={'class': 'form-control'}))
    desviacion = FloatField(label="Desviación Estándar", widget=TextInput(attrs={'class': 'form-control'}))