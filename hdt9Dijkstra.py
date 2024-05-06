import heapq

class Grafo:
    def __init__(self):
        self.vertices = {}

    def agregar_ruta(self, origen, destino, costo):
        if origen not in self.vertices:
            self.vertices[origen] = {}
        if destino not in self.vertices:
            self.vertices[destino] = {}
        self.vertices[origen][destino] = costo
        self.vertices[destino][origen] = costo  # Las rutas son simétricas

def leer_archivo(nombre_archivo):
    grafo = Grafo()
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            origen, destino, costo = linea.strip().split(', ')
            costo = int(costo)
            grafo.agregar_ruta(origen, destino, costo)
    return grafo

def dijkstra(grafo, inicio):
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

if __name__ == "__main__":
    main()