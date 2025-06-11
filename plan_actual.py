import json
import regex as re

#estructura con clave valor para saber el tipo de créditos y el tipo de mención
tipo_credito = {0:"optativo", 1:"básico", 2:"obligatorio", 3:"TFG"}
tipo_mencion = {0:"Software", 1:"Computación", 2:"Computadores", 3:"Tecnologías de la información", 4:"NINGUNA porque no hay créditos de mención", 5:"NINGUNA ya que hay varias menciones con la misma cantidad de créditos"}

#estructuras para guardar el número de creditos cursados por año primero optativas, basicas, obligatorias y tfg
mis_creditos_primero = [0, 0, 0, 0]
mis_creditos_segundo = [0, 0, 0, 0]
mis_creditos_tercero = [0, 0, 0, 0]
mis_creditos_cuarto_software = [0, 0, 0, 0]
mis_creditos_cuarto_computacion = [0, 0, 0, 0]
mis_creditos_cuarto_computadores = [0, 0, 0, 0]
mis_creditos_cuarto_redes = [0, 0, 0, 0]

#expresión regularar que obtiene del fichero fuente de asignaturas cursadas las líneas y las divide en grupo asignatura y casilla
regex_linea_mis_asignaturas = r"(?P<asignatura>([a-zA-ZÁÉÍÓÚáéíóú]+ )*[a-zA-ZÁÉÍÓÚáéíóú]+) (?P<casilla>\[(|X)\])"
compile_mis_asignaturas = re.compile(regex_linea_mis_asignaturas)

#función para obtener los datos del plan actual
def obtener_plan_actual(fichero): 
    with open(fichero, "r") as file: 
        return json.load(file)

#devuelve si una casilla está marcada o no
def casilla_marcada(casilla):
    isMarcada = False
    if (casilla[1] == 'X'):
        isMarcada = True

    return isMarcada

#función para obtener las asignaturas cursadas del fichero
def obtener_mis_asignaturas_plan_actual(fichero):
    mis_asignaturas = []
    with open(fichero, "r") as file: 
        for linea in file.readlines():
            if match := compile_mis_asignaturas.match(linea):
                if(casilla_marcada(match.group("casilla"))):
                    mis_asignaturas.append(linea)

    return mis_asignaturas

#recorro el plan de estudios y guardo el desglose de creditos de cada curso en una estructura de datos
def clasificar_creditos_plan_actual(plan_actual):
    lista = []
    for dict in plan_actual:
        if "curso" in dict:
            if(dict["curso"] == 1 or dict["curso"] == 2 or dict["curso"] == 3 or dict["curso"] == 4):
                lista.append(dict)

    return lista

#comprueba si los créditos de las menciones solo incluyen los dedicados al tfg
def comprobar_solo_tfg_plan_actual(software, computacion, computadores, redes):
    soloTFG = True

    for i in range(3, -1, -1):
        if(tipo_credito[i] == "TFG" and soloTFG == True):
            if(software[i] != 12):
                soloTFG = False

        elif(tipo_credito[i] != "TFG" and soloTFG == True):
            if(software[i] != 0 or computacion[i] != 0 or computadores[i] != 0 or redes[i] != 0):
                soloTFG = False

    return soloTFG

#comprueba si los créditos de las menciones son igual a 0
def comprobar_no_mencion_plan_actual(software, computacion, computadores, redes):
    sinMencion = True

    for i in range(0, 4):
        if(sinMencion == True):
            if(software[i] != 0 or computacion[i] != 0 or computadores[i] != 0 or redes[i] != 0):
                sinMencion = False

    return sinMencion

#devuelve la mención con más créditos cursada
def mencion_mas_creditos_plan_actual(software, computacion, computadores, redes):
    lista_creditos = [software, computacion, computadores, redes]
    hayVarias = False
    soloTFG = comprobar_solo_tfg_plan_actual(mis_creditos_cuarto_software, mis_creditos_cuarto_computacion, mis_creditos_cuarto_computadores, mis_creditos_cuarto_redes)
    resultado = {"mencion": None, "creditos": 0}
    contador = 0

    for creditos_mencion in lista_creditos:
        if(creditos_mencion > resultado["creditos"]):
            resultado["mencion"] = tipo_mencion[contador]
            resultado["creditos"] = creditos_mencion

            if(hayVarias):
                hayVarias = False
        
        elif(creditos_mencion ==  resultado["creditos"]):
            hayVarias = True

        contador += 1

    if(soloTFG):
        resultado["mencion"] = tipo_mencion[4]
        resultado["creditos"] = resultado["creditos"] + 12

    if(comprobar_no_mencion_plan_actual(mis_creditos_cuarto_software, mis_creditos_cuarto_computacion, mis_creditos_cuarto_computadores, mis_creditos_cuarto_redes)):
        resultado["mencion"] = tipo_mencion[4]
        resultado["creditos"] = resultado["creditos"]

    elif(hayVarias):
        resultado["mencion"] = tipo_mencion[5]

    return resultado

