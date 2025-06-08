import json
import regex as re

#estructuras para guardar el número de creditos cursados por año primero optativas, basicas, obligatorias y tfg
desglose_primero = [0, 0, 0, 0]
desglose_segundo = [0, 0, 0, 0]
desglose_tercero = [0, 0, 0, 0]
desglose_cuarto = [0, 0, 0, 0]

#expresión regularar que obtiene del fichero fuente de asignaturas cursadas las líneas y las divide en grupo asignatura y casilla
pattern_cursado = r"(?P<asignatura>([a-zA-ZÁÉÍÓÚáéíóú]+ )*[a-zA-ZÁÉÍÓÚáéíóú]+) (?P<casilla>\[(|X)\])"
compile_cursado = re.compile(pattern_cursado)

#función para obtener los datos del plan antiguo
def obtener_plan_antiguo(fichero):
    with open(fichero, "r") as file: 
        return json.load(file)

#función para obtener las asignaturas cursadas del fichero
def obtener_mis_asignaturas(fichero):
    with open(fichero, "r") as file: 
        return file.readlines()

#recorro el plan de estudios y guardo el desglose de creditos de cada curso en una estructura de datos
def clasificar_creditos(plan_antiguo):
    lista = []
    for dict in plan_antiguo:
        if "curso" in dict:
            if(dict["curso"] == 1 or dict["curso"] == 2 or dict["curso"] == 3 or dict["curso"] == 4):
                lista.append(dict)

    return lista

def casilla_marcada(casilla):
    isMarcada = False
    if (casilla[1] == 'X'):
        isMarcada = True

    return isMarcada

def creditos_totales():
    total = 0
    
    for i in range(0, 4):
        total = total + desglose_primero[i] + desglose_segundo[i] + desglose_tercero[i] + desglose_cuarto[i]

    return total


def mis_creditos(mis_asignaturas, plan_antiguo):
    for linea in mis_asignaturas:
        if match := compile_cursado.match(linea):
            asignatura = match.group("asignatura")
            casilla = match.group("casilla")

            if(casilla_marcada(casilla)):
                for actual in plan_antiguo:
                    if "asignatura" in actual:
                        if(asignatura == actual["asignatura"] and (actual["cuatrimestre"] == 1 or actual["cuatrimestre"] == 2)):
                            desglose_primero[actual["tipo"]] += actual["creditos"]

                        elif(asignatura == actual["asignatura"]and (actual["cuatrimestre"] == 3 or actual["cuatrimestre"] == 4)):
                            desglose_segundo[actual["tipo"]] += actual["creditos"]

                        elif(asignatura == actual["asignatura"] and (actual["cuatrimestre"] == 5 or actual["cuatrimestre"] == 6)):
                            desglose_tercero[actual["tipo"]] += actual["creditos"]

                        elif(asignatura == actual["asignatura"] and (actual["cuatrimestre"] == 7 or actual["cuatrimestre"] == 8)):
                            desglose_cuarto[actual["tipo"]] += actual["creditos"]
    
    return creditos_totales()

def comprobar_creditos_curso(curso, mi_curso):
    sinFallos = True

    if(curso["optativo"] < mi_curso[0] or curso["basico"] < mi_curso[1] or curso["obligatorio"] < mi_curso[2] or curso["tfg"] < mi_curso[3]):
        sinFallos = False

    return sinFallos

def comprobar_creditos(clasificacion, primero, segundo, tercero, cuarto):
    sinFallos = True

    if(not comprobar_creditos_curso(clasificacion[0], primero) or not comprobar_creditos_curso(clasificacion[1], segundo) or not comprobar_creditos_curso(clasificacion[2], tercero) or not comprobar_creditos_curso(clasificacion[3], cuarto)):
        sinFallos = False

    return sinFallos


plan_antiguo = obtener_plan_antiguo("plan-antiguo.json") #aquí se almacenará todo el json del plan antiguo
mis_asignaturas = obtener_mis_asignaturas("mis_asignaturas.txt") #guardamos la información de nuestras asignaturas cursadas
clasificacion_antiguos = clasificar_creditos(plan_antiguo)

total = mis_creditos(mis_asignaturas, plan_antiguo)

if(comprobar_creditos(clasificacion_antiguos, desglose_primero, desglose_segundo, desglose_tercero, desglose_cuarto)): 
    porcentaje = total/240 * 100
    print(f"Enhorabuena, tus créditos totales en el plan actual son: {total}. Esto supone el {porcentaje}% de créditos superados.")

else: 
    print("ERROR EN LA ELECCIÓN DE ASIGNATURAS")

