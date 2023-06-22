from .classes import *

def get_min_reloj(llegada_parque, estacionamiento, lista_cajas_est, lista_cajas_cont, lista_cajas_entradas, llegada_premium):
    lista = [llegada_parque, estacionamiento, llegada_premium] + lista_cajas_entradas + lista_cajas_cont + lista_cajas_est
    val = [0, None]
    for i in lista:
        if val[0] == 0:
            val[0] = i.valor_reloj
            val[1] = i
        else:
            if i.valor_reloj < val[0] and i.valor_reloj != 0:
                val[0] = i.valor_reloj
                val[1] = i
    return val

def disp_ce(lista_cajas_estacionamiento):
    for i in range(len(lista_cajas_estacionamiento)):
        if lista_cajas_estacionamiento[i].estado == "Libre":
            return i
    return False

def disp_caja_control(lista_cajas_control):
    for i in range(len(lista_cajas_control)):
        if lista_cajas_control[i].estado == "Libre":
            return i
    return False

def disp_caja_entradas(lista_cajas_entradas):
    for i in range(len(lista_cajas_entradas)):
        if lista_cajas_entradas[i].estado == "Libre":
            return i
    return False

def mandado_a_cola(lista):
    indice = -1
    for i in range(len(lista)):
        if indice == -1:
            indice = i
        if len(lista[i]) < len(lista[indice]):
            indice = i
    return indice

