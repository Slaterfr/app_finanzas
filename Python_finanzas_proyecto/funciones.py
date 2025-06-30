import pickle
from abc import ABC, abstractmethod


class Transaccion(ABC):
    @abstractmethod
    def ingresar_datos(self, categoria, monto):
        pass

    @abstractmethod
    def calcular_balance(self):
        pass


class Ingreso(Transaccion):
    def __init__(self):
        self.datos = {}

    def ingresar_datos(self, categoria, monto):
        self.datos[categoria] = self.datos.get(categoria, 0) + monto

    def calcular_balance(self):
        return sum(self.datos.values())
    
    def modificar_datos(self, categoria, monto):
        if categoria in self.datos:
            self.datos[categoria] = monto
        else:
            raise ValueError("Ese ingreso no existe.")


class Gasto(Transaccion):
    def __init__(self):
        self.datos = {}

    def ingresar_datos(self, categoria, monto):
        self.datos[categoria] = self.datos.get(categoria, 0) + monto

    def calcular_balance(self):
        return -sum(self.datos.values())
    def modificar_datos(self, categoria, monto):
        if categoria in self.datos:
            self.datos[categoria] = monto
        else:
            raise ValueError("Ese gasto no existe.")


def guardar_datos_pickle(ingresos, gastos, archivo="datos.pkl"):
    with open(archivo, "wb") as archivo:
        pickle.dump({"ingresos": ingresos.datos, "gastos": gastos.datos}, archivo)


def cargar_datos_pickle(archivo="datos.pkl"):
    try:
        with open(archivo, "rb") as archivo:
            return pickle.load(archivo)
    except FileNotFoundError:
        return {"ingresos": {}, "gastos": {}}
















