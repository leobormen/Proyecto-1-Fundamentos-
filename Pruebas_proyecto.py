import tkinter as tk
from tkinter import *
import keyboard
import time
import random
import socket
import threading

SERVER_IP = "10.165.83.130"  # Cambia esto con la IP de la Pico W
PORT = 1717

Morse_diccionario = {"a": [0, 2, 1], "b": [1, 2, 0, 2, 0, 2, 0], "c": [1, 2, 0, 2, 1, 2, 0], "d": [1, 2, 0, 2, 0], "e": [0], "f": [0, 2, 0, 2, 1, 2, 0],
         "g": [1, 2, 1, 2, 0], "h": [0, 2, 0, 2, 0, 2, 0], "i": [0, 2, 0], "j": [0, 2, 1, 2, 1, 2, 1], "k": [1, 2, 0, 2, 1], "l": [0, 2, 1, 2, 0, 2, 0], 
         "m": [1, 2, 1], "n": [1, 2, 0], "ñ": [1, 2, 1, 2, 0, 2, 1, 2, 1], "o": [1, 2, 1, 2, 1],"p": [0, 2, 1, 2, 1, 2, 0], "q": [1, 2, 1, 2, 0, 2, 1], 
         "r": [0, 2, 1, 2, 0], "s": [0, 2, 0, 2, 0], "t": [1], "u": [0, 2, 0, 2, 1], "v": [0, 2, 0, 2, 0, 2, 1], "w": [0, 2, 1, 2, 1], "x": [1, 2, 0, 2, 0, 2, 1], 
         "y": [1, 2, 0, 2, 1, 2, 1], "z": [1, 2, 1, 2, 0, 2, 0], "0": [1, 2, 1, 2, 1, 2, 1, 2, 1], "1": [0, 2, 1, 2, 1, 2, 1, 2, 1], 
         "2": [0, 2, 0, 2, 1, 2, 1, 2, 1], "3": [0, 2, 0, 2, 0, 2, 1, 2, 1], "4": [0, 2, 0, 2, 0, 2, 0, 2, 1], "5": [0, 2, 0, 2, 0, 2, 0, 2, 0], 
         "6": [1, 2, 0, 2, 0, 2, 0, 2, 0], "7": [1, 2, 1, 2, 0, 2, 0, 2, 0], "8": [1, 2, 1, 2, 1, 2, 0, 2, 0], "9": [1, 2, 1, 2, 1, 2, 1, 2, 0],
         "+": [0, 2, 1, 2, 0, 2, 1, 2, 0], "-": [1, 2, 0, 2, 0, 2, 0, 2, 0, 2, 1]}


puntajes = []

with open("puntajes.txt", "r") as file:
    puntajes_str = file.read()
    puntajes = puntajes_str.split(",")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    try:
        client_socket.connect((SERVER_IP, PORT))
        threading.Thread(target=receive_messages, daemon=True).start()
        status_label.config(text="Conectado al servidor")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

def receive_messages():
    global puntaje2
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            puntaje2 += finalizar(list(msg))
            print(puntaje2)
            Puntaje2_Label["text"] = finalizar(list(msg)), "/", len(palabra_morse)
            if rondas == 3:
                finalizar_juego2.place(y=350, x=200)
            else:
                ronda_siguiente_juego2.place(y=350,x=200)
        except:
            break

def puntaje():
    for i in range(len(puntajes)):
        if puntaje_juego1 > int(puntajes[i]):
            print("holaaa")
            record_label.place(x=300, y=300)
            puntajes.insert(i,str(puntaje_juego1))
            puntajes.pop()
            puntajes_str = (puntajes[0] + "," + puntajes[1] + "," + puntajes[2] + "," + puntajes[3] + "," + puntajes[4] + "," 
                            + puntajes[5] + "," + puntajes[6] + "," + puntajes[7] + "," + puntajes[8] + "," + puntajes[9])
            with open("puntajes.txt", "w") as archivo:
                archivo.write(puntajes_str)
            break

def ver_puntuaciones():
    window_main.place_forget()
    puntuacion1_label["text"] = puntajes[0]
    puntuacion2_label["text"] = puntajes[1]
    puntuacion3_label["text"] = puntajes[2]
    puntuacion4_label["text"] = puntajes[3]
    puntuacion5_label["text"] = puntajes[4]
    puntuacion6_label["text"] = puntajes[5]
    puntuacion7_label["text"] = puntajes[6]
    puntuacion8_label["text"] = puntajes[7]
    puntuacion9_label["text"] = puntajes[8]
    puntuacion10_label["text"] = puntajes[9]
    window_puntuaciones.place(x=0,y=0)

def menu():
    finalizar_juego1.place_forget()
    finalizar_juego2.place_forget()
    window_puntuaciones.place_forget()
    window_juego_1.place_forget()
    window_juego_2.place_forget()
    window_main.place(x=0,y=0)

