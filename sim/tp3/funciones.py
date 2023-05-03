import random
from numpy import log, cos, pi
TABLA_AVERIAS = [
    (5, 0.25, 0, 0.249999),
    (6, 0.45, 0.25, 0.69999),
    (7, 0.20, 0.70, 0.89999),
    (8, 0.10, 0.90, 0.99999),
]

MEDIA_FUNC_MOTOR = 14
DESVIACION_FUNC_MOTOR = 1.5
COSTO_REVISION = 900
COSTO_ARREGLO = 2500

def obtener_var_normal(media: float, desviacion: float):
    rand1 = round(random.random(), 2)
    if rand1 == 0:
        rand1 = 0.01
    rand2 = round(random.random(), 2)
    normal_var = round(((((-2*log(rand1))*cos(2*pi*rand2)))*desviacion)+media, 2)
    return {'rand1': rand1, 'rand2': rand2, 'normal_var': normal_var}


def get_cant_dias_hasta_averia():
    cant_dias_hasta_averia = 0
    rand_averia = round(random.random(), 4)
    if rand_averia == 1:
        rand_averia = 0.9999
    for i in TABLA_AVERIAS:
        # Busco el día que cae la avería
        if i[3] >= rand_averia >= i[2]:
            cant_dias_hasta_averia = i[0] - 1
    return rand_averia, cant_dias_hasta_averia


def simular_e1(total_simulaciones: int, desde: int, cantidad: int, media: float, desviacion: float):
    cont = 1
    ciclo = 0
    dia = 0
    resultado = {}
    vector_estado = {}
    base_dict = {"random_averia": "", "dia_averia": "", "cant_dias_hasta_averia": "", "reparacion": "",
                 "mantenimiento": "", "total_gastos": "", "promedio_gastos": "", "total_horas_motor": "",
                 "promedio_horas": "", "ciclo": ""}
    while ciclo <= total_simulaciones:
        dia += 1
        vector_estado["actual"] = obtener_var_normal(media, desviacion)
        vector_estado["actual"] |= base_dict
        if cont == 1:
            print("Cont deberia ser 1", cont, " ", ciclo)
            rand_averia, cant_dias_hasta_averia = get_cant_dias_hasta_averia()
            dia_averia = dia + cant_dias_hasta_averia
            vector_estado["actual"]["random_averia"] = rand_averia
            vector_estado["actual"]["dia_averia"] = dia_averia
            vector_estado["actual"]["cant_dias_hasta_averia"] = cant_dias_hasta_averia
            vector_estado["actual"]["reparacion"] = "No"
            vector_estado["actual"]["mantenimiento"] = "No"
            if dia == 1:
                ciclo += 1
                vector_estado["actual"]["total_gastos"] = 0
                vector_estado["actual"]["promedio_gastos"] = round(vector_estado["actual"]["total_gastos"] / dia, 2)
                vector_estado["actual"]["total_horas_motor"] = vector_estado["actual"]["normal_var"]
                vector_estado["actual"]["promedio_horas"] = vector_estado["actual"]["normal_var"]
            else:
                vector_estado["actual"]["total_gastos"] = vector_estado["anterior"]["total_gastos"]
                vector_estado["actual"]["promedio_gastos"] = round(vector_estado["actual"]["total_gastos"] / dia, 2)
                vector_estado["actual"]["total_horas_motor"] = vector_estado["anterior"]["total_horas_motor"] +vector_estado["actual"]["normal_var"]
                vector_estado["actual"]["promedio_horas"] = round(vector_estado["actual"]["total_horas_motor"]/dia, 2)
            vector_estado["actual"]["ciclo"] = ciclo
            cont += 1

        else:
            # Estos tres son comunes a todos
            vector_estado["actual"]["random_averia"] = vector_estado["anterior"]["random_averia"]
            vector_estado["actual"]["dia_averia"] = vector_estado["anterior"]["dia_averia"]
            vector_estado["actual"]["cant_dias_hasta_averia"] = vector_estado["anterior"]["cant_dias_hasta_averia"] - 1
            # Aca entran los dias 5 y 6 en donde el motor se rompe
            if (8 >= cont >= 5) and vector_estado["anterior"]["dia_averia"] == dia:
                print("arreglo", cont, " ", ciclo)
                vector_estado["actual"]["ciclo"] = ciclo
                ciclo += 1
                vector_estado["actual"]["reparacion"] = "Si"
                vector_estado["actual"]["mantenimiento"] = "No"
                vector_estado["actual"]["total_gastos"] = vector_estado["anterior"]["total_gastos"] + COSTO_ARREGLO
                cont = 1
            # Aca entran los dias en los que no se rompe
            else:
                print("nada ", cont, " ", ciclo, vector_estado["actual"]["random_averia"] )
                cont += 1
                vector_estado["actual"]["ciclo"] = ciclo
                vector_estado["actual"]["reparacion"] = "No"
                vector_estado["actual"]["mantenimiento"] = "No"
                vector_estado["actual"]["total_gastos"] = vector_estado["anterior"]["total_gastos"]
            # Estas tres tamb son comunes a los 3 estados
            vector_estado["actual"]["promedio_gastos"] = round(vector_estado["actual"]["total_gastos"] / dia, 2)
            vector_estado["actual"]["total_horas_motor"] = vector_estado["anterior"]["total_horas_motor"] + vector_estado["actual"]["normal_var"]
            vector_estado["actual"]["promedio_horas"] = round(vector_estado["actual"]["total_horas_motor"]/dia, 2)

        vector_estado["anterior"] = vector_estado["actual"]
        if cantidad+desde >= dia >= desde:
            resultado[str(dia)] = vector_estado["actual"]
        if ((8 >= cont >= 5) and vector_estado["anterior"]["dia_averia"] == dia) and ciclo == total_simulaciones:
            resultado[str(dia)] = vector_estado["actual"]
        vector_estado["actual"] = {}
        if cont > 20:
            break
    return resultado


