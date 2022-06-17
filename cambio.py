import networkx as nx
import matplotlib.pyplot as plt

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

barrio = nx.Graph()
barrio.add_weighted_edges_from(calles)

barrioOriginal = nx.DiGraph()
barrioOriginal.add_weighted_edges_from(calles)

distancias, caminos = nx.single_source_dijkstra(barrio, origenColectivo)
camino = caminos[destinoEscuela]
distancia = distancias[destinoEscuela]

callesACambiar = []
for i in range(len(camino)-1):
    actual = camino[i]
    siguiente = camino[i+1]
    adyacentes = nx.neighbors(barrioOriginal, actual)
    if siguiente not in adyacentes:
        for i in range(len(calles)):
            if calles[i][0] == siguiente and calles[i][1] == actual:
                callesACambiar.append(i+1)
                continue

callesACambiar.sort()

archivo = open("cambio.out", "wt")
archivo.write(str(distancia) + "\n")
archivo.write("".join(str(i) + " " for i in callesACambiar))
archivo.close()


# mostrar grafo
""" pos = nx.spring_layout(barrio)
nx.draw(barrio, pos, with_labels=True)

plt.show() """
