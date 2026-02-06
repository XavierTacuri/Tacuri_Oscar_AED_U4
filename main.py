# Oscar Tacuri
import argparse
import math
import os
import platform
import random
import time
from typing import List, Tuple, Optional

#Utilidades y tiempos del sistema

def tiempo_Actutal() -> float:
    """
    Devuelve el tiempo actual en milisegundos usando perf_counter().
    """
    return time.perf_counter()*1000.0

def medir_Tiempo(metodo, *args,repeticiones:int=1,**kwargs )->Tuple[float,any]:
    """
    Ejecuta el metodo y mide cuánto tarda (en ms).
    - repeticiones: permite promediar para reducir ruido.
    Retorna: (tiempo_promedio_ms, resultado_de_la_funcion)
    """

    salida = None
    t0=tiempo_Actutal()
    for _ in range(repeticiones):
        salida=metodo(*args,**kwargs)
    t1=tiempo_Actutal()
    return (t1-t0)/repeticiones, salida

def informacion_Sistema()->str:
    """
    Devuelve información del computador y
    las características del ordenador en las que fue ejecutado.
    """
    return (
        f"Sistema Operativo: {platform.system()}{platform.release()}\n"
        f"Arquitectura: {platform.machine()}\n"
        f"Procesador: {platform.processor() or 'No disponible'}\n"
        f"Python: {platform.python_version()}\n"
    )

#Generar la Matriz Aleatoria

def generar_Matriz(n:int,minimo:int,maximo:int):
    """
    Genera una matriz n x n con valores aleatorios con los limites [minimo, maximo].
    """
    random.seed(123)
    return [[random.randint(minimo,maximo) for _ in range(n)] for _ in range(n)]

def aplanar_Arreglo(arreglo):
    """
    Convierte una matriz a un arreglo.
    """
    return [x for fila in arreglo for x in fila]

#Algoritmos de Busqueda
def buscar_Secuencial(arreglo,numero):
    """
    Recorre elemento por elemento hasta encontrar el objetivo.
    """
    for i, elmt in enumerate(arreglo):
        if elmt==numero:
            return i
    return -1

def buscar_Binaria(arreglo,numero):
    """
    Búsqueda binaria: requiere arreglo ORDENADO.
    En cada paso descarta la mitad del espacio de búsqueda.
    """
    izq,der = 0, len(arreglo)-1
    while izq <= der:
        medio = (izq+der)//2
        if arreglo[medio]==numero:
            return medio
        if arreglo[medio]<numero:
            izq=medio+1
        else:
            der=medio-1
    return -1

def buscar_Interpol(arreglo,numero):
    """
    Búsqueda por interpolación: requiere arreglo ORDENADO.
    En vez de ir al punto medio, ESTIMA la posición (pos) asumiendo distribución uniforme.
    """
    izq,der = 0, len(arreglo)-1
    while izq <= der and numero>= arreglo[izq] and numero<=arreglo[der] :   # La condición asegura que el objetivo esté dentro del rango actual

        if arreglo[der]==arreglo[izq]:       # Si todos los valores son iguales, se evita división por cero
            return izq if arreglo[izq]==numero else -1

        pos = izq+ int((der-izq)*             # Fórmula de interpolación para estimar la posición
                       (numero-arreglo[izq])/
                       (arreglo[der]-arreglo[izq]))

        if pos < izq or pos > der:
            return -1

        if arreglo[pos]==numero:
            return pos
        if arreglo[pos]<numero:
            izq = pos + 1
        else:
            der= pos - 1
    return -1

#Metodos de Ordenamientos

def buble_Sort(arreglo):
    """
    Bubble Sort: compara vecinos e intercambia.
    """
    lista=arreglo[:]   # Copia la lista para no modificar el original
    n=len(lista)
    for i in range(n):
        for j in range(0,n - i - 1):
            if lista[j]>lista[j+1]:
                lista[j],lista[j+1]=lista[j+1],lista[j]
    return lista

