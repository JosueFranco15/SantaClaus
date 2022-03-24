import time
import random

def vacaciones():
    time.sleep(random.randint(7,10))

def reno_fnc():
    global renos
    global nombres_renos
    vacaciones()
    semaf_principal.acquire()
    renos += 1
    print(f'el num de los renos {renos}')
    print(f'Llegó el reno {nombres_renos[renos-1]}')
    time.sleep(random.randint(1,4))
    if renos == 7:
        print('Ya estamos los 7 renos, hablenle a Santa!!')
        santa_semaf.release()
    else:
        print('\n')
    semaf_principal.release()
    renos_semaf.acquire()
    enganchar_trineo()

def enganchar_trineo():
    print('Renos enganchando trineo...')
    time.sleep(random.randint(1,3))
    print('Renos listos!')
    time.sleep(random.randint(1,2))
    print('¡Repartiendo juguetes...!')