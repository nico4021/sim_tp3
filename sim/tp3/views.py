from django.shortcuts import render
from .forms import Tp3Form
from .funciones import simular_e1, simular_e2

def index_view(request):
    return render(request, 'index.html')

def tp3_view(request):
    if request.method == "POST":
        formulario = Tp3Form(request.POST)
        if formulario.is_valid():
            cantidad_simulaciones = formulario.cleaned_data["cantidad_simulaciones"]
            mostrar_desde = formulario.cleaned_data["mostrar_desde"]
            cuantas_mostrar = formulario.cleaned_data["cuantas_mostrar"]
            media = formulario.cleaned_data["media"]
            desviacion = formulario.cleaned_data["desviacion"]
            contexto1 = simular_e1(cantidad_simulaciones, mostrar_desde, cuantas_mostrar, media, desviacion)
            contexto2 = simular_e2(cantidad_simulaciones, mostrar_desde, cuantas_mostrar, media, desviacion)
            return render(request, 'tp3.html', {'form': formulario, "contexto1": contexto1, 'contexto2': contexto2})
    else:
        formulario = Tp3Form()
        return render(request, 'tp3.html', {'form': formulario, 'error': "a"})