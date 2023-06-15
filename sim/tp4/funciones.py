from .classes import *

def get_min_reloj(llegada_parque, estacionamiento, lista_cajas_est, lista_cajas_cont, lista_cajas_entradas):
    lista = [llegada_parque, estacionamiento] + lista_cajas_entradas + lista_cajas_cont + lista_cajas_est
    val = [0, None]
    for i in lista:
        if val[0] == 0:
            val[0] = i.valor_reloj
            val[1] = i
        else:
            if i.valor_reloj < val[0] and i.valor_reloj != 0:
                print(True)
                val[0] = i.valor_reloj
                val[1] = i
    return val

def disp_ce(lista_cajas_estacionamiento):
    for i in range(len(lista_cajas_estacionamiento)):
        if lista_cajas_estacionamiento[i].estado == "Libre":
            print(f"Caja E disponible: {i}")
            return i
    return False

def disp_caja_control(lista_cajas_control):
    for i in range(len(lista_cajas_control)):
        if lista_cajas_control[i].estado == "Libre":
            print(f"Caja CT disponible: {i}")
            return i
    return False

def mandado_a_cola(lista):
    indice = -1
    for i in range(len(lista)):
        print(len(lista[i]), indice)
        if indice == -1:
            indice = i
        if len(lista[i]) < len(lista[indice]):
            indice = i
    return indice

