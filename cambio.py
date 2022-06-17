import networkx as nx
import matplotlib.pyplot as plt

def main():
    archivo = open("cambio.in", "rt")
    linea1 = archivo.readline().split()
    cantidadEsquinas = int(linea1[0])
    origenColectivo = int(linea1[1])
    destinoEscuela = int(linea1[2])

    cantidadCalles = int(archivo.readline())

    calles = []
    for x in archivo:
        calles.append(tuple(int(i) for i in x.split()))
    archivo.close()
    oCambioCallesMano = CambioCallesMano(calles, origenColectivo, destinoEscuela)

class CambioCallesMano:
    def __init__(self, calles, origenColectivo, destinoEscuela):
        self.calles=calles
        self.origenColectivo=origenColectivo
        self.destinoEscuela=destinoEscuela
        self.barrio = nx.Graph()
        self.barrio.add_weighted_edges_from(calles)

        self.barrioOriginal = nx.DiGraph()
        self.barrioOriginal.add_weighted_edges_from(calles)

        self.distancias, caminos = nx.single_source_dijkstra(barrio, origenColectivo)
        self.camino = caminos[destinoEscuela]
        self.distancia = distancias[destinoEscuela]
        encontrarCallesACambiar()

    def encontrarCallesACambiar():
        callesACambiar = []
        for i in range(len(self.camino)-1):
            actual = self.camino[i]
            siguiente = self.camino[i+1]
            adyacentes = nx.neighbors(self.barrioOriginal, actual)
            if siguiente not in adyacentes:
                for i in range(len(self.calles)):
                    if calles[i][0] == siguiente and self.calles[i][1] == actual:
                        callesACambiar.append(i+1)
                        continue

        callesACambiar.sort()
        imprimirArchivo()
    def imprimirArchivo():        
        archivo = open("cambio.out", "wt")
        archivo.write(str(distancia) + "\n")
        archivo.write("".join(str(i) + " " for i in callesACambiar))
        archivo.close()


# mostrar grafo
""" pos = nx.spring_layout(barrio)
nx.draw(barrio, pos, with_labels=True)

plt.show()"""
