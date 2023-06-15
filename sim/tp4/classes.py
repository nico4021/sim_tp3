from abc import ABC, abstractmethod
import random
from numpy import log

PROB_PERSONAS = [
    (3, 0, 0.24),
    (4, 0.25, 0.74),
    (5, 0.75, 0.9999),
]

def get_rand():
    rnd = round(random.uniform(0, 1), 4)
    if rnd == 1:
        rnd = 0.9999
    return rnd

class Evento(ABC):
    def __init__(self, id, rand=0, valor=0, valor_reloj=0, *args, **kwargs):
        self.id = id
        self.rand = rand
        self.valor = valor
        self.valor_reloj = valor_reloj

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def calc_valor_reloj(self, reloj):
        pass

    def reset(self):
        self.rand = 0
        self.valor = 0
        self.valor_reloj = 0

class LlegadaCajaEstacionamiento(Evento):
    def __init__(self, estado="Libre", id_grupo=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.estado = estado
        self.id_grupo = id_grupo

    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            if llave == "id":
                continue
            d[f"Caja Est {self.id} - {llave}"] = valor
        return d

    def calc_valor_reloj(self, reloj):
        self.rand = get_rand()
        self.valor = -0.483*log(1-self.rand)
        self.valor_reloj = reloj + self.valor

class LlegadaParque(Evento):
    def __init__(self, num_grupo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_grupo = num_grupo

    def calc_valor_reloj(self, reloj):
        self.rand = get_rand()
        self.valor = -40*log(1-self.rand)
        self.valor_reloj = reloj + self.valor

    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            if llave == "id":
                continue
            d[f"LlegadaParque - {llave}"] = valor
        return d

class LlegadaCajaCompra:
    def __init__(self, id, cola=0, estado1="Libre", rnd_atencion_1=0, demora_atencion_1=0, fin_atencion_1=0, estado2="Libre" ,
                 rnd_atencion_2=0, demora_atencion_2=0, fin_atencion_2=0, id_grupo1=0, id_grupo2=0):
        self.id = id
        self.cola = cola
        self.estado1 = estado1
        self.rnd_atencion_1 = rnd_atencion_1
        self.demora_atencion_1 = demora_atencion_1
        self.fin_atencion_1 = fin_atencion_1
        self.id_grupo1 = id_grupo1
        self.estado2 = estado2
        self.rnd_atencion_2 = rnd_atencion_2
        self.demora_atencion_2 = demora_atencion_2
        self.fin_atencion_2 = fin_atencion_2
        self.id_grupo2 = id_grupo2

    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            if llave == "id":
                continue
            d[f"CajaEntradas{self.id} - {llave}"] = valor
        return d

    def calc_valor_reloj_1(self, reloj):
        self.rnd_atencion_1 = get_rand()
        self.demora_atencion_1 = -1.533*log(1-self.rnd_atencion_1)
        self.fin_atencion_1 = self.demora_atencion_1 + reloj

    def calc_valor_reloj_2(self, reloj):
        self.rnd_atencion_2 = get_rand()
        self.demora_atencion_2 = -1.533*log(1-self.rnd_atencion_1)
        self.fin_atencion_2 = self.demora_atencion_2 + reloj

    def reset1(self):
        self.rnd_atencion_1 = 0
        self.demora_atencion_1 = 0
        self.fin_atencion_1 = 0

    def reset2(self):
        self.rnd_atencion_2 = 0
        self.demora_atencion_2 = 0
        self.fin_atencion_2 = 0

class LlegadaCajaControl(Evento):
    def __init__(self, estado="Libre", cola=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.estado = estado
        self.cola = cola

    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            if llave == "id":
                continue
            d[f"Caja Control {self.id} - {llave}"] = valor
        return d

    def calc_valor_reloj(self, reloj):
        self.rand = get_rand()
        self.valor = -0.083*log(1-self.rand)
        self.valor_reloj = self.valor + reloj


class Grupo:
    def __init__(self, id, estado, cantidad_personas=0, tipo_entrada=None, hora_llegada=None,
                 hora_llegada_estacionamiento=None, hora_llegada_caja_est=None, hora_llegada_caja_compra=None):
        self.id = id
        self.estado = estado
        self.cantidad_personas = cantidad_personas
        self.tipo_entrada = tipo_entrada
        self.hora_llegada = hora_llegada
        self.hora_llegada_estacionamiento = hora_llegada_estacionamiento
        self.hora_llegada_caja_est = hora_llegada_caja_est
        self.hora_llegada_caja_compra = hora_llegada_caja_compra

    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            if llave == "id":
                continue
            d[f"G {self.id} - {llave}"] = valor
        return d


class LlegadaGrupo:

    def __init__(self, rnd_cant_personas=0, cant_personas=0, num_grupo=0, rnd_precompra=0, tiene_precompra=None):
        self.num_grupo = num_grupo
        self.rnd_cant_personas = rnd_cant_personas
        self.cant_personas = cant_personas
        self.rnd_precompra = rnd_precompra
        self.tiene_precompra = tiene_precompra

    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            d[f"Grupos - {llave}"] = valor
        return d

    def calc_cant_personas(self):
        self.rnd_cant_personas = get_rand()
        for i in PROB_PERSONAS:
            if i[1] <= self.rnd_cant_personas <= i[2]:
                self.cant_personas = i[0]

    def calc_precompra(self):
        self.rnd_precompra = get_rand()
        if 0 <= self.rnd_precompra <= 0.419:
            self.tiene_precompra = False
        elif 0.42 <= self.rnd_precompra <= 0.999:
            self.tiene_precompra = True


class Estacionamiento(Evento):

    def __init__(self, num_grupo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_grupo = num_grupo

    def calc_valor_reloj(self, reloj):
        self.rand = get_rand()
        self.valor = -5*log(1-self.rand)
        self.valor_reloj = reloj + self.valor

    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            if llave=="id":
                continue
            d[f"Estacionamiento - {llave}"] = valor
        return d

    def reset(self):
        self.rand = 0
        self.valor = 0
        self.valor_reloj = 0

class Persona:
    def __init__(self, estado, hora_llegada):
        self.estado = estado
        self.hora_llegada = hora_llegada

    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            d[f"G {self.id} - {llave}"] = valor
        return d