#devuelve la cantidad de créditos totales cursados
def creditos_totales_plan_actual():
    total_software = 0
    total_computacion = 0
    total_computadores = 0
    total_redes = 0
    
    for i in range(0, 4):
        total_software = total_software + mis_creditos_primero[i] + mis_creditos_segundo[i] + mis_creditos_tercero[i] + mis_creditos_cuarto_software[i]

    for i in range(0, 4):
        total_computacion = total_computacion + mis_creditos_primero[i] + mis_creditos_segundo[i] + mis_creditos_tercero[i] + mis_creditos_cuarto_computacion[i]

    for i in range(0, 4):
        total_computadores = total_computadores + mis_creditos_primero[i] + mis_creditos_segundo[i] + mis_creditos_tercero[i] + mis_creditos_cuarto_computadores[i]

    for i in range(0, 4):
        total_redes = total_redes + mis_creditos_primero[i] + mis_creditos_segundo[i] + mis_creditos_tercero[i] + mis_creditos_cuarto_redes[i]

    return mencion_mas_creditos_plan_actual(total_software, total_computacion, total_computadores, total_redes)

#devuelve el desglose de los créditos por curso y especialidad
def mis_creditos(mis_asignaturas, plan_actual):

    mis_cursos = [mis_creditos_primero, mis_creditos_segundo, mis_creditos_tercero, mis_creditos_cuarto_software, mis_creditos_cuarto_computacion, mis_creditos_cuarto_computadores, mis_creditos_cuarto_redes]

    for linea in mis_asignaturas:
        if match := compile_mis_asignaturas.match(linea):
            asignatura = match.group("asignatura")

            for actual in plan_actual:
                if "asignatura" in actual:
                    if(asignatura == actual["asignatura"] and (actual["cuatrimestre"] == 1 or actual["cuatrimestre"] == 2)):
                        mis_creditos_primero[actual["tipo"]] += actual["creditos"]

                    elif(asignatura == actual["asignatura"]and (actual["cuatrimestre"] == 3 or actual["cuatrimestre"] == 4)):
                        mis_creditos_segundo[actual["tipo"]] += actual["creditos"]

                    elif(asignatura == actual["asignatura"] and (actual["cuatrimestre"] == 5 or actual["cuatrimestre"] == 6)):
                        mis_creditos_tercero[actual["tipo"]] += actual["creditos"]

                    elif(asignatura == actual["asignatura"] and (actual["cuatrimestre"] == 7 or actual["cuatrimestre"] == 8)):
                        if "mencion" in actual:
                            if actual["mencion"] == "software":
                                mis_creditos_cuarto_software[actual["tipo"]] += actual["creditos"]
                            
                            elif actual["mencion"] == "computacion":
                                mis_creditos_cuarto_computacion[actual["tipo"]] += actual["creditos"]
                            
                            elif actual["mencion"] == "computadores":
                                mis_creditos_cuarto_computadores[actual["tipo"]] += actual["creditos"]

                            elif actual["mencion"] == "redes":
                                mis_creditos_cuarto_redes[actual["tipo"]] += actual["creditos"]

                        elif actual["asignatura"] == "Trabajo fin de grado":
                            mis_creditos_cuarto_software[actual["tipo"]] += actual["creditos"]
                            mis_creditos_cuarto_computacion[actual["tipo"]] += actual["creditos"]
                            mis_creditos_cuarto_computadores[actual["tipo"]] += actual["creditos"]
                            mis_creditos_cuarto_redes[actual["tipo"]] += actual["creditos"]
    
    return mis_cursos

