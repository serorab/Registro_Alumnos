import pygame #Librería necesaria para la reproducción del audio.
import time #Se importa para controlar el tiempo de reproducción del audio.
import pickle
from itertools import islice
from banner import baner
from validaciones import alfabetico
from validaciones import numerico

# Declaración de variables
listaTitulos = ['DNI:', 'Nombre:', 'Apellido:', 'Domicilio:']
listaMaterias = ['Materia 1:', 'Materia 2:']
listaNotas = ['Nota 1', 'Nota 2']

menu_1 = '''
                    Seleccione el número de la opción deseada:

            1. Ver alumnos inscriptos
            2. Agregar Alumno
            3. Consultar datos del alumno y/o agregar materias.
            4. Dar de baja a un alumno.
            5. Salir
'''

menu_2 = '''        
                    Seleccione el número de la opción deseada:

            1. Modificar datos generales
            2. Agregar o cambiar materias
            3. Cargar y/o modificar notas
            4. <-- Volver atrás
'''

# Creación de funciones

# Menús
def opcionMenu_1():
    print(menu_1)
    opcion = input()

    if opcion == '1':
        verAlumnos()
        volverAtras()

    elif opcion == '2':
        agregarAlumno()
        volverAtras()

    elif opcion == '3':
        print("Ingrese el DNI del alumno: ", end='')
        dni = input()
        print('\nINFORMACIÓN DEL ALUMNO:')
        if consultarAlumno(dni):

            #Imprime los datos del alumno
            for index, (llave, valor) in enumerate(islice(consultarAlumno(dni).items(), 4)):
                print(llave, valor)

            for index, (key, value) in enumerate(islice(consultarAlumno(dni).items(), 6, None)):
                print(key, value)

            opcionMenu_2(dni)
        else:
            print(f'No se encontró el DNI {dni} en la base de datos.')
            volverAtras()

    elif opcion == '4':
        print('''
¡ADVERTENCIA! Esta acción borrará todos los datos del alumno de manera permanente.
        
                            ¿Desea continuar? S/N

        ''')
        opcion = input()
        if opcion.upper() == 'S':
            dni = input('Ingrese el DNI del alumno: ')
            if consultarAlumno(dni):
                print('Se borrará de manera permanente el registro de:')
                for index, (key, value) in enumerate(islice(consultarAlumno(dni).items(), 4)):
                    print(key, value)
                print('\n¿Desea continuar? S/N\n')
                op = input()
                if op.upper() == 'S':
                    eliminarAlumno(dni)

                elif op.upper() == 'N':
                    opcionMenu_1()

                else:
                    print('La opción ingresada no es válida')
                    opcionMenu_1()

            else:
                print(f'El DNI {dni} no se puede eliminar porque no pertenece a la base de datos.')
                opcionMenu_1()

        elif opcion.upper() == 'N':
            opcionMenu_1()

        else:
            print('La opción ingresada no es válida.')
            opcionMenu_1()

    elif opcion == '5':
        print(baner)
        reproducirAudio()        
        exit()

    else:
        print('La opción ingresada no es válida.')
        opcionMenu_1()

def opcionMenu_2(dni):
    print(menu_2)
    opcion = input()

    if opcion == '1':
        print('DATOS GENERALES')

        #Muestra los primeros 4 datos del alumno (DNI, Nombre, Apellido y Domicilio).
        for index, (key, value) in enumerate(islice(consultarAlumno(dni).items(), 4)):
            print(key, value)

        modificarDatosG(dni)

    elif opcion == '2':
        print('''
¡ATENCIÓN! Esta acción borrará los registros de las materias actuales incluyendo sus calificaciones. 
       Si lo que desea es modificar las notas, vaya a la opción "Ver y/o modificar notas".
    
                                ¿Desea continuar? S/N
                                ''')
        op = input()
        if op.upper() =='S':
            agregarMaterias(dni)
            agregarNotas(dni)
            opcionMenu_2(dni)

        elif op.upper() == 'N':
            opcionMenu_2(dni)

        else:
            print('La opción ingresada no es válida.')
            opcionMenu_2(dni)

    elif opcion == '3':
        if len(consultarAlumno(dni)) > 6:
            print('Las notas del alumno', consultarAlumno(dni)['Nombre:'], consultarAlumno(dni)['Apellido:'], 'son:')

            # El ciclo itera desde el elemento 6
            for index, (key, value) in enumerate(islice(consultarAlumno(dni).items(), 6, None)):
                print(key, value)

            print('\n¿Desea hacer modificaciones a las notas? S/N\n')
            mod = input()

            if mod.upper() == 'S':
                modificarNotas(dni)
                opcionMenu_2(dni)

            elif mod.upper() == 'N':
                opcionMenu_2(dni)

            else:
                print('La opción ingresada no es válida.')
                opcionMenu_2(dni)

        else:
            print(
                f"El alumno {consultarAlumno(dni)['Nombre:']} {consultarAlumno(dni)['Apellido:']} aún no tiene materias cargadas. \n\n¿Desea cargar las materias en este momento? S/N\n")
            op = input()
            if op.upper() == 'S':
                if len(consultarAlumno(dni)) < 5:
                    agregarMaterias(dni)
                    agregarNotas(dni)
                    modificarNotas(dni)
                    opcionMenu_2(dni)

                else:
                    agregarNotas(dni)
                    opcionMenu_2(dni)

            elif op.upper() == 'N':
                opcionMenu_2(dni)

            else:
                print('La opción ingresada no es válida.')
                opcionMenu_2(dni)

    else:
        opcionMenu_1()