def insertion_Sort(arreglo):
    """
    Insertion Sort: inserta cada elemento en su posición correcta.
    """
    lista=arreglo[:]
    for i in range(1, len(lista)):
        clave = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > clave:    # Mueve elementos mayores a la derecha para insertar "clave"
            lista[j+1] = lista[j]
            j -= 1
        lista[j+1] = clave
    return lista

def merger_Sort(arreglo):
    """
    Merge Sort (Divide y vencerás):
    1) Divide el arreglo en dos mitades
    2) Ordena recursivamente cada mitad
    3) Fusiona las mitades ordenadas
    """
    if len(arreglo)<=1:
        return arreglo[:]
    medio = len(arreglo)//2
    izq = merger_Sort(arreglo[:medio])
    der = merger_Sort(arreglo[medio:])
    return merge(izq,der)

def merge(izq,der):
    """
    Fusiona dos listas ya ordenadas (izq y der) en una sola lista ordenada.
    """
    result = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            result.append(izq[i])
            i += 1
        else:
            result.append(der[j])
            j += 1
    result.extend(izq[i:])
    result.extend(der[j:])
    return result

def shell_Sort(arreglo):
    """
    Shell Sort:
    - Generaliza insertion sort usando saltos(gaps) para mover elementos lejos.
    - Su complejidad depende de la secuencia de saltos (gaps).
    """
    lista=arreglo[:]
    n = len(lista)
    gap = n//2
    while gap > 0:
        for i in range (gap, n):
            temp = lista[i]
            j = i
            while j >= gap and lista[j-gap] > temp:
                lista[j] = lista[j-gap]
                j -= gap
            lista[j] = temp
            gap //= 2
    return lista

def counting_Sort(arreglo, min, max):
    """
    Counting Sort:
    - Cuenta cuántas veces aparece cada valor.
    - Requiere que el rango [minimo, maximo] sea manejable.
    """
    k = max - min + 1
    conteo = [0] * k
    for x in arreglo:                # Conteo de frecuencias
        conteo [x - min] += 1        # Se ajusta por minimo para manejar negativos
    salida = []                      # Reconstrucción ordenada
    for i, c in enumerate(conteo):
        salida.extend([i + min]* c)
    return salida

def radix_Sort(arreglo):
    """
    Radix Sort (no comparativo):
    - Se separan negativos y positivos,
     se ordenan por su valor absoluto y se reconstruye.
    """
    # Separamos negativos (guardando el valor absoluto) y positivos
    negativos = [-x for x in arreglo if x < 0]
    positivos = [x for x in arreglo if x >=0]

    # Ordenamos cada parte
    negativos = radix_SortOr(negativos)
    positivos = radix_SortOr(positivos)

    # Reconstruimos: los negativos deben ir antes, en orden correcto
    negativos = [-x for x in reversed(negativos)]
    return negativos + positivos

def radix_SortOr(arreglo):
    """
    Ordena cada parte que recibe y devuelve el arreglo ya ordenado
    """
    if not arreglo:
        return []        # Si el arreglo está vacío, retorna lista vacía
    lista = arreglo[:]
    exp = 1             # exp representa el dígito actual:
                        # 1 = unidades, 10 = decenas, 100 = centenas...
    maximo = max(arreglo)
    while maximo // exp > 0:
        lista = contar_digito(lista,exp)       # Se ordena el arreglo según el dígito actual
        exp *= 10                              # Se avanza al siguiente dígito (multiplicando por 10)
    return lista

