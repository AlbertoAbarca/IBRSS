import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, Counter
import random
import math


MAPA_ALCALDIAS = {
    "Alvaro Obregon" : 1,
    "Azcapotzalco" : 2,
    "Benito Juarez" : 3,
    "Coyoacan" : 4,
    "Cuajimalpa" : 5,
    "Cuauhtemoc" : 6,
    "Gustavo A. Madero" : 7,
    "Iztacalco" : 8,
    "Iztapalapa" : 9,
    "Magdalena Contreras" : 10,
    "Miguel Hidalgo" : 11,
    "Milpa Alta" : 12,
    "Tlahuac" : 13,
    "Tlalpan" : 14,
    "Venustiano Carranza" : 15,
    "Xochimilco" : 16
}


estaciones = [
    ("Pantitlan", 1, 1, 1, 15),
    ("Zaragoza", 1, 2, 2, 15),
    ("Gomez Farias", 1, 3, 3, 15),
    ("Puerto Aereo", 1, 4, 4, 15),
    ("Balbuena", 1, 5, 5, 15),
    ("Moctezuma", 1, 6, 6, 15),
    ("San Lazaro", 1, 7, 7, 15),
    ("Candelaria", 1, 8, 8, 15),
    ("Merced", 1, 9, 9, 15),
    ("Pino Suarez", 1, 10, 10, 6),
    ("I. Catolica", 1, 11, 11, 6),
    ("Salto Del Agua", 1, 12, 12, 6),
    ("Balderas", 1, 13, 13, 6),
    ("Cuauhtemoc", 1, 14, 14, 6),
    ("Insurgentes", 1, 15, 15, 6),
    ("Sevilla", 1, 16, 16, 6),
    ("Chapultepec", 1, 17, 17, 6),
    ("Juanacatlan", 1, 18, 18, 11),
    ("Tacubaya", 1, 19, 19, 11),
    ("Observatorio", 1, 20, 20, 1),
    ("Cuatro Caminos", 2, 1, 21, 0),
    ("Panteones", 2, 2, 22, 11),
    ("Tacuba", 2, 3, 23, 11),
    ("Cuitlahuac", 2, 4, 24, 11),
    ("Popotla", 2, 5, 25, 11),
    ("Colegio Militar", 2, 6, 26, 11),
    ("Normal", 2, 7, 27, 11),
    ("San Cosme", 2, 8, 28, 6),
    ("Revolucion", 2, 9, 29, 6),
    ("Hidalgo", 2, 10, 30, 6),
    ("Bellas Artes", 2, 11, 31, 6),
    ("Allende", 2, 12, 32, 6),
    ("Zocalo", 2, 13, 33, 6),
    ("Pino Suarez", 2, 14, 10, 6),
    ("San Antonio Abad", 2, 15, 34, 6),
    ("Chabacano", 2, 16, 35, 6),
    ("Viaducto", 2, 17, 36, 3),
    ("Xola", 2, 18, 37, 3),
    ("Villa de Cortes", 2, 19, 38, 3),
    ("Nativitas", 2, 20, 39, 3),
    ("Portales", 2, 21, 40, 3),
    ("Ermita", 2, 22, 41, 3),
    ("General Anaya", 2, 23, 42, 4),
    ("Tasquenna", 2, 24, 43, 4),
    ("Indios Verdes", 3, 1, 44, 7),
    ("Panteones", 3, 2, 45, 7),
    ("Potrero", 3, 3, 46, 7),
    ("La Raza", 3, 4, 47, 7),
    ("Tlatelolco", 3, 5, 48, 6),
    ("Guerrero", 3, 6, 49, 6),
    ("Hidalgo", 3, 7, 30, 6),
    ("Juarez", 3, 8, 50, 6),
    ("Salto Del Agua", 3, 9, 12, 6),
    ("Ninnos Heroes", 3, 10, 51, 6),
    ("Hospital General", 3, 11, 52, 6),
    ("Centro Medico", 3, 12, 53, 6),
    ("Etiopia", 3, 13, 54, 3),
    ("Eugenia", 3, 14, 55, 3),
    ("Division Del Norte", 3, 15, 56, 3),
    ("Zapata", 3, 16, 57, 3),
    ("Coyoacan", 3, 17, 58, 3),
    ("Viveros", 3, 18, 59, 1),
    ("Miguel Angel De Quevedo", 3, 19, 60, 4),
    ("Copilco", 3, 20, 61, 4),
    ("Universidad", 3, 21, 62, 4),
    ("Martin Carrera", 4, 1, 63, 7),
    ("Talisman", 4, 2, 64, 7),
    ("Bondojito", 4, 3, 65, 7),
    ("Consulado", 4, 4, 66, 7),
    ("Canal Del Norte", 4, 5, 67, 15),
    ("Morelos", 4, 6, 68, 15),
    ("Candelaria", 4, 7, 8, 15),
    ("Fray Servando", 4, 8, 70, 15),
    ("Jamaica", 4, 9, 71, 15),
    ("Santa Anita", 4, 10, 72, 8),
    ("Pantitlan", 5, 1, 1, 15),
    ("Hangares", 5, 2, 73, 15),
    ("Terminal Aerea", 5, 3, 74, 15),
    ("Oceania", 5, 4, 75, 15),
    ("Aragon", 5, 5, 76, 15),
    ("Eduardo Molina", 5, 6, 77, 7),
    ("Consulado", 5, 7, 78, 7),
    ("Valle Gomez", 5, 8, 79, 15),
    ("Misterios", 5, 9, 80, 7),
    ("La Raza", 5, 10, 81, 7),
    ("Autobuses Del Norte", 5, 11, 82, 7),
    ("Instituto Del Petroleo", 5, 12, 83, 7),
    ("Politecnico", 5, 13, 84, 7),
    ("El Rosario", 6, 1, 85, 2),
    ("Tezozomoc", 6, 2, 86, 2),
    ("Azcapotzalco", 6, 3, 87, 2),
    ("Arena CDMX", 6, 4, 88, 2),
    ("Norte 45", 6, 5, 89, 2),
    ("Vallejo", 6, 6, 90, 2),
    ("Instituto Del Petroleo", 6, 7, 91, 7),
    ("Lindavista", 6, 8, 92, 7),
    ("Deportivo 18 De Marzo", 6, 9, 93, 7),
    ("Basilica", 6, 10, 94, 7),
    ("Martin Carrera", 6, 11, 95, 7),
    ("El Rosario", 7, 1, 85, 2),
    ("Aquiles Serdan", 7, 2, 96, 2),
    ("Camarones", 7, 3, 97, 2),
    ("Refineria", 7, 4, 98, 2),
    ("Tacuba", 7, 5, 23, 11),
    ("San Joaquin", 7, 6, 99, 11),
    ("Polanco", 7, 7, 100, 11),
    ("Auditorio", 7, 8, 101, 11),
    ("Constituyentes", 7, 9, 102, 11),
    ("Tacubaya", 7, 10, 19, 11),
    ("Sn. Pedro De Los Pinos", 7, 11, 103, 3),
    ("Sn. Antonio", 7, 12, 104, 3),
    ("Mixcoac", 7, 13, 105, 3),
    ("Barranca Del Muerto", 7, 14, 106, 1),
    ("Garibaldi", 8, 1, 107, 6),
    ("Bellas Artes", 8, 2, 31, 6),
    ("San Juan De Letran", 8, 3, 107, 6),
    ("Salto Del Agua", 8, 4, 12, 6),
    ("Doctores", 8, 5, 108, 6),
    ("Obrera", 8, 6, 109, 6),
    ("Chabacano", 8, 7, 35, 6),
    ("La Viga", 8, 8, 110, 15),
    ("Santa Anita", 8, 9, 72, 8),
    ("Coyuya", 8, 10, 111, 8),
    ("Iztacalco", 8, 11, 112, 8),
    ("Apatlaco", 8, 12, 113, 9),
    ("Aculco", 8, 13, 114, 9),
    ("Escuadron 201", 8, 14, 115, 9),
    ("Atlalilco", 8, 15, 116, 9),
    ("Iztapalapa", 8, 16, 117, 9),
    ("C. De Estrella", 8, 17, 118, 9),
    ("UAM", 8, 18, 119, 9),
    ("Const. de 1917", 8, 19, 120, 9),
    ("Pantitlan", 9, 1, 1, 8),
    ("Puebla", 9, 2, 121, 8),
    ("Ciudad Deportivo", 9, 3, 122, 8),
    ("Velodromo", 9, 4, 123, 15),
    ("Mixiuhca", 9, 5, 124, 15),
    ("Jamaica", 9, 6, 7, 15),
    ("Chabacano", 9, 7, 35, 6),
    ("Lazaro Cardenas", 9, 8, 125, 6),
    ("Centro Medico", 9, 9, 126, 6),
    ("Chilpancingo", 9, 10, 127, 6),
    ("Patriotismo", 9, 11, 128, 6),
    ("Tacubaya", 9, 12, 19, 11),
    ("Pantitlan", 10, 1, 1, 0),
    ("Agricola Oriental", 10, 2, 129, 8),
    ("Canal De San Juan", 10, 3, 130, 8),
    ("Tepalcates", 10, 4, 131, 9),
    ("Guelatao", 10, 5, 132, 9),
    ("Pennon Viejo", 10, 6, 133, 9),
    ("Acatitla", 10, 7, 134, 9),
    ("Santa Marta", 10, 8, 135, 9),
    ("Los Reyes", 10, 9, 136, 0),
    ("La Paz", 10, 10, 137, 0),
    ("Mixcoac", 12, 1, 105, 0),
    ("Insurgentes Sur", 12, 2, 138, 3),
    ("Hospital 20 De Noviembre", 12, 3, 139, 3),
    ("Zapata", 12, 4, 140, 3),
    ("Parque De Los Venados", 12, 5, 141, 3),
    ("Eje Central", 12, 6, 142, 3),
    ("Ermita", 12, 7, 41, 3),
    ("Mexicaltzingo", 12, 8, 143, 9),
    ("Atlalilco", 12, 9, 144, 9),
    ("Culhuacan", 12, 10, 145, 9),
    ("San Andres Tomatlan", 12, 11, 146, 9),
    ("Lomas Estrella", 12, 12, 147, 9),
    ("Calle 11", 12, 13, 148, 0),
    ("Periferico Ote.", 12, 14, 149, 13),
    ("Tezonco", 12, 15, 150, 13),
    ("Olivos", 12, 16, 151, 13),
    ("Nopalera", 12, 17, 152, 13),
    ("Zapotitlan", 12, 18, 153, 13),
    ("Tlaltenco", 12, 19, 154, 13),
    ("Tlahuac", 12, 20, 155, 13),
    ("Ciudad Azteca", 13, 1, 156, 0),
    ("Plaza Aragon", 13, 2, 157, 0),
    ("Olimpica", 13, 3, 158, 0),
    ("Ecatepec", 13, 4, 159, 0),
    ("Muzquiz", 13, 5, 160, 0),
    ("Rio De Los Remedios", 13, 6, 161, 0),
    ("Impulsora", 13, 7, 162, 0),
    ("Nezahualcoyotl", 13, 8, 163, 0),
    ("Villa De Aragon", 13, 9, 164, 7),
    ("Bosque De Aragon", 13, 10, 165, 7),
    ("Deportivo Oceania", 13, 11, 166, 7),
    ("Oceania", 13, 12, 167, 7),
    ("Romero Rubio", 13, 13, 168, 15),
    ("Flores Magon", 13, 14, 169, 15),
    ("San Lazaro", 13, 15, 170, 15),
    ("Morelos", 13, 16, 68, 15),
    ("Tepito", 13, 17, 171, 6),
    ("Lagunilla", 13, 18, 172, 6),
    ("Garibaldi", 13, 19, 107, 6),
    ("Guerrero", 13, 20, 49, 6),
    ("Buenavista", 13, 21, 173, 6),
    ("Alvaro Obregon", 0, 0, 174, 1),
    ("Azcapotzalco", 0, 0, 175, 2),
    ("Benito Juarez", 0, 0, 176, 3),
    ("Coyoacan", 0, 0, 177, 4),
    ("Cuajimalpa", 0, 0, 178, 5),
    ("Cuauhtemoc", 0, 0, 179, 6),
    ("Gustavo A. Madero", 0, 0, 180, 7),
    ("Iztacalco", 0, 0, 181, 8),
    ("Iztapalapa", 0, 0, 182, 9),
    ("Magdalena Contreras", 0, 0, 183, 10),
    ("Miguel Hidalgo", 0, 0, 184, 11),
    ("Milpa Alta", 0, 0, 185, 12),
    ("Tlahuac", 0, 0, 186, 13),
    ("Tlalpan", 0, 0, 187, 14),
    ("Venustiano Carranza", 0, 0, 188, 15),
    ("Xochimilco", 0, 0, 189, 16)
]

    
# Agrupar estaciones por nombre normalizado
estaciones_por_nombre = defaultdict(list)
for nombre, linea, orden, id_global, id_alcaldia in estaciones:
    nombre_normalizado = nombre.strip().lower()
    estaciones_por_nombre[nombre_normalizado].append((linea, orden, id_global, id_alcaldia))

