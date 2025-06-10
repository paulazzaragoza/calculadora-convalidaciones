import os
import json
import regex as re
from plan_actual import obtener_mis_asignaturas_plan_actual, resultado_actual
from plan_nuevo import resultado_nuevo, obtener_optativos_restantes, casilla_marcada

#expresión regular para las líneas
regex_linea_mis_asignaturas = r"(?P<asignatura>([a-zA-ZÁÉÍÓÚáéíóú]+ )*[a-zA-ZÁÉÍÓÚáéíóú]+) (?P<casilla>\[(|X)\])"
compile_mis_asignaturas = re.compile(regex_linea_mis_asignaturas)

#variable que guarda el valor de una casilla marcada
casilla_marcada = "[X]"

#obtenemos mis asiganturas del plan actual


#guarda la optativas que se cursan en el plan nuevo e indica si se han cogido o no
optativas_plan_nuevo_crusadas = {"Prácticas externas I": False,
    "Fundamentos de los sistemas ciberfísicos": False,
    "Imagen digital": False,
    "Interfaces de visualización de datos I": False,
    "Informática industrial": False,
    "Seguridad en servicios y sistemas I": False,
    "Prácticas externas II": False}

#función para obtener las convalidaciones
def obtener_convalidaciones(fichero):
    with open(fichero, "r") as doc: 
        return json.load(doc)

#función para obtener las claves de las convalidaciones
def obtener_claves_convalidaciones(convalidaciones):
    claves = []
    for dict in convalidaciones:
        for key in dict.keys():
            if key not in claves:
                claves.append(key)

    return claves

def obtener_convalidacion(asignatura, convalidaciones):
    claves = obtener_claves_convalidaciones(convalidaciones)
    nueva = None

    if asignatura in claves:
        for convalidacion in convalidaciones:
            if asignatura in convalidacion.keys():
                return convalidacion[asignatura]

    return nueva

#función para obtener las convalidaciones iniciales
def obtener_mis_convalidaciones_iniciales(mis_asignaturas, convalidaciones):
    mis_convalidaciones = []
    for asignatura in mis_asignaturas:
        asignatura_nombre_actual = compile_mis_asignaturas.match(asignatura).group("asignatura")
        
        mis_convalidaciones.append(obtener_convalidacion(asignatura_nombre_actual, convalidaciones))
    
        #if(asignatura_nombre_actual == "Álgebra y matemática discreta"): 
            #mis_convalidaciones.append("Matemática discreta")

    with open(".archivo-auxiliar.txt", "w") as example:
        with open(".plantilla-plan-nuevo.txt", "r") as file:
            for line in file.readlines():
                if match := compile_mis_asignaturas.match(line):
                    if match.group("asignatura") in mis_convalidaciones:
                            linea_marcada = match.group("asignatura") + " " + casilla_marcada + '\n'
                            example.write(linea_marcada)

                            if match.group("asignatura") in optativas_plan_nuevo_crusadas.keys(): 
                                optativas_plan_nuevo_crusadas[match.group("asignatura")] = True

                    else:
                        example.write(line)
                
                else:
                        example.write(line)

#función para obtener las asignaturas que no tiene convalidación
def obtener_asignaturas_sin_convalidacion(mis_asignaturas, claves):
    asignaturas_sin_covalidacion = []
    for actual in mis_asignaturas:
        asignatura_nombre_actual = compile_mis_asignaturas.match(actual).group("asignatura")

        if asignatura_nombre_actual not in claves: 
            asignaturas_sin_covalidacion.append(asignatura_nombre_actual)

    return asignaturas_sin_covalidacion

#función para marcar una asignatura
def marcar_asignatura(asignatura):
    with open("mis-asignaturas-convalidadas.txt", "w") as example:
        with open(".archivo-auxiliar.txt", "r") as file:
            for line in file.readlines():
                if match := compile_mis_asignaturas.match(line):
                    if(match.group("casilla"))[1] != 'X' and match.group("asignatura") == asignatura:
                        linea_marcada = match.group("asignatura") + " " + casilla_marcada + '\n'
                        optativas_plan_nuevo_crusadas[match.group("asignatura")] = True
                        example.write(linea_marcada)
                    
                    else: 
                        example.write(line)

                else:
                    example.write(line)

#devuelve las asignaturas optativas que no están seleccionadas en el plan nuevo
def asignaturas_optativas_sin_seleccionar_plan_nuevo(): 
    keyset = optativas_plan_nuevo_crusadas.keys()
    sin_cursar = dict()
    contador = 0

    for key in keyset:
        if optativas_plan_nuevo_crusadas[key] == False:
            sin_cursar[contador] = key
            contador += 1

    return sin_cursar

def main():


    convalidaciones = obtener_convalidaciones("convalidaciones.json")

    mis_asignaturas = obtener_mis_asignaturas_plan_actual("mis-asignaturas.txt")
    obtener_mis_convalidaciones_iniciales(mis_asignaturas, convalidaciones)
    asignaturas_sin_covalidacion = obtener_asignaturas_sin_convalidacion(mis_asignaturas, obtener_claves_convalidaciones(convalidaciones))
    print(asignaturas_sin_covalidacion)
    creditos_optativos = obtener_optativos_restantes()
    optativas_sin_cursar = asignaturas_optativas_sin_seleccionar_plan_nuevo()

    while(creditos_optativos != 0 and len(asignaturas_sin_covalidacion) > 0):
        print(f"Tienes {len(asignaturas_sin_covalidacion)} asignaturas que puedes convalidar por optativas. Escribe su número.")
        for key in  optativas_sin_cursar.keys():
            print(f"{key}-.{optativas_sin_cursar[key]}")
        
        num = input("\nNúmero de la optativa: ")
        marcar_asignatura(optativas_sin_cursar[int(num)])
        creditos_optativos -= 6
        del asignaturas_sin_covalidacion[0]
        optativas_sin_cursar = asignaturas_optativas_sin_seleccionar_plan_nuevo()

    os.remove(".archivo-auxiliar.txt")
    os.system("clear")

    str_resultado_actual = resultado_actual()
    print(str_resultado_actual)

    str_resultado_nuevo = resultado_nuevo()
    print(str_resultado_nuevo)

if __name__ == "__main__":
    main()