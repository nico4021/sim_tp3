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
            contexto3 = {}
            ultima_fila_e1 = list(contexto1.items())[-1][1]
            ultima_fila_e2 = list(contexto2.items())[-1][1]
            contexto3["prom_func_e1"] = ultima_fila_e1["promedio_horas"]
            contexto3["prom_gastos_e1"] = ultima_fila_e1["promedio_gastos"]
            contexto3["max_fun_e1"] = ultima_fila_e1["max_hora_historico"]
            contexto3["prom_func_e2"] = ultima_fila_e2["promedio_horas"]
            contexto3["prom_gastos_e2"] = ultima_fila_e2["promedio_gastos"]
            contexto3["max_fun_e2"] = ultima_fila_e2["max_hora_historico"]
            return render(request, 'tp3.html', {'form': formulario, "contexto1": contexto1, 'contexto2': contexto2, "contexto3": contexto3})
    else:
        formulario = Tp3Form()
        return render(request, 'tp3.html', {'form': formulario, 'error': "a"})