# Seleccionar estaciones únicas por ID más común
estaciones_representativas = {}
for nombre, registros in estaciones_por_nombre.items():
    ids_globales = [r[2] for r in registros]
    id_mas_comun = Counter(ids_globales).most_common(1)[0][0]
    for registro in registros:
        if registro[2] == id_mas_comun:
            estaciones_representativas[nombre] = registro
            break

# Mapeos clave para el grafo
id_a_nombre = {e[3]: e[0].title() for e in estaciones}
id_a_linea = {e[3]: e[1] for e in estaciones}
ids_estaciones = sorted(set(id_a_nombre.keys()) | set(id_a_linea.keys()))  

# --- Construcción del grafo ---

# Conexiones por adyacencia en misma línea
conexiones = set()
for i in range(len(estaciones)):
    for j in range(len(estaciones)):
        if i == j:
            continue
        _, linea1, orden1, id1, _ = estaciones[i]
        _, linea2, orden2, id2, _ = estaciones[j]
        if linea1 == linea2 and abs(orden1 - orden2) == 1:
            conexiones.add((min(id1, id2), max(id1, id2)))

# Conexiones por transbordo (misma estación)
estaciones_por_id = defaultdict(list)
for nombre, _, _, id_global, _ in estaciones:
    estaciones_por_id[id_global].append(nombre)

