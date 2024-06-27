import enum

class ElementType(enum.Enum):
    AIR = 'Air'
    WATER = 'Water'

    def getValue(self):
        return self.value
    
    @staticmethod
    def list():
        lista = []
        for i in ElementType:
            lista.append({"key":i.name, "value": i.value})
        return lista

    def __json__(self):
        return self.value