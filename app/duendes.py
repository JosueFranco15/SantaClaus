import time
import random

def duende_fnc():
    global duendes
    global total_duendes
    #? Semáforo para esperar cuando santa esta ayudando a otro grupo de duendes
    duendes_help_semaf.acquire()
    semaf_principal.acquire()

    duendes +=1
    print('Llegó un duende')
    time.sleep(random.randint(1,4))
    print(f'los due: {duendes}')
    if duendes == 3:
        santa_semaf.release()
        print('Santa viene a ayudarnos')
    else:
        # duendes_help_semaf.release()
        print('Necesitamos otro duende')
    semaf_principal.release()
    duendes_semaf.acquire()
    obtener_ayuda()
    semaf_principal.acquire()
    duendes -= 1
    if duendes == 0:
        duendes_help_semaf.release()
    semaf_principal.release()

def obtener_ayuda():
    global duendes
    print('Santa claus ayudando...')
    time.sleep(random.randint(1,3))
    print('Grupo de duendes ayudados')