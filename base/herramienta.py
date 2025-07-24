import importlib
import pkgutil
import inspect

from abc import ABC, abstractmethod
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QPushButton

class Herramienta(ABC):
    def __init__(self, contexto):
        super().__init__()
        self.contexto = contexto

    @classmethod
    @abstractmethod
    def nombre_plugin(cls):
        pass

    @classmethod
    @abstractmethod
    def etiqueta_plugin(cls):
        pass
    
    @abstractmethod
    def run(self):
        pass

class CargadorPlugins(object):
    def __init__(self, paquete_plugins):
        self.paquete_plugins = paquete_plugins

    def iterar_sobre_namespace(self, namespace_pkg):
        return pkgutil.iter_modules(namespace_pkg.__path__, namespace_pkg.__name__ + ".")

    def get_nombre_modulo_clase(self, clase):
        return clase.__dict__['__module__'] if '__module__' in clase.__dict__.keys() and 'nombre_plugin' in clase.__dict__.keys() else None
        
    def get_clases(self, moduleInfo):
        rta = []
        nombre = moduleInfo.name
        modulo = importlib.import_module(nombre)

        submodulos = [moduleInfo for moduleInfo in self.iterar_sobre_namespace(modulo)]
        submodulos_importados = {
            nombre: importlib.import_module(nombre) for _, nombre, _ in submodulos
        }

        for clave, modulo in submodulos_importados.items():
            clases = inspect.getmembers(modulo, inspect.isclass)
            [rta.append(clase if clave == self.get_nombre_modulo_clase(clase[1]) else None) for clase in clases]
        
        return [clase for clase in rta if clase]

    def cargar_plugins(self):
        listados_clases = [self.get_clases(moduleInfo) for moduleInfo in self.iterar_sobre_namespace(self.paquete_plugins) if moduleInfo.ispkg]
        lista_plana = sum(listados_clases, [])
        rta = {
            nombre: clase for nombre, clase in lista_plana
        }
        return rta

class Popup(QDialog):
    def __init__(self, titulo, contenido, icono=None):
        super().__init__()
        
        self.setWindowTitle(titulo)

        layout = QVBoxLayout()
        for unComponente in contenido:
            layout.addWidget(unComponente)

        self.setLayout(layout)

        if icono:
            self.setWindowIcon(icono)

class BotoneraPopUp(QDialogButtonBox):
    def __init__(self, accionAceptar, accionCancelar):
        super().__init__()
        aceptar = QPushButton('Aceptar')
        aceptar.clicked.connect(accionAceptar)
        cancelar = QPushButton('Cancelar')
        cancelar.clicked.connect(accionCancelar)

        self.addButton(aceptar, QDialogButtonBox.AcceptRole)
        self.addButton(cancelar, QDialogButtonBox.RejectRole)
    