import time
import random

def santa_fnc():
    global renos
    global duendes
    global total_renos
    global total_duendes_ayudados
    while True:
        santa_semaf.acquire()
        semaf_principal.acquire()
        print('santa')
        
        print(f'numero de duendes {duendes}')
        if renos == total_renos:
            print('reni')
            preparar_trineo()
            renos = 0
            for _ in range(total_renos):
                renos_semaf.release()
        else:
            if duendes == total_duendes_ayudados:
                print('duendi')
                ayudar_duendes()
                duendes = 0
                for _ in range(total_duendes_ayudados):
                    duendes_semaf.release()
            else:
                print('nada')
        semaf_principal.release()

def ayudar_duendes():
    print('Santa esta ayudando a duendes...')
    time.sleep(random.randint(1,3))

def preparar_trineo():
    print('Santa esta preparando el trineo...')
    time.sleep(random.randint(1,3))
    print('El trineo está listo!')
    time.sleep(1)
    print('Amonooooossss mis renooss!')