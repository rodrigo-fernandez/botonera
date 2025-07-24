#! python312
import configparser
import argparse
import sys
import os
from base.herramienta import CargadorPlugins
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

import plugins


class VentanaPrincipal(QWidget):
    def __init__(self, configuracion, clases):
        super().__init__()
        self.DATA_ROL_ITEM_PLUGIN = 257

        self.setWindowTitle('Botonera')
        self.resize(200, 400)

        estado = QLineEdit()

        menu = QListWidget()
        menu.itemClicked.connect(self.itemElegido)

        for indice, nombrePlugin in enumerate(clases.keys()):
            
            plugin = self.initPlugin(configuracion, estado, nombrePlugin, clases[nombrePlugin])
            
            item = QListWidgetItem(plugin.etiqueta_plugin())
            item.setTextAlignment(Qt.AlignCenter)
            item.setData(self.DATA_ROL_ITEM_PLUGIN, plugin)
            menu.addItem(item)

        layout = QVBoxLayout()
        layout.addWidget(menu)
        
        layout.addWidget(estado)

        self.setLayout(layout)
        
        self.setWindowIcon(self.getIcono())

        self.show()
    
    def getIcono(self):
        icono = QIcon(os.path.dirname(__file__) + "/config/iconos/navaja_suiza.svg")
        return icono
    
    def itemElegido(self, item):
        item.data(self.DATA_ROL_ITEM_PLUGIN).run()
    
    def initPlugin(self, configuracion, estado, nombrePlugin, pluginClass):
        contexto = {}
        if nombrePlugin in configuracion:
            contexto = {
                clave : (configuracion[nombrePlugin][clave]) for clave in configuracion[nombrePlugin]
            }
        contexto['barraEstado'] = estado
        rta = pluginClass(contexto)
        return rta


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Botonera de funciones")
    parser.add_argument("--config", default=os.path.dirname(__file__) + "/config/.botonera")
    args = parser.parse_args()
    
    configuracion = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    configuracion.read(args.config)
        
    clases = CargadorPlugins(plugins).cargar_plugins()
    #print(clases)
    
    app = QApplication(sys.argv)

    w = VentanaPrincipal(configuracion, clases)

    app.exec()