def volverAtras():
    print('\n<-- Presione Enter para volver atrás')
    input()
    opcionMenu_1()

# Funciones para ver y manipular los datos

def verAlumnos():
    print('Alumnos inscriptos:\n')

    #Con try consigo poner excepciones en el caso de haber un error
    #Con With me aseguro que el archivo externo se cierre finalizada la acción.
    try:
        with open('Alumnos.IFTS18', 'rb') as alumnos:
            abrirListaGeneral = pickle.load(alumnos)
            if len(abrirListaGeneral) < 1:
                print('La lista se encuentra vacía. Por favor, ingrese alumno desde el menú principal.')

            elif len(abrirListaGeneral) == 1:
                for i in abrirListaGeneral:
                    if len(i) < 1:
                        print('La lista se encuentra vacía. Por favor, ingrese alumno desde el menú principal.')

        for alumno in abrirListaGeneral:
            print(' ')
            #El ciclo itera sólo hasta el elemento 6 del diccionario
            for index, (key, value) in enumerate(islice(alumno.items(), 4)):
                print(key, value)

            if len(alumno)>4:
                print('Materia 1: ', alumno['Materia 1:'], '-', alumno[alumno['Materia 1:']]['Situación:'])
                print('Materia 2: ', alumno['Materia 2:'], '-', alumno[alumno['Materia 2:']]['Situación:'])

            elif len(alumno) == 4:
                print('No tiene materias cargadas.')

    except FileNotFoundError:
        print('''
    El archivo "Alumnos" no se ha creado aún. Ingrese un alumno desde 
la opción "Agregar Alumno" del menú principal para crear la base de datos.''')
        opcionMenu_1()

def agregarAlumno():
    try:
        with open('Alumnos.IFTS18', 'rb+') as archivo:
            abrirDiccionario = pickle.load(archivo)
            listaNombres = abrirDiccionario
            diccionario = {}

            #Ciclo para ingresar datos del alumno
            for i in range(4):
                print("Ingrese ", listaTitulos[i], end=' ')
                dato = input()
                if listaTitulos[i] == 'DNI:':
                    if numerico(dato):
                        pass
                    else:
                        print("Ingrese sólo números sin espacio ni puntos")
                        break

                if listaTitulos[i] == "Nombre:":
                    if alfabetico(dato):
                        pass
                    else:
                        print("Ingrese sólo letras sin espacio ni puntos")
                        break

                if listaTitulos[i] == "Apellido:":
                    if alfabetico(dato):
                        pass
                    else:
                        print("Ingrese sólo letras sin espacio ni puntos")
                        break

                if consultarAlumno(dato):
                    print(f'El DNI {dato} ya pertenece a la base de datos.')
                    break

                diccionario[listaTitulos[i]] = dato

            # Agrega el diccionario a la lista y con 'seek', inicializa y desplaza el índice.
            # Finalmente 'pickle.dump' guarda en binario la información.
            listaNombres.append(diccionario)
            archivo.seek(0, 2)
            archivo.seek(0)
            pickle.dump(listaNombres, archivo)

    except FileNotFoundError:
        listaNombres = []
        diccionario = {}

        with open('Alumnos.IFTS18', 'wb') as archivo:

            #Ciclo para ingresar datos del alumno.
            for i in range(4):
                print("Ingrese ", listaTitulos[i], end=' ')
                dato = input()
                if listaTitulos[i] == 'DNI:':
                    if numerico(dato):
                        pass
                    else:
                        print("Ingrese sólo números sin espacio ni puntos")
                        break

                if listaTitulos[i] == "Nombre:":
                    if alfabetico(dato):
                        pass
                    else:
                        print("Ingrese sólo letras sin espacio ni puntos")
                        break
                diccionario[listaTitulos[i]] = dato

            #Agrega el diccionario a la lista y con 'seek', inicializa y desplaza el índice.
            #Finalmente 'pickle.dump' guarda en binario la información.
            listaNombres.append(diccionario)
            archivo.seek(0, 2)
            archivo.seek(0)
            pickle.dump(listaNombres, archivo)

