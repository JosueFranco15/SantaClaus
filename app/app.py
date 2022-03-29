import threading
import time, random
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue") 

window = customtkinter.CTk()
window.title("Problema Santa Claus en Py 🎄🎅🏽🎁")
window.geometry("1200x900")

santa_img = ImageTk.PhotoImage(Image.open('img/santa.jpg').resize((400, 400)))
trineo_img = ImageTk.PhotoImage(Image.open('img/trineo.jpg').resize((400, 400)))
santa_duendes_img = ImageTk.PhotoImage(Image.open('img/santa_duendes.jpg').resize((400, 400)))

renos_img = ImageTk.PhotoImage(Image.open('img/back_ground.jpg').resize((400, 400)))
duendes_img = ImageTk.PhotoImage(Image.open('img/back_ground.jpg').resize((400, 400)))



duendes_canv = tk.Canvas(window, width=400, height=400, bg="black")
duendes_canv.create_image(5,5, anchor=tk.NW, image=duendes_img) 
duendes_canv.grid(row= 0, column= 0)

renos_canv = tk.Canvas(window, width=400, height=400, bg="black")
renos_canv.create_image(5,5, anchor=tk.NW, image=renos_img) 
renos_canv.grid(row= 0, column= 2)

# Etiquetas graficas de mensajes
duendes_cont = tk.StringVar()
renos_cont = tk.StringVar()
duendes_msg = tk.StringVar()
renos_msg = tk.StringVar()

duende_lb = tk.Label(window, textvariable = duendes_cont, font= ("Arial", 16)).grid(row = 1, column = 0)
duendes_msg_lb = tk.Label(window, textvariable = duendes_msg, font= ("Arial", 16)).grid(row = 3, column = 1)
renos_msg_lb = tk.Label(window, textvariable = renos_msg, font= ("Arial", 16)).grid(row = 4, column = 1)
reno_lb = tk.Label(window, textvariable = renos_cont, font= ("Arial", 16)).grid(row = 1, column = 2)

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
    global window
    #? Semáforo para esperar cuando santa esta ayudando a otro grupo de duendes
    duendes_help_semaf.acquire()
    semaf_principal.acquire()
    duendes +=1
    time.sleep(random.randint(1,4))

    duendes_img = ImageTk.PhotoImage(Image.open(f'img/duende{duendes}.jpg').resize((400, 400)))
    duendes_canv = tk.Canvas(window, width=400, height=400, bg="black")
    duendes_canv.create_image(5,5, anchor=tk.NW, image=duendes_img) 
    duendes_canv.grid(row= 0, column= 0)
    duendes_cont.set(f"Hay {duendes} duende(s) trabajando")
    
    if duendes == 3:
        santa_semaf.release()
        duendes_msg.set(f"Duendes: Santa viene a ayudarnos")
    else:
        duendes_msg.set(f"Duendes: Necesitamos otro duende")
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
    duendes_msg.set('Santa claus ayudando...')
    time.sleep(random.randint(1,3))
    duendes_msg.set('Grupo de duendes ayudados')


#+ ----------------- Renos ------------------------------------------------
def vacaciones():
    time.sleep(random.randint(7,10))

def reno_fnc():
    global renos
    global window
    global renos_img

    vacaciones()
    semaf_principal.acquire()
    renos += 1
    time.sleep(random.randint(2,5))

    renos_cont.set(f"Hay {renos} reno(s) en el establo")
    renos_msg.set(f'Llegó el reno {nombres_renos[renos-1]}')

    renos_img = ImageTk.PhotoImage(Image.open(f'img/reno{renos}.jpg').resize((400, 400)))
    renos_canv = tk.Canvas(window, width=400, height=400, bg="black")
    renos_canv.create_image(5,5, anchor=tk.NW, image=renos_img) 
    renos_canv.grid(row= 0, column= 2)

    if renos == 7:
        renos_msg.set('Renos: Ya estamos los 7 renos, hablenle a Santa!!')
        santa_semaf.release()
    else:
        print('\n')
    semaf_principal.release()
    renos_semaf.acquire()
    enganchar_trineo()

def enganchar_trineo():
    renos_msg.set('Renos enganchando trineo...')
    time.sleep(random.randint(1,3))
    renos_msg.set('Renos listos!')
    time.sleep(random.randint(1,2))
    renos_msg.set('¡Repartiendo juguetes...!')
#+ -----------------------------------------------------------------------

#! --------------------- Santa Claus -------------------------------------
def santa_fnc():
    global renos
    global duendes
    global total_renos
    global total_duendes_ayudados
    global santa_img
    global trineo_img
    global santa_gui
    
    while True:
        santa_semaf.acquire()
        semaf_principal.acquire()
        if renos == total_renos:
            preparar_trineo()
            renos = 0
            for _ in range(total_renos):
                renos_semaf.release()
        else:
            if duendes == total_duendes_ayudados:
                ayudar_duendes()
                duendes = 0
                for _ in range(total_duendes_ayudados):
                    duendes_semaf.release()
        semaf_principal.release()

def ayudar_duendes():
    global santa_duendes_img
    print('Santa esta ayudando a duendes...')
    santa_gui.create_image(10,10, anchor=tk.NW, image=santa_duendes_img) 
    time.sleep(random.randint(1,2))

def preparar_trineo():
    global trineo_img
    print('Santa esta preparando el trineo...')
    time.sleep(random.randint(1,3))
    print('El trineo está listo!')
    time.sleep(1)
    santa_gui.create_image(10,10, anchor=tk.NW, image=trineo_img) 
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

def exit_fnc():
    window.destroy()

def iniciar():
    main_thread = threading.Thread(target=main_fnc)
    main_thread.start()

btn_play = customtkinter.CTkButton(master=window, text="Navidad Empieza", command=iniciar)
btn_exit = customtkinter.CTkButton(master=window, text="Salir", compound="right", fg_color="#D35B58", hover_color="#C77C78",command=exit_fnc)

santa_gui = tk.Canvas(window, width=400, height=400, bg="black")
santa_gui.create_image(5,5, anchor=tk.NW, image=santa_img) 
santa_gui.grid(row= 0, column= 1)

btn_play.grid(row= 5, column= 0)
btn_exit.grid(row=5, column= 2)
if __name__ == '__main__':
    semaf_principal.release()
    window.mainloop()