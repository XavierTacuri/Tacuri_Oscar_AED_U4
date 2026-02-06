# Tarea Unidad 4 – Teoría de la Complejidad

## Descripción del Proyecto

Este proyecto implementa múltiples algoritmos de búsqueda y ordenamiento con el objetivo de analizar su comportamiento según la teoría de la complejidad algorítmica.

Se trabaja sobre una matriz de números enteros generada aleatoriamente de tamaño:

1000 x 1000  → 1,000,000 datos

El programa mide tiempos reales de ejecución y compara soluciones genéricas vs optimizadas.

---

##  Algoritmos de Búsqueda

| Algoritmo | Complejidad | Descripción |
|---|---|---|
| Secuencial | O(n) | Recorre elemento por elemento |
| Binaria | O(log n) | Divide el arreglo ordenado |
| Interpolación | O(log log n) | Estima posición matemática |

---

## Algoritmos de Ordenamiento

| Algoritmo | Complejidad | Tipo |
|---|---|---|
| Bubble Sort | O(n²) | Comparativo |
| Insertion Sort | O(n²) | Comparativo |
| Merge Sort | O(n log n) | Divide y vencerás |
| Shell Sort | ~O(n log n) | Incremental |
| Counting Sort | O(n+k) | No comparativo |
| Radix Sort | O(d(n+k)) | No comparativo |

---

## Problema Planteado

Se implementó el conteo de pares complementarios:

(x, -x)

### Solución No Optimizada
- Dos ciclos anidados  
- Complejidad: O(n²)

### Solución Optimizada
- Diccionario de frecuencias  
- Complejidad: O(n)

Esto demuestra cómo el uso de estructuras hash reduce significativamente el tiempo de ejecución.

---

##  Cómo Ejecutar

Desde PyCharm o terminal:

```bash
python main.py
```

El programa solicitará:
```
Ingrese el número que desea buscar:
```
---

## 📈 Ejemplo de Salida

```
Búsqueda Secuencial:  Encontrado Posición 382356 | Tiempo: 87.148 ms
Búsqueda Binaria: Encontrado Posición 382811 | Tiempo 0.020 ms
Búsqueda Interpolación:  Encontrado Posición 382498 | Tiempo 0.005 ms
```

---

## Información del Sistema

El programa muestra automáticamente:

- Sistema Operativo
- Arquitectura
- Procesador
- Versión de Python

---

##  Objetivo Académico

Comprender cómo la complejidad algorítmica afecta el rendimiento del software y cómo elegir estructuras de datos adecuadas mejora la eficiencia computacional.

---

##  Autor

Oscar Xavier Tacuri  
***Estudiante de Ingeniería de Software***