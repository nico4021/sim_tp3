from django.shortcuts import render
from django.shortcuts import render
from .forms import Tp4Form
from .funciones import tp4


# Create your views here.
def tp4_view(request):
    if request.method == "POST":
        formulario = Tp4Form(request.POST)
        if formulario.is_valid():
            cantidad_simulaciones = formulario.cleaned_data["cantidad_simulaciones"]
            mostrar_desde = formulario.cleaned_data["mostrar_desde"]
            cuantas_mostrar = formulario.cleaned_data["cuantas_mostrar"]
            media = formulario.cleaned_data["media"]
            desviacion = formulario.cleaned_data["desviacion"]
            a, llaves = tp4(mostrar_desde, cuantas_mostrar, cantidad_simulaciones)
            return render(request, 'tp4.html', {'form': formulario, "contexto1": a, "llaves": llaves})
    else:
        formulario = Tp4Form()
        return render(request, 'tp4.html', {'form': formulario, 'error': "a"})