import networkx as nx
import matplotlib.pyplot as plt

from bokeh.io import output_file, show
from bokeh.models import WheelZoomTool, HoverTool, ResetTool, SaveTool
from bokeh.models import Circle, MultiLine, Plot, Range1d, NodesAndLinkedEdges, MultiLine
from bokeh.models import Legend, LegendItem
from bokeh.palettes import Spectral10
from bokeh.plotting import from_networkx

# Colores
color = {}
color['nodoDefault'] = Spectral10[0]
color['nodoOrigen'] = Spectral10[2]
color['nodoDestino'] = Spectral10[8]
color['aristaDefault'] = '#CCCCCC'
color['aristaCamino'] = Spectral10[1]
color['aristaCambio'] = Spectral10[7]

# Lectura de archivo .in *****************************************
nombreArchivo = "caso_01_pruebaDeClase.in"
#nombreArchivo = "caso_02_salida_sinCamino.in"
#nombreArchivo = "caso_03_salida_TodasCallesCambianSentido.in"
#nombreArchivo = "caso_04_salida_faltaDato.in"
#nombreArchivo = "caso_05_mismoOrigenMismoDestino.in"
#nombreArchivo = "caso_06_salida_noHayCambios.in"
archivo = open(nombreArchivo, "rt")
linea1 = archivo.readline().split()
cantidadEsquinas = int(linea1[0])
origenColectivo = int(linea1[1])
destinoEscuela = int(linea1[2])
cantidadCalles = int(archivo.readline())
calles = []
for x in archivo:
    calles.append(tuple(int(i) for i in x.split()))
archivo.close()


# Creación de Grafos (Dirigido y no dirigido) ********************
barrioOriginal = nx.DiGraph()
barrioOriginal.add_weighted_edges_from(calles)

barrio = nx.Graph()


# Aristas y Nodos con atributos **********************************
numCalle = 1
for c in calles:
    barrio.add_edge(c[0], c[1], weight=c[2], calle=numCalle)
    numCalle += 1

nx.set_node_attributes(barrio, color['nodoDefault'], name='color')
nx.set_edge_attributes(barrio, color['aristaDefault'], name='color')


# Búsqueda del camino más corto ***********************************
camino = []
try:
    barrio.nodes[origenColectivo]['color'] = color['nodoOrigen']
    barrio.nodes[destinoEscuela]['color'] = color['nodoDestino']
    distancias, caminos = nx.single_source_dijkstra(barrio, origenColectivo)
    camino = caminos[destinoEscuela]
    distancia = distancias[destinoEscuela]

    # Búsqueda de calles a cambiar ********************************
    callesACambiar = []
    for i in range(len(camino)-1):
        actual = camino[i]
        siguiente = camino[i+1]
        arista = (actual, siguiente)
        if arista in barrioOriginal.edges:
            barrio.edges[arista]['color'] = color['aristaCamino']
        else:
            callesACambiar.append(barrio.edges[arista]['calle'])
            barrio.edges[arista]['color'] = color['aristaCambio']

    callesACambiar.sort()
except:
    print("No se pudo encontrar un camino")


# Escribir .out ***************************************************
archivo = open("cambio.out", "wt")
if len(camino) == 0:
    archivo.write("NO HAY CAMINO")
else:
    archivo.write(str(distancia) + "\n")
    archivo.write("".join(str(i) + " " for i in callesACambiar))
archivo.close()


# Mostrar Grafo con Bokeh ******************************************
plot = Plot(width=600, height=600, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
plot.title.text = "Cambio de manos de calles"

node_hover_tool = HoverTool(tooltips=[("Esquina", "@index")])
plot.add_tools(node_hover_tool, WheelZoomTool(), ResetTool(), SaveTool())

graph_renderer = from_networkx(barrio, nx.spring_layout, scale=1, center=(0, 0))
graph_renderer.node_renderer.glyph = Circle(size=25, fill_color="color")
graph_renderer.edge_renderer.glyph = MultiLine(line_color="color", line_alpha=0.8, line_width=5)
graph_renderer.selection_policy = NodesAndLinkedEdges()
plot.renderers.append(graph_renderer)

leyenda = Legend(items=[LegendItem(label="Esquina", renderers=[graph_renderer.node_renderer]),
                 LegendItem(label="Calle", renderers=[graph_renderer.edge_renderer])])
plot.add_layout(leyenda)

output_file("grafo_interactivo.html")
show(plot)