for id_estacion, nombres in estaciones_por_id.items():
    if len(nombres) > 1:  # Es punto de transbordo
        conexiones.add((id_estacion, id_estacion))

# Crear grafo de conexiones
grafo_metro = nx.Graph()
for id_estacion in ids_estaciones:
    grafo_metro.add_node(id_estacion, label=id_a_nombre.get(id_estacion, f"Estación {id_estacion}"))

for id1, id2 in conexiones:
    if id1 != id2:  # Ignorar self-loops
        grafo_metro.add_edge(id1, id2)

# --- Visualización ---
colores_lineas = {linea: i for i, linea in enumerate(sorted(set(id_a_linea.values())))}
colores_nodos = [colores_lineas.get(id_a_linea.get(n, 0), 0) for n in grafo_metro.nodes()]

plt.figure(figsize=(14, 10))
posicionamiento = nx.spring_layout(grafo_metro, seed=42)
nx.draw_networkx_nodes(grafo_metro, posicionamiento, node_size=700, node_color=colores_nodos, cmap=plt.cm.tab20)
nx.draw_networkx_edges(grafo_metro, posicionamiento, width=1.5, edge_color="gray")
nx.draw_networkx_labels(grafo_metro, posicionamiento, labels=id_a_nombre, font_size=9, font_weight="bold")
plt.title("Red del Metro CDMX", fontsize=16)
plt.axis("off")
plt.show()