def consultarAlumno(dni):
    with open('Alumnos.IFTS18', 'rb') as consulta:
        print('')
        consultaAlumno = pickle.load(consulta)
        diccionario = {}
        dniExiste = False

        #La variable 'valor' recorre los elementos de consultaAlumno.
        for valor in consultaAlumno:
            #La variable 'dicc' recorre los elementos de valor.
            for dicc in valor.items():
                if (dni == dicc[1]) and (dicc[0] == 'DNI:'):
                    for key, value in valor.items():
                        diccionario[key] = value
                        dniExiste = True

        if dniExiste:
            return diccionario

        else:
            return dniExiste

def modificarDatosG(dni):
    with open('Alumnos.IFTS18', 'rb+') as modificar:
        modificarAlumno = pickle.load(modificar)
        print('\nIngrese el número de la opción deseada:\n\n1. Para modificar DNI.\n2. Para modificar Nombre.\n3. Para modificar Apellido.\n4. Para modificar Domicilio.')
        seleccion = input()

        if seleccion == '1':
            seleccion = 'DNI:'
    
        elif seleccion == '2':
            seleccion = 'Nombre:'

        elif seleccion == '3':
            seleccion = 'Apellido:'

        elif seleccion == '4':
            seleccion = 'Domicilio:'

        else:
            print(f'{seleccion} no es una opción válida.')

        #Ciclo que busca al alumno y reemplaza el dato que elija el usuario.
        for valor in modificarAlumno:
            for mod in valor.items():
                if dni == mod[1] and (mod[0] == 'DNI:'):
                    for mod in valor.items():
                        if seleccion == mod[0]:
                            print(f'\nIngrese {seleccion}')
                            nuevoDato = input()
                            valor[seleccion] = nuevoDato
                            listaNueva = valor
                            if numerico(listaNueva['DNI:']):
                                modificarAlumno.remove(valor)
                            
                            else:
                                print('Ingrese sólo números sin espacio ni puntos')
                                opcionMenu_2(dni)                                

        modificarAlumno.append(listaNueva)
        modificar.seek(0)
        pickle.dump(modificarAlumno, modificar)

    print('\nInformación guardada con éxito.')
    opcionMenu_2(listaNueva['DNI:'])

def agregarMaterias(dni):
    listaMateria = []
    listaNueva = []
    diccionario = {}

    with open('Alumnos.IFTS18', 'rb+') as materia:
        agregaMateria = pickle.load(materia)

        for i in range(2):
            print('Ingrese ', listaMaterias[i])
            mat = input()
            listaMateria.append(mat)

        #Ciclo busca los datos del alumno, los guarda en una lista nueva y borra los datos anteriores.
        for valor in agregaMateria:
            for mod in valor.items():
                if dni == mod[1] and (mod[0] == 'DNI:'):
                    listaNueva = valor
                    agregaMateria.remove(valor)

        #Ciclo itera hasta el elemento 4 y los agrega a un diccionario.
        for index, (key, value) in enumerate(islice(listaNueva.items(), 4)):
            diccionario[key] = value

        for i in range(2):
            diccionario[listaMaterias[i]] = listaMateria[i]

        agregaMateria.append(diccionario)
        materia.seek(0)
        pickle.dump(agregaMateria, materia)

def agregarNotas(dni):
    listaNota = []
    listaMateriaNota = []
    diccionario1 = {}
    diccionario2 = {}

    with open('Alumnos.IFTS18', 'rb+') as notas:
        modificaNotas = pickle.load(notas)
        materiasMatriculadas = consultarAlumno(dni)

        #Ciclo que permite ingresar las notas de las materias
        for i in range(4):
            mat = 0.0
            listaNota.append(mat)

        #Ciclo que guarda los datos en una lista y borra la anterior.
        for valor in modificaNotas:
            for mod in valor.items():
                if dni == mod[1] and (mod[0] == 'DNI:'):
                    listaMateriaNota = valor
                    modificaNotas.remove(valor)

        #Ciclo que agrega los datos a diccionarios. Cada uno de ellos son agregados a las materias.
        for i in range(2):
            diccionario1[listaNotas[i]] = listaNota[i]
            diccionario2[listaNotas[i]] = listaNota[2 + i]

        diccionario1['Promedio general:'] = 0.0
        diccionario1['Situación:'] = 'No regular'
        diccionario2['Promedio general:'] = 0.0
        diccionario2['Situación:'] = 'No regular'
        listaMateriaNota[materiasMatriculadas[listaMaterias[0]]] = diccionario1
        listaMateriaNota[materiasMatriculadas[listaMaterias[1]]] = diccionario2

        modificaNotas.append(listaMateriaNota)
        notas.seek(0)
        pickle.dump(modificaNotas, notas)

