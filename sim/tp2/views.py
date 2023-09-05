from django.shortcuts import render
from .forms import Tp2Poisson, Tp2Normal, Tp2Uniforme, Tp2Exponencial
from .funciones import generateUniformes, generateNormales, generatePoissones, generateExponenciales

# Create your views here.
def tp2_view(request):
    return render(request, 'tp2.html')

def tp2_normal(request):
    if request.method == "POST":
        formulario = Tp2Normal(request.POST)
        if formulario.is_valid():
            cantidad = formulario.cleaned_data["cantidad"]
            intervalos = formulario.cleaned_data["intervalos"]
            media = formulario.cleaned_data["media"]
            varianza = formulario.cleaned_data["varianza"]
            generateNormales(cantidad, intervalos, media, varianza)
            return render(request, 'tp2_normal.html')
    else:
        formulario = Tp2Normal()
        return render(request, 'tp2_normal.html', {'form': formulario, 'error': "a"})

def tp2_exponencial(request):
    if request.method == "POST":
        formulario = Tp2Exponencial(request.POST)
        if formulario.is_valid():
            cantidad = formulario.cleaned_data["cantidad"]
            intervalos = formulario.cleaned_data["intervalos"]
            var_lambda = formulario.cleaned_data["var_lambda"]
            generateExponenciales(cantidad, intervalos, var_lambda)
            return render(request, 'tp2_exponencial.html')
    else:
        formulario = Tp2Exponencial()
        return render(request, 'tp2_exponencial.html', {'form': formulario, 'error': "a"})

def tp2_poisson(request):
    if request.method == "POST":
        formulario = Tp2Poisson(request.POST)
        if formulario.is_valid():
            cantidad = formulario.cleaned_data["cantidad"]
            intervalos = formulario.cleaned_data["intervalos"]
            var_lambda = formulario.cleaned_data["var_lambda"]
            generatePoissones(cantidad, intervalos, var_lambda)
            return render(request, 'tp2_poisson.html')
    else:
        formulario = Tp2Poisson()
        return render(request, 'tp2_poisson.html', {'form': formulario, 'error': "a"})

def tp2_uniforme(request):
    if request.method == "POST":
        formulario = Tp2Uniforme(request.POST)
        if formulario.is_valid():
            cantidad = formulario.cleaned_data["cantidad"]
            intervalos = formulario.cleaned_data["intervalos"]
            valor_min = formulario.cleaned_data["valor_min"]
            valor_max = formulario.cleaned_data["valor_max"]
            generateUniformes(cantidad, intervalos, valor_min, valor_max)
            return render(request, 'tp2_uniforme.html')
    else:
        formulario = Tp2Uniforme()
        return render(request, 'tp2_uniforme.html', {'form': formulario, 'error': "a"})
