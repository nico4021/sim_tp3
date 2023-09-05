from django.forms import IntegerField, TextInput, Select, Form, CharField, ModelChoiceField, Textarea, PasswordInput, \
    SelectMultiple, ModelMultipleChoiceField, BooleanField, CheckboxInput, FloatField


class FormBase(Form):
    class Meta:
        abstract = True
    cantidad = IntegerField(label='Cantidad de nùmeros a generar?', widget=TextInput(attrs={'class': 'form-control'}))
    intervalos = IntegerField(label='En cuántos intervalos dividir los números?', widget=TextInput(attrs={'class': 'form-control'}))


class Tp2Uniforme(FormBase):
    valor_min = IntegerField(label='Valor mínimo(a)', widget=TextInput(attrs={'class': 'form-control'}))
    valor_max = IntegerField(label='Valor máximo(b)', widget=TextInput(attrs={'class': 'form-control'}))


class Tp2Normal(FormBase):
    media = IntegerField(label='Media(u)', widget=TextInput(attrs={'class': 'form-control'}))
    varianza = IntegerField(label='Varianza(v)', widget=TextInput(attrs={'class': 'form-control'}))


class Tp2Poisson(FormBase):
    var_lambda = IntegerField(label='Lambda', widget=TextInput(attrs={'class': 'form-control'}))


class Tp2Exponencial(FormBase):
    var_lambda = IntegerField(label='Lambda', widget=TextInput(attrs={'class': 'form-control'}))