def tp4(desde, cantidad_mostrar, total):
    fin = {}
    llaves = {}
    lista_personas = []
    # INICIALIZACION -------------------------------------------------------------------
    cont_filas = 0
    cont_grupos = 0
    lista_grupos = []
    llegada_parque = LlegadaParque(id=1, num_grupo=0)
    llegada_grupo = LlegadaGrupo()
    cola_caja_estacionamiento = []
    cola_control = [[], [], [], []]
    cola_entradas = [[], [], []]
    lista_cajas_estacionamiento = []
    lista_cajas_control = []
    lista_cajas_entradas = []
    dicc = {"reloj": 0,
            }
    llegada_parque.calc_valor_reloj(reloj=dicc["reloj"])
    dict_metricas = {'max_cola_estacionamiento': 0,
                     'metros_de_carretera_total': 0,
                     'ac_demora_estacionar': 0,
                     'ac_estacionados': 0,
                     'ac_demora_atencion_en_caja_compra': 0,
                     'promedio_demora_atencion_en_caja_compra': 0,
                     'ac_demora_control': 0,
                     'ac_personas': 0,
                     'ac_tiempo_sistema': 0,
                     'promedio_tiempo_sistema': 0}

    estacionamiento = Estacionamiento(id=1, num_grupo=0)
    dicc.update(llegada_parque.to_dict())
    dicc.update(llegada_grupo.to_dict())
    dicc.update(estacionamiento.to_dict())
    dicc.update(dict_metricas)

    for i in range(1, 6, 1):
        lista_cajas_estacionamiento.append(LlegadaCajaEstacionamiento(id=i, estado="Libre"))
        dicc.update(lista_cajas_estacionamiento[i-1].to_dict())
    for i in range(1, 7, 1):
        lista_cajas_entradas.append(LlegadaCajaCompra(id=i))
        dicc.update(lista_cajas_entradas[i-1].to_dict())
    for i in range(1, 5, 1):
        lista_cajas_control.append(LlegadaCajaControl(id=i))
        dicc.update(lista_cajas_control[i-1].to_dict())

    # INICIALIZACION -------------------------------------------------------------------
    for i in range(1, total+1, 1):
        cont_filas += 1
        prox_reloj = get_min_reloj(llegada_parque, estacionamiento, lista_cajas_estacionamiento, lista_cajas_control, lista_cajas_entradas)
        # LLEGADA AL PARQUE
        if isinstance(prox_reloj[1], LlegadaParque):
            print("LLEGADA PARQUEEEE \n")
            # Actualizo el reloj
            dicc["reloj"] = prox_reloj[0]
            # Creo la proxima llegada al parque
            llegada_parque.calc_valor_reloj(dicc["reloj"])
            # Actualizo la llegada al parque
            dicc.update(llegada_parque.to_dict())
            # Creo el grupo que llegó
            cont_grupos += 1
            llegada_grupo.num_grupo = cont_grupos
            llegada_grupo.calc_cant_personas()
            llegada_grupo.calc_precompra()

            caja_est_disp = disp_ce(lista_cajas_estacionamiento)
            if caja_est_disp is not False:
                # Creo el grupo con estado Siendo Atendido Caja Estacionamiento
                lista_grupos.append(Grupo(id=cont_grupos, estado="SACE", hora_llegada=dicc["reloj"],
                                          tipo_entrada=llegada_grupo.tiene_precompra, cantidad_personas=llegada_grupo.cant_personas))
                # Actualizo el diccionario con los valores del nuevo grupo
                dicc.update(llegada_grupo.to_dict())
                # Calculamos el fin de atencion de la caja disponible
                lista_cajas_estacionamiento[caja_est_disp].calc_valor_reloj(dicc["reloj"])
                # Seteo estado ocupado de la caja
                lista_cajas_estacionamiento[caja_est_disp].estado = "Ocupada"
                # Seteo num grupo que atiende esa caja
                lista_cajas_estacionamiento[caja_est_disp].id_grupo = llegada_grupo.num_grupo
                # Actualizo el diccionario con la caja calculada
                dicc.update(lista_cajas_estacionamiento[caja_est_disp].to_dict())
            else:
                # Creo el grupo con estado Esperando Atencion Caja Estacionamiento
                grupo = Grupo(id=cont_grupos, estado="EACE", hora_llegada=dicc["reloj"],
                              tipo_entrada=llegada_grupo.tiene_precompra, cantidad_personas=llegada_grupo.cant_personas)
                lista_grupos.append(grupo)
                # Actualizo el diccionario con los valores del nuevo grupo
                dicc.update(llegada_grupo.to_dict())
                cola_caja_estacionamiento.append(grupo)
                if len(cola_caja_estacionamiento) > dicc["max_cola_estacionamiento"]:
                    dicc["max_cola_estacionamiento"] = len(cola_caja_estacionamiento)

        elif isinstance(prox_reloj[1], LlegadaCajaEstacionamiento):
            print("LLEGADA CAJA ESTACIONAMIENTO \n")
            # Actualizo el reloj
            dicc["reloj"] = prox_reloj[0]
            # Calculamos tiempo estacionamiento
            estacionamiento.calc_valor_reloj(dicc["reloj"])
            estacionamiento.num_grupo = prox_reloj[1].id_grupo
            dicc.update(estacionamiento.to_dict())
            if len(cola_caja_estacionamiento) > 0:
                # Transicion ocupada -> ocupada
                prox_reloj[1].estado = "Ocupada"
                # Calculo el fin de esa atencion
                prox_reloj[1].calc_valor_reloj(dicc["reloj"])
                prox_reloj[1].id_grupo = cola_caja_estacionamiento[0].id
                lista_cajas_estacionamiento[caja_est_disp] = prox_reloj[1]
                del cola_caja_estacionamiento[0]
                # Actualizo el diccionario con la nueva atencion
                dicc.update(prox_reloj[1])
            else:
                prox_reloj[1].estado = "Libre"
                prox_reloj[1].reset()
                dicc.update(prox_reloj[1].to_dict())
        elif isinstance(prox_reloj[1], Estacionamiento):
            print("LLEGADA ESTACIONAMIENTO \n")
            # Actualizo Reloj
            dicc["reloj"] = prox_reloj[0]
            # Agrego a la estadistica
            dicc["ac_estacionados"] += 1
            for grupo in lista_grupos:
                if grupo.id == prox_reloj[1].num_grupo:
                    if grupo.tipo_entrada:
                        for i in range(1, grupo.cantidad_personas+1, 1):
                            disp_caja = disp_caja_control(lista_cajas_control)
                            if disp_caja >= 0:
                                persona = Persona(estado="SC", hora_llegada=dicc["reloj"])
                                # Agrego una persona a la lista de personas
                                lista_personas.append(persona)
                                lista_cajas_control[disp_caja].estado = "Ocupada"
                                lista_cajas_control[disp_caja].calc_valor_reloj(dicc["reloj"])
                                dicc.update(lista_cajas_control[disp_caja].to_dict())
                            else:
                                persona = Persona(estado="EC", hora_llegada=dicc["reloj"])
                                lista_personas.append(persona)
                                indice = mandado_a_cola(cola_control)
                                lista_cajas_control[indice].cola += 1
                                dicc.update(lista_cajas_control[indice].to_dict())
                                cola_control[indice].append(persona)
                    else:
                        #Ir a comprar entrara
                        print("no tiene precompra")

        #elif isinstance(prox_reloj[1], LlegadaCajaCompra):
        #elif isinstance(prox_reloj[1], LlegadaCajaControl):
        if i >= desde and cont_filas <= cantidad_mostrar:
            fin[f"{cont_filas}"] = dicc.copy()
    for i in dicc.keys():
        llaves[i] = ""
    return fin, llaves
