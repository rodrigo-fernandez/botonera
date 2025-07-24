from datetime import date
from base.herramienta import Herramienta


class GetHoy(Herramienta):
    def getHoy(self, format):
        #return date.today().strftime(str(format))
        return date.today().strftime("%Y%m%d")
    
    @classmethod
    def nombre_plugin(cls):
        return 'GetHoy'
    
    @classmethod
    def etiqueta_plugin(cls):
        return 'Hoy'
    
    def run(self):
        formato = self.contexto['formato_fecha'] if 'formato_fecha' in self.contexto and self.contexto['formato_fecha'] else "%Y%m%d"
        hoy = self.getHoy(formato)
        
        if 'barraEstado' in self.contexto and self.contexto['barraEstado']:
            self.contexto['barraEstado'].setText(hoy)
