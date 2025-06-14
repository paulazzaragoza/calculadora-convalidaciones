# calculadora-convalidaciones
Este proyecto es una calculadora para la convalidaciones entre el [plan de estudios actual](https://www.um.es/web/estudios/grados/informatica/plan-guias) (última actualización curso 2024/2025) y el [nuevo plan de estudios](https://www.um.es/documents/120586/13682118/Criterio+4.1+Descripcion+del+plan+de+estudios.pdf/b6504539-20ce-a69e-47c9-ae6d36568509?t=1721117452031) de la Univerisdad de Murcia. Para ello hemos tenido en cuenta la [tabla de adpataciones](https://www.um.es/documents/120586/145413/Tabla+Adaptaci%C3%B3n+GII+plan+1+al+plan+2.pdf/bfb582c8-7e8e-c3f4-31d9-d4ec974e5101?t=1731425581811) subidas por la propia Universidad de Murcia (última actualización 22 de noviembre de 2024).

## manual de usuario
Primero de todo __tenemos que acceder al fichero mis-asignaturas.txt__ que contiene todas las asignatura del plan actual divididas por cursos y por menciones. Para señalar una asignatura que hemos cursado o queremos cursar debemos marcarla -> [X]. Si no queremos cursar una asignatura debemos dejarla en blanco -> [].
- Autómatas y lenguajes formales [X] (ejemplo de asignatura marcada porque está aprobada o queremos cursarla).
- Compiladores [] (ejemplo de asignatura sin marcar).

> ⚠️ **Advertencia:** la __X__ con la que marquemos debe ser en __mayúscula__.

Para usar nuestro programa __debemos estar en la ruta donde se encuentre la descarga del repositorio__. Una vez en la ruta del repositorio debemos ejecutar: 
```
./convalidaciones
```
o
```
python3 convalidaciones.py
```

Si tienes asignaturas que pueden convalidarse por optatitvas te saldrá en pantalla un listado de las opatitiva del plan nuevo indexadas con un número. Para seleccionar que quieres la covalidación con esa optativa, debes teclear dicho número que lo indexa. 
- 0-.Prácticas externas I (ejemplo de salida por terminal del listado de optativas).
- Número de la optativa: 0 (ejemplo para marcar que quieres esa optativa convalidada).

¡Listo! __Ya tienes tus resultados en el fichero mis-asignaturas-convalidadas.txt__. Este fichero tiene la misma estructura que el fichero inicial, está separado por cursos y por menciones. Como hemos mencionado antes si encontramos una casilla marcada -> [X] significa que esa asignatura esta aprobada. Si, por el contrario, encontramos que la casilla está vacía -> [] esto significa que la asignatura no está superada y se tendría que cursar. 
- Estructura y tecnología de computadores [X] (ejemplo de asignatura aprobada con el nuevo plan).
- Algoritmos y estructuras de datos II [] (ejemplo de asignatura no superada con el nuevo plan).

## explicación del la salida
Tras toda esta ejecución, al final del programa te saldrá un desglose de los créditos que te faltan por cursar. Este deslgose está tanto con el plan actual como con el plan nuevo y te indica, además, el tipo de crédito que es: formación básica, obligatoria o TFG. 