def simular_e2(total_simulaciones: int, desde: int, cantidad: int, media: float, desviacion: float):
    cont = 1
    ciclo = 0
    dia = 0
    resultado = {}
    vector_estado = {}
    base_dict = {"random_averia": "", "dia_averia": "", "cant_dias_hasta_averia": "", "reparacion": "",
                 "mantenimiento": "", "total_gastos": "", "promedio_gastos": "", "total_horas_motor": "",
                 "promedio_horas": "", "ciclo": ""}
    while ciclo <= total_simulaciones:
        dia += 1
        vector_estado["actual"] = obtener_var_normal(media, desviacion)
        vector_estado["actual"] |= base_dict
        if cont == 1:
            print("Cont deberia ser 1", cont)
            rand_averia, cant_dias_hasta_averia = get_cant_dias_hasta_averia()
            dia_averia = dia + cant_dias_hasta_averia
            vector_estado["actual"]["random_averia"] = rand_averia
            vector_estado["actual"]["dia_averia"] = dia_averia
            vector_estado["actual"]["cant_dias_hasta_averia"] = cant_dias_hasta_averia
            vector_estado["actual"]["reparacion"] = "No"
            vector_estado["actual"]["mantenimiento"] = "No"
            if dia == 1:
                ciclo += 1
                vector_estado["actual"]["total_gastos"] = 0
                vector_estado["actual"]["promedio_gastos"] = round(vector_estado["actual"]["total_gastos"] / dia, 2)
                vector_estado["actual"]["total_horas_motor"] = vector_estado["actual"]["normal_var"]
                vector_estado["actual"]["promedio_horas"] = vector_estado["actual"]["normal_var"]
            else:
                vector_estado["actual"]["total_gastos"] = vector_estado["anterior"]["total_gastos"]
                vector_estado["actual"]["promedio_gastos"] = round(vector_estado["actual"]["total_gastos"] / dia, 2)
                vector_estado["actual"]["total_horas_motor"] = vector_estado["anterior"]["total_horas_motor"] +vector_estado["actual"]["normal_var"]
                vector_estado["actual"]["promedio_horas"] = round(vector_estado["actual"]["total_horas_motor"]/dia, 2)
            vector_estado["actual"]["ciclo"] = ciclo
            cont += 1

        else:
            # Estos tres son comunes a todos
            vector_estado["actual"]["random_averia"] = vector_estado["anterior"]["random_averia"]
            vector_estado["actual"]["dia_averia"] = vector_estado["anterior"]["dia_averia"]
            vector_estado["actual"]["cant_dias_hasta_averia"] = vector_estado["anterior"]["cant_dias_hasta_averia"] - 1
            # Aca entran los dias 5 y 6 en donde el motor se rompe
            if (cont == 6 or cont == 5) and vector_estado["anterior"]["dia_averia"] == dia:
                print("arreglo", cont)
                vector_estado["actual"]["ciclo"] = ciclo
                ciclo += 1
                vector_estado["actual"]["reparacion"] = "Si"
                vector_estado["actual"]["mantenimiento"] = "No"
                vector_estado["actual"]["total_gastos"] = vector_estado["anterior"]["total_gastos"] + COSTO_ARREGLO
                cont = 1
            # Aca entra el dia 6 de mantenimiento nomas
            elif cont == 6:
                print("mant", cont)
                vector_estado["actual"]["ciclo"] = ciclo
                ciclo += 1
                vector_estado["actual"]["reparacion"] = "No"
                vector_estado["actual"]["mantenimiento"] = "Si"
                vector_estado["actual"]["total_gastos"] = vector_estado["anterior"]["total_gastos"] + COSTO_REVISION
                cont = 1
            # Aca entran los dias 2, 3, 4 y 5 si no se rompe
            else:
                print("nada ", cont)
                cont += 1
                vector_estado["actual"]["ciclo"] = ciclo
                vector_estado["actual"]["reparacion"] = "No"
                vector_estado["actual"]["mantenimiento"] = "No"
                vector_estado["actual"]["total_gastos"] = vector_estado["anterior"]["total_gastos"]
            # Estas tres tamb son comunes a los 3 estados
            vector_estado["actual"]["promedio_gastos"] = round(vector_estado["actual"]["total_gastos"] / dia, 2)
            vector_estado["actual"]["total_horas_motor"] = vector_estado["anterior"]["total_horas_motor"] + vector_estado["actual"]["normal_var"]
            vector_estado["actual"]["promedio_horas"] = round(vector_estado["actual"]["total_horas_motor"]/dia, 2)

        vector_estado["anterior"] = vector_estado["actual"]
        if cantidad+desde >= dia >= desde:
            resultado[str(dia)] = vector_estado["actual"]
        if (((6 >= cont >= 5) and vector_estado["anterior"]["dia_averia"] == dia) or cont == 6) and ciclo == total_simulaciones:
            resultado[str(dia)] = vector_estado["actual"]
        vector_estado["actual"] = {}
    return resultado