def contar_digito(arreglo,exp):
    salida = [0]*len(arreglo)                   # Lista auxiliar donde se guardará el resultado ordenado
    cont = [0]*10                               # Arreglo de conteo para los dígitos 0..9
    for x in arreglo:
        cont[(x//exp)%10]+=1                     # (x // exp) % 10 obtiene el dígito actual
    for i in range(1,10):
        cont[i]+=cont[i-1]
    for i in range(len(arreglo)-1,-1,-1):       # Se recorre de derecha a izquierda para mantener estabilidad
        x = arreglo[i]
        d = (x//exp)%10
        cont[d]-=1
        salida[cont[d]]=x
    return salida

#Problema Planteado

#Solucion no optimizada
def contar_Pares(arreglo, x:int)->int:
    pares = 0                                   #Contador de pares encontrados
    n = len(arreglo)                            #Contador de pares encontrados
    for i in range(n):                          #Bucles que recorre las filas
        for j in range(i+1,n):                  #Bucle que recorre las columanas
            if (arreglo[i]==x and arreglo[j]== -x) or (arreglo[i]== -x and arreglo[j]== x): # Verifica si se cumple (x, -x) o (-x, x)
                pares += 1
    return pares
#Solucion Optimizada
def contar_ParesOp(arreglo, x: int)->int:

    frecuencia = {}                             # Diccionario para almacenar conteos
    for i in arreglo:                           # Recorre el arreglo una sola vez
        frecuencia[i] = frecuencia.get(i,0) + 1 # get(valor,0) evita errores si la clave no existe

    return frecuencia.get(x,0)*frecuencia.get(-x,0)  # Calcula el total de pares complementarios




#Principal
def main():
    print("===Informacion del Sistema===")
    print(informacion_Sistema())

    print("Generando Matriz....")
    matriz = generar_Matriz(1000,-1000,1000)

    arreglo = aplanar_Arreglo(matriz)
    arreglo_Ord = sorted(arreglo)
    numero_buscar = int(input("Ingrese el número que desea buscar: "))
    print("Metodos de Buscaqueda....\n")
    tiempo,idx = medir_Tiempo(buscar_Secuencial,arreglo_Ord,numero_buscar)
    print(f"Búsqueda Secuencial: {' - Encontrado Posicion ' + str(idx) if idx != -1 else 'No encontrado'} | Tiempo  {tiempo:.3f} ms\n")

    tiempo,idx1 = medir_Tiempo(buscar_Binaria,arreglo_Ord,numero_buscar)
    print(f"Búsqueda Binaria: {' - Encontrado Posicion ' + str(idx1) if idx1 != -1 else 'No encontrado'} | Tiempo  {tiempo:.3f} ms\n")

    tiempo,idx2 = medir_Tiempo(buscar_Interpol,arreglo_Ord,numero_buscar)
    print(f"Búsqueda Interpolacion: {' - Encontrado Posicion ' + str(idx2) if idx2 != -1 else 'No encontrado'} | Tiempo  {tiempo:.3f} ms\n")


    print("Metodos de Ordenamiento.....\n")
    muestra = arreglo[:4000]

    tiempo,_ = medir_Tiempo(buble_Sort,muestra)
    print(f"Ordenamiento Bubble Sort: Tiempo {tiempo:.3f} ms")

    tiempo,_ =medir_Tiempo(insertion_Sort,muestra)
    print(f"Ordenamiento Insertion Sort: Tiempo {tiempo:.3f} ms")

    tiempo,_ = medir_Tiempo(merger_Sort,muestra)
    print(f"Ordenamiento Merger Sort: Tiempo {tiempo:.3f} ms")

    tiempo,_ = medir_Tiempo(shell_Sort,muestra)
    print(f"Ordenamiento Shell Sort: Tiempo {tiempo:.3f} ms")

    tiempo,_ = medir_Tiempo(counting_Sort,muestra,-1000,1000)
    print(f"Ordenamiento Counting Sort: Tiempo {tiempo:.3f} ms")

    tiempo,_ = medir_Tiempo(radix_Sort,muestra)
    print(f"Ordenamiento Radix Sort: Tiempo {tiempo:.3f} ms\n")

    print("===Problema Planteado===\n")
    nParBu = int(input("Ingrese el número que desea buscar: "))

    print("===Resultados===")
    tiempo,resuGene = medir_Tiempo(contar_Pares,muestra,nParBu)
    print(f"Solucion No Optimizada (muestra {len(muestra)}): pares = {resuGene}, tiempo= {tiempo:.3f} ms")

    tiempo,resuGeneOp = medir_Tiempo(contar_ParesOp,muestra,nParBu)
    print(f"Solucion Optimizada (muestra {len(muestra)}): pares = {resuGeneOp}, tiempo= {tiempo:.3f} ms")




if __name__ == '__main__':
    main()

#Oscar Tacuri - Algoritmos y Estructura de Datos
#Uniad 4
