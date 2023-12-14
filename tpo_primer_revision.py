# Cooperativa
from random import randint # Usada para generar los numeros de abonado
from tabulate import tabulate #libreria para mostrar la estructura en formato de tabla (facilita el printeo)
from os import name , system # Funcion para limpiar la consola y que no se acumulen salidas.
from msvcrt import getch # Funcion para freezear los prints y que no se limpien de la consola.

def limpiar_consola():
    sistema_operativo = name
    if sistema_operativo == 'posix':  # Linux y macOS
        system('clear')
    elif sistema_operativo == 'nt':  # Windows
        system('cls')


def mostrar_localidades():
    # La funcion printea las locacalidades disponibles y el numero que corresponde 
    localidades = ['Pinamar' , 'Ostende' , 'Cariló' , 'Valeria']
    for i,localidad in enumerate(localidades , 1):
            print(f'{i} - {localidad}')


def mostrar_opciones(): 
    # La funcion muestra las opciones del menu y los numeros que corresponden a cada uno
    for i, e in enumerate('Guardar los datos y salir del programa/Agregar abonado nuevo/Buscar abonado por apellido/Mostrar todos los abonados/Eliminar un abonado del sistema'.split('/')): #usa la barra como divisor para crear lista a partir de string 
        print(f'{i} - {e}')


def validar_ip(dato): 
        # La funcion recibe el dato que ingresa el usuario y valida que sea una ip valida (4 numeros de 000 a 255 separados por puntos.) y lo devuelve como una tupla de enteros
        # En cualquier otro caso devuelve None
        try:
            dato = tuple(int(e) for e in dato.split('.'))
            assert all(e >= 0 and e < 256 for e in dato)
            assert len(dato) == 4
        except:
            return None
        else:
            return dato

def convertir_ciudad(numero:int) -> str:
    localidades = ['Pinamar' , 'Ostende' , 'Cariló' , 'Valeria']
    return localidades[numero - 1]

def nuevo_abonado():
    limpiar_consola()
    nuevo_abonado = {'numero' : 0 }
    while nuevo_abonado['numero'] in datos_abonados or nuevo_abonado['numero'] == 0:
        nuevo_abonado['numero'] = randint(1000,9999)
    print(f'\nCreando abonado numero: {nuevo_abonado['numero']}')
    while True:
        nuevo_abonado['apellido'] = input('\nIngrese el apellido del abonado: ').capitalize()
        if nuevo_abonado['apellido'].isalpha(): 
            break
    while True:
        nuevo_abonado['dni'] = input('\nIngrese el DNI del abonado sin puntos (ej: 12345678): ')
        if nuevo_abonado['dni'].isdigit():
            nuevo_abonado['dni'] = int(nuevo_abonado['dni'])
            if nuevo_abonado['dni'] > 1000000 and nuevo_abonado['dni'] < 100000000:
                break 
    mostrar_localidades()
    while True:
        nuevo_abonado['localidad'] = input('\nIngrese el numero que corresponda a la localidad del abonado: ')
        try:
            nuevo_abonado['localidad'] = int(nuevo_abonado['localidad'])
        except:
            continue
        else:
            if nuevo_abonado['localidad'] in range(1,5):
                break     
    while True:
        nuevo_abonado['ip'] = input('\nIngrese la IP para el abonado (formato = 000.000.000.000): ')
        if ip:=validar_ip(nuevo_abonado['ip']):
            nuevo_abonado['ip'] = ip
            break

    datos_abonados[nuevo_abonado['numero']] = tuple(nuevo_abonado.values())[1:]

def guardar_datos():
    
    try:
        with open('abonados.csv', 'w', encoding='utf-8') as archivo_abonados:

            archivo_abonados.write(';'.join(encabezado))

            for nro,abonado in datos_abonados.items():
                linea = f'{nro};' + ';'.join(map(str, abonado)) + '\n'
                archivo_abonados.write(linea)

        print("Datos de abonados guardados correctamente en 'abonados.csv'")
    except Exception as e:
        print(f"Error al guardar los datos de abonados: {e}")

def cargar_datos():
    
    try:
        with open('abonados.csv', 'r' , encoding='UTF-8') as file:
            file.readline() #saltar primer linea
            for line in file:  
                datos = [dato for dato in line.strip().split(';')]
                datos_abonados[int(datos[0])] = [datos[1], int(datos[2]), int(datos[3]), tuple(int(e) for e in datos[4].strip('()').split(','))]       
    except:
        return None
    return 'Nro_abonado;Apellido;Dni;Localidad;IP\n'.split(';')



def buscar_abonado_por_apellido():
    limpiar_consola()
    apellido_buscar = input("Ingrese el apellido a buscar: ").capitalize()
    
    lista = [[clave , valor[0] ,valor[1] ,convertir_ciudad(valor[2]) , ','.join('{:03}'.format(x) for x in valor[3])] for clave, valor in datos_abonados.items() if valor[0] == apellido_buscar] #mejor formato para mostrar los datos
    if lista:
        return tabulate(lista, headers=[dato for dato in encabezado], tablefmt="fancy_grid")
    else: 
        return None

def mostrar_todos_los_abonados() -> None:
    limpiar_consola()
    datos_tabla = [[clave , valor[0] ,valor[1] ,convertir_ciudad(valor[2]) , ','.join('{:03}'.format(x) for x in valor[3])] for clave, valor in datos_abonados.items()] #mejor formato para mostrar los datos
    # Imprimir la tabla
    tabla = tabulate(datos_tabla, headers=[dato for dato in encabezado], tablefmt="fancy_grid")
    print(tabla)

def eliminar_abonado():
    
    limpiar_consola()
    nro_eliminar = input("Ingrese el número de abonado a eliminar: ")
    if nro_eliminar.isdigit():
        nro_eliminar = int(nro_eliminar)
    else:
        print(f'{nro_eliminar} no es un número.')
    if nro_eliminar in datos_abonados:
        del datos_abonados[nro_eliminar]
        print(f"Abonado {nro_eliminar} eliminado con éxito.")
    else:
        print(f"No se encontró el abonado con el número {nro_eliminar}.")

def menu():
    while True:
        limpiar_consola()
        mostrar_opciones()
        op = input('Ingrese la opcion a realizar: ')
        if op == '0':
            break
        elif op == '1':
            nuevo_abonado()
        elif op == '2':
            dato = buscar_abonado_por_apellido()
            if not dato:
                print('No se pudo encontrar el abonado')
            else:
                print(dato)
        elif op == '3':
            mostrar_todos_los_abonados()
        elif op == '4':
            eliminar_abonado()
        else:
            print('Opcion invalida.')
        print('Presione una tecla para continuar')
        getch()


datos_abonados = {}
encabezado = cargar_datos()
if not datos_abonados:
    op = input('Ocurrio un error al cargar el archivo. ¿Desea usar el programa sin datos preexistentes? (Y/N): ').lower()
    if op == 'y':
        menu()
        guardar_datos()
else:
    menu()
    limpiar_consola()
    guardar_datos()
print('El programa finalizó.')
