from abc import ABC, abstractmethod
import random
from numpy import log

PROB_PERSONAS = [
    (5, 0, 0.24),
    (3, 0.25, 0.74),
    (4, 0.75, 0.9999),
]

def get_rand():
    rnd = round(random.uniform(0, 1), 4)
    if rnd == 1:
        rnd = 0.9999
    return rnd

class Evento(ABC):
    def __init__(self, id, rand=0, valor=0, valor_reloj=0, valor_formula=0, *args, **kwargs):
        self.id = id
        self.rand = rand
        self.valor = valor
        self.valor_reloj = valor_reloj
        self.valor_formula = valor_formula

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
            if llave == "id" or llave == "valor_formula":
                continue
            d[f"Caja Est {self.id} - {llave}"] = valor
        return d

    def calc_valor_reloj(self, reloj):
        self.rand = get_rand()
        self.valor = -self.valor_formula*log(1-self.rand)
        self.valor_reloj = reloj + self.valor

    def reset(self):
        super(LlegadaCajaEstacionamiento, self).reset()
        self.id_grupo = 0

class LlegadaParque(Evento):
    def __init__(self, num_grupo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_grupo = num_grupo

    def calc_valor_reloj(self, reloj):
        self.rand = get_rand()
        self.valor = -self.valor_formula*log(1-self.rand)
        self.valor_reloj = reloj + self.valor

    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            if llave == "id" or llave == "valor_formula":
                continue
            d[f"LlegadaParque - {llave}"] = valor
        return d


class LlegadaCajaCompra(Evento):
    def __init__(self, num_grupo=0, estado="Libre", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.estado = estado
        self.num_grupo = num_grupo
    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            if llave == "id" or llave == "valor_formula":
                continue
            d[f"CajaEntradas{self.id} - {llave}"] = valor
        return d

    def calc_valor_reloj(self, reloj):
        self.rand = get_rand()
        self.valor = -self.valor_formula*log(1-self.rand)
        self.valor_reloj = self.valor + reloj

    def reset(self):
        self.rand = 0
        self.valor = 0
        self.valor_reloj = 0
        self.num_grupo = 0

class LlegadaCajaControl(Evento):
    def __init__(self, estado="Libre", persona=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.estado = estado
        self.persona = persona

    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            if llave == "id" or llave == "valor_formula":
                continue
            d[f"Caja Control {self.id} - {llave}"] = valor
        return d

    def calc_valor_reloj(self, reloj):
        self.rand = get_rand()
        self.valor = -self.valor_formula*log(1-self.rand)
        self.valor_reloj = self.valor + reloj

    def reset(self):
        super(LlegadaCajaControl, self).reset()
        self.persona = 0


class Grupo:
    def __init__(self, id, estado, cantidad_personas=0, tipo_entrada=None, hora_llegada=None,
                 hora_llegada_estacionamiento=None, hora_llegada_caja_est=None, hora_llegada_caja_compra=None, es_premium = None):
        self.id = id
        self.estado = estado
        self.cantidad_personas = cantidad_personas
        self.tipo_entrada = tipo_entrada
        self.es_premium = es_premium
        self.hora_llegada = hora_llegada
        self.hora_llegada_estacionamiento = hora_llegada_estacionamiento
        self.hora_llegada_caja_est = hora_llegada_caja_est
        self.hora_llegada_caja_compra = hora_llegada_caja_compra

    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            if llave == "id" or llave == "valor_formula":
                continue
            d[f"G {self.id} - {llave}"] = valor
        return d


class LlegadaGrupo:

    def __init__(self, rnd_cant_personas=0, cant_personas=0, num_grupo=0, rnd_precompra=0, tiene_precompra=None,
                 rnd_premium=0, es_premium=None):
        self.num_grupo = num_grupo
        self.rnd_cant_personas = rnd_cant_personas
        self.cant_personas = cant_personas
        self.rnd_precompra = rnd_precompra
        self.tiene_precompra = tiene_precompra
        self.rnd_premium = rnd_premium
        self.es_premium = es_premium

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

    def calc_premium(self):
        self.rnd_premium = get_rand()
        if self.tiene_precompra:
            if 0 <= self.rnd_premium <= 0.89:
                self.es_premium = False
            elif 0.9 <= self.rnd_premium <= 0.99999:
                self.es_premium = True


class Estacionamiento(Evento):

    def __init__(self, num_grupo, hora_inicio=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_grupo = num_grupo
        self.hora_inicio = hora_inicio

    def calc_valor_reloj(self, reloj):
        self.rand = get_rand()
        self.valor = -self.valor_formula*log(1-self.rand)
        self.valor_reloj = reloj + self.valor

    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            if llave == "id" or llave == "valor_formula":
                continue
            d[f"Estacionamiento - {llave}"] = valor
        return d

    def reset(self):
        self.rand = 0
        self.valor = 0
        self.num_grupo = 0
        self.valor_reloj = 0
        self.hora_inicio = 0

class LlegadaPremium(Evento):
    def __init__(self, persona=0, estado="Libre", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persona = persona
        self.estado = estado

    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            if llave == "id" or llave == "valor_formula":
                continue
            d[f"Caja Premium {self.id} - {llave}"] = valor
        return d

    def calc_valor_reloj(self, reloj):
        self.rand = get_rand()
        self.valor = -0.06*log(1-self.rand)
        self.valor_reloj = self.valor + reloj

    def reset(self):
        super(LlegadaPremium, self).reset()
        self.persona = 0

class Persona:
    def __init__(self, id, estado, hora_llegada=0, hora_llegada_control=0):
        self.id = id
        self.estado = estado
        self.hora_llegada = hora_llegada
        self.hora_llegada_control = hora_llegada_control


    def to_dict(self):
        d = {}
        for llave, valor in self.__dict__.items():
            d[f"G {self.id} - {llave}"] = valor
        return d