#comprueba que dicho curso tiene los créditos biene elegidos entre optativas, obligatorias y de formación básica
def comprobar_creditos_curso(curso, mi_curso):
    tipoFallo = 5

    if(curso["optativo"] < mi_curso[0]):
        tipoFallo = 0

    elif(curso["basico"] < mi_curso[1]):
        tipoFallo = 1

    elif(curso["obligatorio"] < mi_curso[2]):
        tipoFallo = 2

    elif(curso["tfg"] < mi_curso[3]):
        tipoFallo = 3

    return tipoFallo

#usa la función de arriba, ya que se le pasan todos los cursos
def comprobar_creditos(clasificacion, mi_curso):
    sinFallos = True
    contador = 0

    for anyo in mi_curso:
        try:
            tipo = comprobar_creditos_curso(clasificacion[contador], anyo)
            if (tipo != 5):
                raise Exception(f"Los creditos del tipo {tipo_credito[tipo]} en el curso {contador + 1} exceden el valor para el plan actual.")
        
        except Exception as e:
            sinFallos = False
            print(f"ErrorCréditos: {e}")

        if(contador < 3):
            contador += 1

    return sinFallos

#desglose de los créditos que nos faltan por cursar
def desglose_creditos_por_cursar():
    primero = [0, 60, 0, 0]
    segundo = [0, 0, 60, 0]
    tercero = [6, 0, 54, 0]
    cuarto = [12, 0, 36, 12]

    mis_creditos_cuarto_total = [0, 0, 0, 0]
    mis_creditos_curso = [mis_creditos_primero, mis_creditos_segundo, mis_creditos_tercero, mis_creditos_cuarto_total]

    for i in range(0, 4):
        if(i == 0): 
            mis_creditos_cuarto_total[i] = mis_creditos_cuarto_software[i]

        else: mis_creditos_cuarto_total[i] = mis_creditos_cuarto_software[i] + mis_creditos_cuarto_computacion[i] + mis_creditos_cuarto_computadores[i] + mis_creditos_cuarto_redes[i]

    anyos = [primero, segundo, tercero, cuarto]
    nombre_cursos_dict = {0: "primero", 1: "segundo", 2: "tercero", 3:"cuarto"}
    contador = 0
    str_res = ""

    for curso in anyos:
        cursoEscrito = False
        for i in range (0, 4):
            creditos_restantes = curso[i] - mis_creditos_curso[contador][i]

            if not cursoEscrito and creditos_restantes > 0:
                cursoEscrito = True
                str_aux1 = f"\tDesglose de los créditos de {nombre_cursos_dict[contador]}: \n"

                if(tipo_credito[i] != "TFG"):
                    str_aux2 = f"\t\tTe quedan {creditos_restantes} créditos {tipo_credito[i]}s.\n"
                else:
                    str_aux2 = f"\t\tTe quedan {creditos_restantes} créditos {tipo_credito[i]}.\n"

                str_res = str_res + str_aux1 + str_aux2
            
            elif cursoEscrito and creditos_restantes > 0:
                if(tipo_credito[i] != "TFG"):
                    str_aux = f"\t\tTe quedan {creditos_restantes} créditos {tipo_credito[i]}s.\n"
                else:
                    str_aux = f"\t\tTe quedan {creditos_restantes} créditos {tipo_credito[i]}.\n"
                str_res = str_res + str_aux

        contador += 1

        if(cursoEscrito):
            str_res += '\n'

    return str_res

def resultado_actual():
    plan_actual = obtener_plan_actual(".plan-actual.json") #aquí se almacenará todo el json del plan actual
    mis_asignaturas = obtener_mis_asignaturas_plan_actual("mis-asignaturas.txt") #guardamos la información de nuestras asignaturas cursadas
    
    clasificacion_actuals = clasificar_creditos_plan_actual(plan_actual)

    mi_curso = mis_creditos(mis_asignaturas, plan_actual)

    if(comprobar_creditos(clasificacion_actuals, mi_curso)): 
        total = creditos_totales_plan_actual()
        porcentaje = total["creditos"]/240 * 100
        str_1 = f"Plan actual:\n\tEnhorabuena, tus créditos totales en el plan nuevo son: {total['creditos']} y te especializarías en la mención de {total['mencion']}. Esto supone el {porcentaje}% de créditos superados.\n\n"
        str_2 = desglose_creditos_por_cursar()

        return str_1 + str_2