def tp4(desde, cantidad_mostrar, total, media_est, media_caja_est, media_caja_cont, media_caja_comp, media_llegada_parque):
    fin = {}
    llaves = {}
    lista_personas = []
    # INICIALIZACION -------------------------------------------------------------------
    cont_filas = 0
    cont_grupos = 0
    cont_personas = 0
    cont_personas_premium = 0
    lista_grupos = []
    rta = {}
    llegada_parque = LlegadaParque(id=1, num_grupo=0, valor_formula=media_llegada_parque)
    llegada_grupo = LlegadaGrupo()
    llegada_premium = LlegadaPremium(id=1)
    cola_caja_estacionamiento = []
    cola_premium = []
    cola_control = [[], [], [], []]
    cola_entradas = [[], [], []]
    lista_cajas_estacionamiento = []
    lista_cajas_control = []
    lista_cajas_entradas = []
    dicc = {"reloj": 0,
            }
    llegada_parque.calc_valor_reloj(reloj=dicc["reloj"])
    dict_metricas = {'max_cola_estacionamiento': 0, #ta
                     'metros_de_carretera_total': 0, #se calcula al ultimo
                     'ac_demora_estacionar': 0, #ta
                     'ac_estacionados': 0, #ta
                     'ac_demora_atencion_en_caja_compra': 0,
                     'ac_grupos_en_caja_compra': 0,
                     'ac_demora_control': 0,
                     'ac_personas': 0, # ta
                     'ac_tiempo_sistema': 0, # ta
                     'promedio_tiempo_sistema': 0}

    estacionamiento = Estacionamiento(id=1, num_grupo=0, valor_formula=media_est)
    dicc.update(llegada_parque.to_dict())
    dicc.update(llegada_grupo.to_dict())
    dicc.update(estacionamiento.to_dict())
    dicc.update(dict_metricas)

    for i in range(1, 6, 1):
        lista_cajas_estacionamiento.append(LlegadaCajaEstacionamiento(id=i, estado="Libre", valor_formula=media_caja_est))
        dicc.update(lista_cajas_estacionamiento[i-1].to_dict())
    for i in range(1, 7, 1):
        lista_cajas_entradas.append(LlegadaCajaCompra(id=i, valor_formula=media_caja_comp))
        dicc.update(lista_cajas_entradas[i-1].to_dict())
    for i in range(1, 5, 1):
        lista_cajas_control.append(LlegadaCajaControl(id=i, valor_formula=media_caja_cont))
        dicc.update(lista_cajas_control[i-1].to_dict())
    dicc.update(llegada_premium.to_dict())
    # INICIALIZACION -------------------------------------------------------------------
    for i in range(1, total+1, 1):
        cont_filas += 1
        prox_reloj = get_min_reloj(llegada_parque, estacionamiento, lista_cajas_estacionamiento, lista_cajas_control,
                                   lista_cajas_entradas, llegada_premium)
        # LLEGADA AL PARQUE
        if isinstance(prox_reloj[1], LlegadaParque):
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
            llegada_grupo.calc_premium()

            caja_est_disp = disp_ce(lista_cajas_estacionamiento)
            if caja_est_disp is not False:
                # Creo el grupo con estado Siendo Atendido Caja Estacionamiento
                lista_grupos.append(Grupo(id=cont_grupos, estado="SACE", hora_llegada=dicc["reloj"],
                                          hora_llegada_caja_est=dicc["reloj"],
                                          tipo_entrada=llegada_grupo.tiene_precompra,
                                          cantidad_personas=llegada_grupo.cant_personas,
                                          es_premium=llegada_grupo.es_premium))
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
                              hora_llegada_caja_est=dicc["reloj"],
                              tipo_entrada=llegada_grupo.tiene_precompra, cantidad_personas=llegada_grupo.cant_personas,
                              es_premium=llegada_grupo.es_premium)
                lista_grupos.append(grupo)
                # Actualizo el diccionario con los valores del nuevo grupo
                dicc.update(llegada_grupo.to_dict())
                cola_caja_estacionamiento.append(grupo)
                # Actualizo la metrica de max cola estacionamiento si la cola ahora es mas grande
                if len(cola_caja_estacionamiento) > dicc["max_cola_estacionamiento"]:
                    dicc["max_cola_estacionamiento"] = len(cola_caja_estacionamiento)
                    dicc["metros_de_carretera_total"] = dicc["max_cola_estacionamiento"]*4

        elif isinstance(prox_reloj[1], LlegadaCajaEstacionamiento):
            # Actualizo el reloj
            dicc["reloj"] = prox_reloj[0]
            # Calculamos tiempo estacionamiento
            estacionamiento.calc_valor_reloj(dicc["reloj"])
            estacionamiento.num_grupo = prox_reloj[1].id_grupo
            estacionamiento.hora_inicio = dicc["reloj"]
            dicc.update(estacionamiento.to_dict())
            if len(cola_caja_estacionamiento) > 0:
                caja_est_disp = disp_ce(lista_cajas_estacionamiento)
                # Transicion ocupada -> ocupada
                prox_reloj[1].estado = "Ocupada"
                # Calculo el fin de esa atencion
                prox_reloj[1].calc_valor_reloj(dicc["reloj"])
                prox_reloj[1].id_grupo = cola_caja_estacionamiento[0].id
                lista_cajas_estacionamiento[caja_est_disp] = prox_reloj[1]
                del cola_caja_estacionamiento[0]
                # Actualizo el diccionario con la nueva atencion
                dicc.update(lista_cajas_estacionamiento[caja_est_disp].to_dict())
            else:
                prox_reloj[1].estado = "Libre"
                prox_reloj[1].reset()
                dicc.update(prox_reloj[1].to_dict())
        # Fin estacionamiento
        elif isinstance(prox_reloj[1], Estacionamiento):
            # Actualizo Reloj
            dicc["reloj"] = prox_reloj[0]
            # Agrego 1 a la estadistica
            dicc["ac_estacionados"] += 1
            for grupo in lista_grupos:
                if grupo.id == prox_reloj[1].num_grupo:
                    dicc["ac_demora_estacionar"] += dicc["reloj"] - grupo.hora_llegada_caja_est
                    # Tiene precompra
                    if grupo.tipo_entrada and grupo.es_premium == False:
                        for i in range(1, grupo.cantidad_personas+1, 1):
                            disp_caja = disp_caja_control(lista_cajas_control)
                            cont_personas += 1
                            if disp_caja >= 0:
                                persona = Persona(id=cont_personas, estado="SC", hora_llegada_control=dicc["reloj"], hora_llegada=grupo.hora_llegada)
                                # Agrego una persona a la lista de personas
                                lista_personas.append(persona)
                                lista_cajas_control[disp_caja].estado = "Ocupada"
                                lista_cajas_control[disp_caja].calc_valor_reloj(dicc["reloj"])
                                lista_cajas_control[disp_caja].persona = persona.id
                                dicc.update(lista_cajas_control[disp_caja].to_dict())
                            else:
                                persona = Persona(id=cont_personas, estado="EC", hora_llegada_control=dicc["reloj"], hora_llegada=grupo.hora_llegada)
                                lista_personas.append(persona)
                                indice = mandado_a_cola(cola_control)
                                dicc.update(lista_cajas_control[indice].to_dict())
                                cola_control[indice].append(persona)
                        lista_grupos.remove(grupo)
                    # Tiene precompra y es premium
                    elif grupo.tipo_entrada and grupo.es_premium:
                        for i in range(1, grupo.cantidad_personas+1, 1):
                            cont_personas_premium += 1
                            # Esta libre la caja premium
                            if llegada_premium.estado == "Libre":
                                persona = Persona(id=cont_personas_premium, estado="SCP")
                                # Agrego una persona a la lista de personas
                                #lista_personas.append(persona)
                                llegada_premium.estado = "Ocupada"
                                llegada_premium.calc_valor_reloj(dicc["reloj"])
                                llegada_premium.persona = persona.id
                                dicc.update(llegada_premium.to_dict())
                            else:
                                persona = Persona(id=cont_personas_premium, estado="ECP")
                                cola_premium.append(persona)
                    # No tiene precompra
                    else:
                        caja_entradas_disp = disp_caja_entradas(lista_cajas_entradas)
                        # Hay alguna caja disponible
                        if caja_entradas_disp >= 0:
                            lista_cajas_entradas[caja_entradas_disp].estado = "Ocupada"
                            lista_cajas_entradas[caja_entradas_disp].num_grupo = estacionamiento.num_grupo
                            lista_cajas_entradas[caja_entradas_disp].calc_valor_reloj(reloj=dicc["reloj"])
                            grupo.estado = "SACC"
                            grupo.hora_llegada_caja_compra = dicc["reloj"]
                            dicc.update(lista_cajas_entradas[caja_entradas_disp].to_dict())
                        else:
                            # Busco la cola a la que mando el grupo
                            cola_min = mandado_a_cola(cola_entradas)
                            grupo.estado = "EACC"
                            grupo.hora_llegada_caja_compra = dicc["reloj"]
                            cola_entradas[cola_min].append(grupo)
            estacionamiento.reset()
            dicc.update(estacionamiento.to_dict())

        elif isinstance(prox_reloj[1], LlegadaCajaCompra):
            dicc["reloj"] = prox_reloj[0]
            dicc["ac_grupos_en_caja_compra"] += 1
            for grupo in lista_grupos:
                if grupo.id == prox_reloj[1].num_grupo:
                    dicc["ac_demora_atencion_en_caja_compra"] += dicc["reloj"] - grupo.hora_llegada_caja_compra
            id_caja = prox_reloj[1].id - 1
            if prox_reloj[1].id <= 2 and len(cola_entradas[0]) != 0:
                grupo = cola_entradas[0].pop(0)
                lista_cajas_entradas[id_caja].calc_valor_reloj(reloj=dicc["reloj"])
                lista_cajas_entradas[id_caja].num_grupo = grupo.id
                dicc.update(lista_cajas_entradas[id_caja].to_dict())
            elif 4 >= prox_reloj[1].id > 2 and len(cola_entradas[1]) != 0:
                grupo = cola_entradas[1].pop(0)
                lista_cajas_entradas[id_caja].calc_valor_reloj(reloj=dicc["reloj"])
                lista_cajas_entradas[id_caja].num_grupo = grupo.id
                dicc.update(lista_cajas_entradas[id_caja].to_dict())
            elif 6 >= prox_reloj[1].id > 4 and len(cola_entradas[2]) != 0:
                grupo = cola_entradas[2].pop(0)
                lista_cajas_entradas[id_caja].num_grupo = grupo.id
                lista_cajas_entradas[id_caja].calc_valor_reloj(reloj=dicc["reloj"])
                dicc.update(lista_cajas_entradas[id_caja].to_dict())
            if len(cola_entradas[0]) == 0 and prox_reloj[1].id <= 2:
                lista_cajas_entradas[id_caja].reset()
                lista_cajas_entradas[id_caja].estado = "Libre"
            elif len(cola_entradas[1]) == 0 and 4 >= prox_reloj[1].id > 2:
                lista_cajas_entradas[id_caja].reset()
                lista_cajas_entradas[id_caja].estado = "Libre"
            elif len(cola_entradas[2]) == 0 and 6 >= prox_reloj[1].id > 4:
                lista_cajas_entradas[id_caja].reset()
                lista_cajas_entradas[id_caja].estado = "Libre"
            # Mando el grupo a la caja de control
            for grupo in lista_grupos:
                if grupo.id == prox_reloj[1].num_grupo:
                    dicc["ac_demora_atencion_en_caja_compra"] += dicc["reloj"] - grupo.hora_llegada_caja_compra
                    for i in range(1, grupo.cantidad_personas+1, 1):
                        cont_personas += 1
                        disp_caja = disp_caja_control(lista_cajas_control)
                        if disp_caja >= 0:
                            persona = Persona(id=cont_personas, estado="SC", hora_llegada_control=dicc["reloj"], hora_llegada=grupo.hora_llegada)
                            # Agrego una persona a la lista de personas
                            lista_personas.append(persona)
                            lista_cajas_control[disp_caja].estado = "Ocupada"
                            lista_cajas_control[disp_caja].calc_valor_reloj(dicc["reloj"])
                            lista_cajas_control[disp_caja].persona = persona.id
                            dicc.update(lista_cajas_control[disp_caja].to_dict())
                        else:
                            persona = Persona(id=cont_personas, estado="EC", hora_llegada_control=dicc["reloj"], hora_llegada=grupo.hora_llegada)
                            lista_personas.append(persona)
                            indice = mandado_a_cola(cola_control)
                            dicc.update(lista_cajas_control[indice].to_dict())
                            cola_control[indice].append(persona)

        elif isinstance(prox_reloj[1], LlegadaCajaControl):
            dicc["reloj"] = prox_reloj[0]
            p = ""
            for i in range(len(lista_personas)):
                if lista_personas[i].id == prox_reloj[1].persona:
                    p = i
            p = lista_personas.pop(i)
            dicc["ac_personas"] += 1
            dicc["ac_demora_control"] += dicc["reloj"] - p.hora_llegada_control
            dicc["ac_tiempo_sistema"] += dicc["reloj"] - p.hora_llegada
            if dicc["ac_personas"] > 0:
                dicc["promedio_tiempo_sistema"] = (dicc["ac_tiempo_sistema"] / dicc["ac_personas"])
            # Si hay gente en la cola de esa caja, la paso a atencion
            id_cola = prox_reloj[1].id
            if len(cola_control[id_cola-1]) > 0:
                a_atender = cola_control[id_cola-1].pop(0)
                lista_cajas_control[id_cola-1].calc_valor_reloj(reloj=dicc["reloj"])
                lista_cajas_control[id_cola-1].persona = a_atender.id
                dicc.update(lista_cajas_control[id_cola-1].to_dict())
            # Sino, paso a libre la caja
            else:
                lista_cajas_control[id_cola-1].reset()
                lista_cajas_control[id_cola-1].estado = "Libre"
                dicc.update(lista_cajas_control[id_cola-1].to_dict())
        if isinstance(prox_reloj[1], LlegadaPremium):
            if len(cola_premium) > 0:
                persona = cola_premium.pop(0)
                llegada_premium.estado = "Ocupada"
                llegada_premium.calc_valor_reloj(dicc["reloj"])
                llegada_premium.persona = persona.id
                dicc.update(llegada_premium.to_dict())
            else:
                llegada_premium.estado = "Libre"
                llegada_premium.reset()
                dicc.update(llegada_premium.to_dict())
        if (i >= desde and cont_filas <= cantidad_mostrar) or i == total or i == 1:
            fin[f"{cont_filas}"] = dicc.copy()
            print(i)
        if i == total:
            rta = dicc.copy()
    for i in dicc.keys():
        llaves[i] = ""
    return fin, llaves, rta