def salir():
    try:
        client_socket.close()
    except:
        pass
    window.destroy()

def traducir(palabra):
    global palabra_morse
    for i in range(len(palabra)):
        if palabra[i] == " ":
            palabra_morse += [4]
        else:
            palabra_morse += Morse_diccionario[palabra[i].lower()]
        if palabra[i] != " " and i != (len(palabra)-1):
                palabra_morse += [3]
    print(palabra_morse)

def comparar_entrada():
    global palabra_elegida
    global puntaje_juego1
    Palabra_respuesta = Respuesta.get()
    for i in range(len(Palabra_respuesta[:len(palabra_elegida)])):
        if Palabra_respuesta[i].lower() == palabra_elegida[i].lower():
            puntaje_juego1 += 1
    Puntaje_juego1_Label["text"] = ("Puntaje: ", puntaje_juego1)
    if rondas == 3:
        puntaje()
        finalizar_juego1.place(y=350, x=200)
    else:
        ronda_siguiente_juego1.place(y=350,x=200)

def siguiente_ronda_juego2():
    global palabra_elegida
    global rondas
    rondas += 1
    ronda_siguiente_juego2.place_forget()
    palabra_morse.clear()
    Texto_puntaje["text"] = ""
    Puntaje1_Label["text"] = ""
    Puntaje2_Label["text"] = ""
    palabra_elegida = Lista_palabras[random.randint(0,9)]
    traducir(palabra_elegida)
    msg = "b" + pasar_a_string(palabra_elegida)
    print(msg)
    if msg:
        client_socket.send(msg.encode())

def siguiente_ronda_juego1():
    global palabra_elegida
    global rondas
    rondas += 1
    ronda_siguiente_juego1.place_forget()
    Respuesta.delete(0, tk.END)
    palabra_morse.clear()
    palabra_elegida = Lista_palabras[random.randint(0,9)]
    traducir(palabra_elegida)
    msg = "a" + str(rondas) + pasar_a_string(palabra_elegida)
    print(msg)
    if msg:
        client_socket.send(msg.encode())

def finalizar(lista):  #Finaliza la interpretacion
    puntaje = 0
    print(lista) 
    for i in range (len(palabra_morse[:len(lista)])): # Verifica que tan correcto está el input del jugador, notar que se corta la lista prehecha para acomodar a cuanto puso el usuario
        if palabra_morse[i] == int(lista[i]):
            puntaje += 1
    print(puntaje)
    Texto_puntaje["text"] = "Tu puntaje es"
    return puntaje
    
def contar():  #Esto interpreta como el usuario presiona el boton indicado, define cual numero poner.
    conteo = 0
    global Puntaje1_Label
    global puntaje1
    while keyboard.is_pressed("space"):
        conteo += 0.01
        time.sleep(0.01)
    if conteo <= 0.30:
        lista_jugador_1.append(0) # 0 indica dot
    elif conteo > 0.30:
        lista_jugador_1.append(1) # 1 indica dash
    conteo = 0
    while conteo <= 1:
        conteo += 0.01
        time.sleep(0.01)
        if keyboard.is_pressed("space"):
            break
    if conteo <= 0.30:
        lista_jugador_1.append(2) # 2 indica espacio entre dash o dot
    elif 0.30 < conteo <= 0.70:
        lista_jugador_1.append(3) # 3 indica espacio entre letras
    elif 0.70 < conteo <= 1:
        lista_jugador_1.append(4) # 4 indica espacio entre palabras
    else:
        puntaje1 += finalizar(lista_jugador_1)
        Puntaje1_Label["text"] = finalizar(lista_jugador_1), "/", len(palabra_morse)
        lista_jugador_1.clear()
        ronda_siguiente_juego2.place(y=350,x=200)

def pasar_a_string(lista):
    string_palabra = ""
    for x in lista:
        string_palabra += str(x)
    return string_palabra

def empezar_juego_1():
    global palabra_elegida
    global puntaje_juego1
    global palabra_morse
    global rondas
    rondas = 1
    window_main.place_forget()
    record_label.place_forget()
    window_juego_1.place(x=0,y=0)
    Respuesta.delete(0, tk.END)
    puntaje_juego1 = 0
    palabra_morse.clear()
    palabra_elegida = Lista_palabras[random.randint(0,9)]
    traducir(palabra_elegida)
    msg = "a" + str(rondas) + pasar_a_string(palabra_elegida)
    print(msg)
    if msg:
        client_socket.send(msg.encode())
    
def empezar_juego_2():
    global palabra_elegida
    global puntaje1
    global puntaje2
    global palabra_morse
    global rondas
    rondas = 1
    Texto_puntaje["text"] = ""
    Puntaje1_Label["text"] = ""
    Puntaje2_Label["text"] = ""
    window_juego_2.place(x=0,y=0)
    puntaje2 = 0
    puntaje1 = 0
    palabra_morse.clear()
    palabra_elegida = Lista_palabras[random.randint(0,9)]
    traducir(palabra_elegida)
    msg = "b" + pasar_a_string(palabra_elegida)
    if msg:
        client_socket.send(msg.encode())


