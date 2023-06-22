from django.forms import IntegerField, TextInput, Select, Form, CharField, ModelChoiceField, Textarea, PasswordInput, \
    SelectMultiple, ModelMultipleChoiceField, BooleanField, CheckboxInput, FloatField


class Tp4Form(Form):
    cantidad_simulaciones = IntegerField(label='Cantidad de filas a simular?', widget=TextInput(attrs={'class': 'form-control'}))
    mostrar_desde = IntegerField(label='Desde que línea de simulación mostrar?', widget=TextInput(attrs={'class': 'form-control'}))
    cuantas_mostrar = IntegerField(label='Cuántas líneas mostrar?', widget=TextInput(attrs={'class': 'form-control'}))
    media_llegada_parque = FloatField(label="Media Llegada Parque(min)", widget=TextInput(attrs={'class': 'form-control'}))
    media_llegada_caja_est = FloatField(label="Media Atención Caja Estacionamiento(min)", widget=TextInput(attrs={'class': 'form-control'}))
    media_llegada_caja_cont = FloatField(label="Media Atención Caja Control(min)", widget=TextInput(attrs={'class': 'form-control'}))
    media_llegada_caja_comp = FloatField(label="Media Atención Caja Entradas(min)", widget=TextInput(attrs={'class': 'form-control'}))
    media_estacionamiento = FloatField(label="Media Tiempo de Estacionamiento", widget=TextInput(attrs={'class': 'form-control'}))