# --- Preparación para optimización ---

# Mapeos para cobertura
id_a_alcaldia = {e[3]: e[4] for e in estaciones if e[4] != 0}
alcaldia_a_estaciones = defaultdict(list)
for e in estaciones:
    if e[4] != 0:  # Filtrar estaciones sin alcaldía
        alcaldia_a_estaciones[e[4]].append(e[3])

def calcular_cobertura(estado_binario):
    """Calcula qué alcaldías son cubiertas por las estaciones activas"""
    ids_estaciones = list(id_a_alcaldia.keys())
    estaciones_activas = [ids_estaciones[i] for i, activa in enumerate(estado_binario) if activa == '1']
    
    alcaldias_cubiertas = set()
    for id_estacion in estaciones_activas:
        # Estaciones dentro de 5 saltos
        alcances = nx.single_source_shortest_path_length(grafo_metro, id_estacion, cutoff=5)
        for id_vecino in alcances:
            if id_alcaldia := id_a_alcaldia.get(id_vecino):
                alcaldias_cubiertas.add(id_alcaldia)
    return alcaldias_cubiertas

def calcular_fitness(estado_binario):
    alcaldias_cubiertas = calcular_cobertura(estado_binario)
    alcaldias_no_cubiertas = len(MAPA_ALCALDIAS) - len(alcaldias_cubiertas)
    num_estaciones = estado_binario.count('1')
    return alcaldias_no_cubiertas + num_estaciones / 10  