Lista_palabras = ["mn1","mn1","mn1","mn1","mn1","mn1","mn1","mn1","mn1","mn1"]


palabra_morse= []
lista_jugador_1 = []
puntaje_juego1 = 0
puntaje1 = 0
puntaje2 = 0
puntaje_total_1 = 0
puntaje_total_2 = 0
rondas = 1

#--------------------------------Parte principal de la interfaz-----------------------------

window = tk.Tk()
window.geometry("400x400")

window_main = tk.Canvas(window, height= 400, width= 400)
window_main.place(x=0,y=0)

boton_juego1 = tk.Button(window_main, text= "iniciar juego 1", command= empezar_juego_1)
boton_juego1.place(x= 200, y= 0)

boton_juego2 = tk.Button(window_main, text= "iniciar juego 2", command= empezar_juego_2)
boton_juego2.place(x= 100, y= 0)

boton_puntuaciones = tk.Button(window_main, text= "Mejores puntuaciones", command= ver_puntuaciones)
boton_puntuaciones.place(x= 100, y= 200)

#----------------------------------Ventana del juego 2----------------------------------------

window_juego_2 = tk.Canvas(window, width=400,height=400)

Texto_puntaje = tk.Label(window_juego_2, text="")
Texto_puntaje.place(x= 100, y= 150)

Puntaje1_Label = tk.Label(window_juego_2, text= "hola")
Puntaje1_Label.place(x= 200, y= 225)

Puntaje2_Label = tk.Label(window_juego_2, text= "hola")
Puntaje2_Label.place(x= 300, y= 225)

status_label = tk.Label(window_main, text="Desconectado")
status_label.place(x= 100, y= 300)

salir_btn = tk.Button(window_main, text="Salir", command=salir)
salir_btn.place(x= 100, y= 350)

ronda_siguiente_juego2 = tk.Button(window_juego_2, text= "Siguiente ronda", command=siguiente_ronda_juego2)
finalizar_juego2 = tk.Button(window_juego_2, text= "Finalizar", command=menu)

#-----------------------------------Ventana del juego 1------------------------------------

window_juego_1 = tk.Canvas(window, height=400, width=400)

Respuesta = tk.Entry(window_juego_1)
Respuesta.place(x=10,y=150)

boton_respuesta = tk.Button(window_juego_1, text= "Confirmar", command=comparar_entrada)
boton_respuesta.place(x=200, y= 250)

ronda_siguiente_juego1 = tk.Button(window_juego_1, text= "Siguiente ronda", command=siguiente_ronda_juego1)
finalizar_juego1 = tk.Button(window_juego_1, text= "Finalizar", command=menu)

Puntaje_juego1_Label = tk.Label(window_juego_1, text= "")
Puntaje_juego1_Label.place(x=200,y=300)

record_label = tk.Label(window_juego_1, text= "¡Nuevo record!")

#---------------------------------Ventana de puntuaciones---------------------------------------------------------------

window_puntuaciones = tk.Canvas(window, height=400, width=400)

puntuacion_label = tk.Label(window_puntuaciones, text="Los mejores puntajes son:")
puntuacion_label.place(x= 150, y= 10)
puntuacion1_label = tk.Label(window_puntuaciones, text="", width= 32)
puntuacion1_label.place(x=150, y= 40)
puntuacion2_label = tk.Label(window_puntuaciones, text="", width= 32)
puntuacion2_label.place(x=150, y= 70)
puntuacion3_label = tk.Label(window_puntuaciones, text="", width= 32)
puntuacion3_label.place(x=150, y= 100)
puntuacion4_label = tk.Label(window_puntuaciones, text="", width= 32)
puntuacion4_label.place(x=150, y= 130)
puntuacion5_label = tk.Label(window_puntuaciones, text="", width= 32)
puntuacion5_label.place(x=150, y= 160)
puntuacion6_label = tk.Label(window_puntuaciones, text="", width= 32)
puntuacion6_label.place(x=150, y= 190)
puntuacion7_label = tk.Label(window_puntuaciones, text="", width= 32)
puntuacion7_label.place(x=150, y= 220)
puntuacion8_label = tk.Label(window_puntuaciones, text="", width= 32)
puntuacion8_label.place(x=150, y= 250)
puntuacion9_label = tk.Label(window_puntuaciones, text="", width= 32)
puntuacion9_label.place(x=150, y= 280)
puntuacion10_label = tk.Label(window_puntuaciones, text="", width= 32)
puntuacion10_label.place(x=150, y= 310)

boton_menu = tk.Button(window_puntuaciones, text="Menú", command=menu)
boton_menu.place(x=10, y= 10)


keyboard.add_hotkey('space', contar)


connect()
window.mainloop()   