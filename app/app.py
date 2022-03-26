import logging
import threading
import time, random
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk, ImageSequence


reno_img = Path(__file__).parent / "../img/reno1.gif"
santa_img = Path(__file__).parent / "../img/sleep_santa.gif"
duendes_img = Path(__file__).parent / "../img/duendes.gif"
trineo_img = Path(__file__).parent / "../img/trineo.gif"


log = logging.getLogger('claus')
console = logging.StreamHandler()
log.addHandler(console)
log.setLevel(logging.INFO)


#? Contadores
renos = 0
duendes = 0

#? Constantes
total_renos = 7
total_duendes = 9
total_duendes_ayudados = 3

nombres_renos = ["RODOLFO", "DONDER", "CUPIDO", "COMETA","PRANCER", "DANCER", "DASHER"]

santa_semaf = threading.Semaphore(0)
renos_semaf = threading.Semaphore(0)
duendes_semaf = threading.Semaphore(0)
#? Se dejan pasar 3 procesos (Duendes)
duendes_help_semaf = threading.Semaphore(3)
semaf_principal = threading.Semaphore(0)

#* ----------------- Duendes ----------------------------------------------
def duende_fnc():
    global duendes
    global total_duendes
    global duendes_img
    # play_gif(duendes_img)
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


#+ ----------------- Renos ------------------------------------------------
def vacaciones():
    time.sleep(random.randint(7,10))
def reno_fnc():
    global renos
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
#+ -----------------------------------------------------------------------

#! --------------------- Santa Claus -------------------------------------
def santa_fnc():
    global renos
    global duendes
    global total_renos
    global total_duendes_ayudados
    global santa_img
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
#! -----------------------------------------------------------------------

#? Función principal que crea hilos de duendes, renos y santa
def main_fnc():
    arr_hilos = []

    santa_hilo = threading.Thread(target=santa_fnc)
    arr_hilos.append(santa_hilo)

    for _ in range(total_renos):
        renos_hilo = threading.Thread(target=reno_fnc)
        arr_hilos.append(renos_hilo)
    
    for _ in range(total_duendes):
        duendes_hilo = threading.Thread(target=duende_fnc)
        arr_hilos.append(duendes_hilo)

    for hilo in arr_hilos:
        hilo.start()

    for hilo in arr_hilos:
        hilo.join()

window = tk.Tk()
window.title("Problema Santa Claus in Py")
window.geometry("700x500")
def play_gif(image_path):
    global img
    img = Image.open(image_path)
    lbl = tk.Label(window)
    lbl.place(x=50,y=10)
    for img in ImageSequence.Iterator(img):
        img = ImageTk.PhotoImage(img)
        lbl.config(image = img)
        window.update()
        time.sleep(0.08)
    window.after(0,play_gif(image_path))

def exit_fnc():
    window.destroy()


# tk.Button(window,text="play", command=main_fnc).place(x=500,y = 300)
btn_play = tk.Button(window,text="Navidad Empieza", command=lambda: play_gif(duendes_img)).place(x=500,y = 300)
btn_exit = tk.Button(window,text = "Salir", command=exit_fnc).place (x = 450,y= 300)
if __name__ == '__main__':
    semaf_principal.release()
    # main_fnc()
    
    window.mainloop()