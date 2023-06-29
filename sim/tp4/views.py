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
            media_llegada_parque = formulario.cleaned_data["media_llegada_parque"]
            media_llegada_caja_est = formulario.cleaned_data["media_llegada_caja_est"]
            media_llegada_caja_cont = formulario.cleaned_data["media_llegada_caja_cont"]
            media_llegada_caja_comp = formulario.cleaned_data["media_llegada_caja_comp"]
            media_estacionamiento = formulario.cleaned_data["media_estacionamiento"]
            a, llaves, rta = tp4(mostrar_desde,
                            cuantas_mostrar,
                            cantidad_simulaciones,
                            media_estacionamiento,
                            media_llegada_caja_est,
                            media_llegada_caja_cont,
                            media_llegada_caja_comp,
                            media_llegada_parque)

            rta["promedio_tiempo_estacionamiento"] = rta["ac_demora_estacionar"] / rta["ac_estacionados"] if rta["ac_estacionados"] !=0 else 0
            rta["promedio_tiempo_control"] = rta["ac_demora_control"] / rta["ac_personas"] if rta["ac_personas"] !=0 else 0
            rta["promedio_tiempo_compra"] = rta["ac_demora_atencion_en_caja_compra"] / rta["ac_grupos_en_caja_compra"] if rta["ac_grupos_en_caja_compra"] !=0 else 0
            return render(request, 'tp4.html', {'form': formulario, "contexto1": a, "llaves": llaves, "rta": rta})
    else:
        formulario = Tp4Form()
        return render(request, 'tp4.html', {'form': formulario, 'error': "a"})