def modificarNotas(dni):
    with open('Alumnos.IFTS18', 'rb+') as camNotas:
        cambioNotas = pickle.load(camNotas)

        print(f"Ingrese el número para la opción deseada:\n1. Para seleccionar {consultarAlumno(dni)['Materia 1:']}\n2. Para seleccionar {consultarAlumno(dni)['Materia 2:']}")
        mate = input()
        notaCam = consultarAlumno(dni)

        if mate == '1':
            print(f"Ingrese el número de la Calificación a cambiar:\n1. Para cambiar Nota 1 = {notaCam[notaCam['Materia 1:']]['Nota 1']}\n2. Para cambiar Nota 2 = {notaCam[notaCam['Materia 1:']]['Nota 2']}")
            nota = input()
            if nota == '1':
                cali = float(input('Ingrese la calificación: '))
                notaCam[notaCam['Materia 1:']]['Nota 1'] = cali

            elif nota == '2':
                cali = float(input('Ingrese la calificación: '))
                notaCam[notaCam['Materia 1:']]['Nota 2'] = cali

            else:
                print('La opción ingresada no es válida.')
                opcionMenu_2(dni)

        elif mate == '2':
            print(f"Ingrese el número de la Calificación a cambiar:\n1. Para cambiar Nota 1 = {notaCam[notaCam['Materia 2:']]['Nota 1']}\n2. Para cambiar Nota 2 = {notaCam[notaCam['Materia 2:']]['Nota 2']}")
            nota = input()

            if nota == '1':
                cali = float(input('Ingrese la calificación: '))
                notaCam[notaCam['Materia 2:']]['Nota 1'] = cali

            elif nota == '2':
                cali = float(input('Ingrese la calificación: '))
                notaCam[notaCam['Materia 2:']]['Nota 2'] = cali

            else:
                print('La opción ingresada no es válida.')
                opcionMenu_2(dni)

        else:
            print('La opción seleccionada no es válida.')
            opcionMenu_2(dni)

        promedio1 = round((((notaCam[notaCam['Materia 1:']]['Nota 1']) + (notaCam[notaCam['Materia 1:']]['Nota 2'])) / 2), 2)
        promedio2 = round((((notaCam[notaCam['Materia 2:']]['Nota 1']) + (notaCam[notaCam['Materia 2:']]['Nota 2'])) / 2), 2)

        def situacionMateria1():
            if promedio1 >= 7:
                return 'Regular'

            else:
                return 'No regular'

        def situacionMateria2():
            if promedio2 >= 7:
                return 'Regular'

            else:
                return 'No regular'

        notaCam[notaCam['Materia 1:']]['Promedio general:'] = promedio1
        notaCam[notaCam['Materia 1:']]['Situación:'] = situacionMateria1()
        notaCam[notaCam['Materia 2:']]['Promedio general:'] = promedio2
        notaCam[notaCam['Materia 2:']]['Situación:'] = situacionMateria2()

        # Ciclo que guarda los nuevos datos en una lista y borra la anterior.
        for valor in cambioNotas:
            for mod in valor.items():
                if dni == mod[1] and (mod[0] == 'DNI:'):
                    cambioNotas.remove(valor)

        cambioNotas.append(notaCam)
        camNotas.seek(0)
        pickle.dump(cambioNotas, camNotas)

def eliminarAlumno(dni):
    with open('Alumnos.IFTS18', 'rb+') as eliminar:
        bajaAlumno = pickle.load(eliminar)

        #Ciclo que busca al alumno y lo borra de la base de datos.
        for valor in bajaAlumno:
            for mod in valor.items():
                if dni == mod[1] and (mod[0] == 'DNI:'):
                    bajaAlumno.remove(valor)

        eliminar.seek(0)
        pickle.dump(bajaAlumno, eliminar)
    print('Operación exitosa')
    volverAtras()

def reproducirAudio():
    pygame.mixer.init()
    pygame.mixer.music.load('baby.mp3')
    pygame.mixer.music.play()
    time.sleep(2.5)
    pygame.mixer.music.stop()

opcionMenu_1()