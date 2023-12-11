# Cooperativa
from random import randint
from tabulate import tabulate

def mostrar_localidades():
    localidades = ['Pinamar' , 'Ostende' , 'Cariló' , 'Valeria']
    for i,localidad in enumerate(localidades , 1):
            print(f'{i} - {localidad}')
    return None


def mostrar_opciones():
    for i, e in enumerate('Guardar los datos y salir del programa/Agregar abonado nuevo/Buscar abonado por apellido/Mostrar todos los abonados/Eliminar un abonado del sistema'.split('/')):
        print(f'{i} - {e}')
    return None


def nuevo_abonado():
    nuevo_abonado = ['nro_abonado' , 'apellido' , 'dni' , 'localidad' , 'ip']
    while nuevo_abonado[0] in datos_abonados or nuevo_abonado[0] == 'nro_abonado':
        nuevo_abonado[0] = randint(1000,9999)
    print(f'\nCreando abonado numero: {nuevo_abonado[0]}')
    while True:
        nuevo_abonado[1] = input('\nIngrese el apellido del abonado: ').capitalize()
        if nuevo_abonado[1].isalpha(): 
            break
    while True:
        nuevo_abonado[2] = input('\nIngrese el DNI del abonado sin puntos (ej: 12345678): ')
        if nuevo_abonado[2].isdigit():
            nuevo_abonado[2] = int(nuevo_abonado[2])
            if nuevo_abonado[2] > 1000000 and nuevo_abonado[2] < 100000000:
                break 
    mostrar_localidades()
    while True:
        nuevo_abonado[3] = input('\nIngrese el numero que corresponda a la localidad del abonado: ')
        try:
            nuevo_abonado[3] = int(nuevo_abonado[3])
        except:
            continue
        else:
            if nuevo_abonado[3] in range(1,5):
                break     
    while True:
        ip = input('\nIngrese la IP para el abonado (formato = 000.000.000.000): ')
        try:
            nuevo_abonado[4] = tuple(int(e) for e in ip.split('.'))
        except:
            continue
        else:
            if len(nuevo_abonado[4]) == 4 and all(nuevo_abonado[4] not in lista for lista in list(datos_abonados.values())):
                break

    datos_abonados[nuevo_abonado[0]] = nuevo_abonado[1:]

    return None

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
                datos_abonados[int(datos[0])] = [datos[1], int(datos[2]), int(datos[3]), (datos[4])]       
    except:
        return None
    return 'Nro_abonado;Apellido;Dni;Localidad;IP\n'.split(';')



def buscar_abonado_por_apellido():
        
    apellido_buscar = input("Ingrese el apellido a buscar: ").capitalize()
    
    for nro, datos in datos_abonados.items():
        if datos[0] == apellido_buscar:
            return tabulate([[nro , *datos]], headers=[dato for dato in encabezado], tablefmt="fancy_grid")
    return None

def mostrar_todos_los_abonados():

    datos_tabla = [[clave , *valor] for clave, valor in datos_abonados.items()]

    # Imprimir la tabla
    tabla = tabulate(datos_tabla, headers=[dato for dato in encabezado], tablefmt="fancy_grid")
    print(tabla)
    return None

#parte de eliminar_abonados()

def eliminar_abonado():
    
    nro_eliminar = input("Ingrese el número de abonado a eliminar: ")
    if nro_eliminar.isdigit():
        nro_eliminar = int(nro_eliminar)
    else:
        print(f'{nro_eliminar} no es un número.')
    if nro_eliminar in datos_abonados:
        del datos_abonados[nro_eliminar]
        print(f"Abonado {nro_eliminar} eliminado.")
    else:
        print(f"No se encontró el abonado con el número {nro_eliminar}.")

def menu():
    while True:
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

datos_abonados = {}
encabezado = cargar_datos()
if not datos_abonados:
    op = input('Ocurrio un error al cargar el archivo. ¿Desea usar el programa sin datos preexistentes? (Y/N): ').lower()
    if op == 'y':
        menu()
        guardar_datos()
else:
    menu()
    guardar_datos()
print('El programa finalizó.')