def generar_vecino(estado_actual):
    """Genera un estado vecino cambiando una estación aleatoria"""
    i = random.randint(0, len(estado_actual) - 1)
    nuevo_estado = list(estado_actual)
    nuevo_estado[i] = '1' if estado_actual[i] == '0' else '0'
    return ''.join(nuevo_estado)

def optimizar_cobertura(iteraciones=20000, temp_inicial=50, tasa_enfriamiento=0.001):
    """Algoritmo de recocido simulado para optimizar cobertura"""
    ids_estaciones = list(id_a_alcaldia.keys())
    estado_actual = ''.join(random.choice('01') for _ in ids_estaciones)
    fitness_actual = calcular_fitness(estado_actual)
    temperatura = temp_inicial
    mejor_estado = estado_actual
    mejor_fitness = fitness_actual
    
    print(f"\nInicio - Fitness inicial: {fitness_actual:.2f}")
    print(f"Estaciones iniciales: {[id_a_nombre[ids_estaciones[i]] for i, activa in enumerate(estado_actual) if activa == '1']}")

    for iteracion in range(iteraciones):
        estado_vecino = generar_vecino(estado_actual)
        fitness_vecino = calcular_fitness(estado_vecino)
        delta = fitness_vecino - fitness_actual

        # Criterio de aceptación
        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            estado_actual = estado_vecino
            fitness_actual = fitness_vecino

        # Reporte periódico
        if iteracion % 1000 == 0:
            print(f"\nIter {iteracion}: Temp={temperatura:.4f} Fitness={fitness_actual:.4f}")

        # Actualizar mejor solución
        if fitness_actual < mejor_fitness:
            mejor_estado = estado_actual
            mejor_fitness = fitness_actual
            print(f"\n Nuevo óptimo (Iter {iteracion}):")
            print(f"Fitness: {mejor_fitness:.4f}")
            print(f"Estaciones: {[id_a_nombre[ids_estaciones[i]] for i, activa in enumerate(mejor_estado) if activa == '1']}")
            print(f"Cobertura: {calcular_cobertura(mejor_estado)}")

        # Enfriamiento
        temperatura *= (1 - tasa_enfriamiento)

    # Resultado final
    estaciones_optimas = [ids_estaciones[i] for i, activa in enumerate(mejor_estado) if activa == '1']
    print("\n--- Resultado Final ---")
    print(f"Mejor fitness: {mejor_fitness:.4f}")
    print(f"Estaciones seleccionadas ({len(estaciones_optimas)}):")
    for est_id in estaciones_optimas:
        print(f"- {id_a_nombre[est_id]} (Línea {id_a_linea[est_id]}, Alcaldía {id_a_alcaldia[est_id]})")
    print(f"Alcaldías cubiertas: {calcular_cobertura(mejor_estado)}")
    
    return estaciones_optimas, mejor_fitness

# Ejecutar optimización
estaciones_optimas, mejor_fitness = optimizar_cobertura()