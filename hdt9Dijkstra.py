import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self):
        self.vertices = {}

    def agregar_ruta(self, origen, destino, costo):
        # Para agregar una nueva ruta al grafo entre dos estaciones con el respectivo costo
        if origen not in self.vertices:
            self.vertices[origen] = {}
        if destino not in self.vertices:
            self.vertices[destino] = {}
        self.vertices[origen][destino] = costo
        self.vertices[destino][origen] = costo

def leer_archivo(nombre_archivo):
    # Para leer el archivo que contiene las rutas y costos
    grafo = Grafo()
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            origen, destino, costo = linea.strip().split(', ')
            costo = int(costo)
            grafo.agregar_ruta(origen, destino, costo)
    return grafo

def dijkstra(grafo, inicio):
    # Para implementar el algoritmo de Dijkstra para encontrar las rutas más baratas desde una estación de salida
    distancia = {nodo: float('inf') for nodo in grafo.vertices}
    distancia[inicio] = 0
    cola = [(0, inicio)]
    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)
        if distancia_actual > distancia[nodo_actual]:
            continue
        for vecino, peso in grafo.vertices[nodo_actual].items():
            distancia_total = distancia_actual + peso
            if distancia_total < distancia[vecino]:
                distancia[vecino] = distancia_total
                heapq.heappush(cola, (distancia_total, vecino))
    return distancia

def crear_grafo_networkx(grafo):
    # Para crear el grafo de NetworkX que representa las rutas del grafo proporcionado.
    G = nx.Graph()
    for origen, destinos in grafo.vertices.items():
        for destino, costo in destinos.items():
            G.add_edge(origen, destino, weight=costo)
    return G

def mostrar_mapa(grafo_networkx):
    # Para mostrar el mapa visual de las rutas en el grafo NetworkX utilizando matplotlib.
    pos = nx.spring_layout(grafo_networkx)  # Layout para posicionar los nodos
    nx.draw(grafo_networkx, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')
    labels = nx.get_edge_attributes(grafo_networkx, 'weight')
    nx.draw_networkx_edge_labels(grafo_networkx, pos, edge_labels=labels)
    plt.title("Mapa de posibles destinos")
    plt.show()

def main():
    archivo_rutas = "rutas.txt"
    grafo = leer_archivo(archivo_rutas)

    estacion_salida = input("Ingrese la estación de salida: ")

    if estacion_salida not in grafo.vertices:
        print("La estación de salida ingresada no existe en el sistema de buses.")
        return

    distancias = dijkstra(grafo, estacion_salida)
    print("Destinos posibles y costos desde", estacion_salida)
    for destino, costo in distancias.items():
        print(f"Destino: {destino}, Costo: {costo}")

    grafo_networkx = crear_grafo_networkx(grafo)
    mostrar_mapa(grafo_networkx)

if __name__ == "__main__":
    main()