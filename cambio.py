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

        distancias, caminos = nx.single_source_dijkstra(self.barrio, origenColectivo)
        self.camino = caminos[destinoEscuela]
        self.distancia = distancias[destinoEscuela]
        self.encontrarCallesACambiar()
        self.imprimirArchivo()
        self.mostrarBarrio()

    def encontrarCallesACambiar(self):
        self.callesACambiar = []
        for i in range(len(self.camino)-1):
            actual = self.camino[i]
            siguiente = self.camino[i+1]
            adyacentes = nx.neighbors(self.barrioOriginal, actual)
            if siguiente not in adyacentes:
                for i in range(len(self.calles)):
                    if self.calles[i][0] == siguiente and self.calles[i][1] == actual:
                        self.callesACambiar.append(i+1)
                        continue

        self.callesACambiar.sort()

    def imprimirArchivo(self):        
        archivo = open("cambio.out", "wt")
        archivo.write(str(self.distancia) + "\n")
        archivo.write("".join(str(i) + " " for i in self.callesACambiar))
        archivo.close()

    def mostrarBarrio(self):
        pos = nx.spring_layout(self.barrio)
        nx.draw(self.barrio, pos, with_labels=True)

        plt.show()

main()
