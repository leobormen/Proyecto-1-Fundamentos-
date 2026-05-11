# main.py (MicroPython)
import network
import socket
import time
from machine import Pin


SSID = "Leo" #No debe tener caracteres especiales
PASSWORD = "l3575592l"

Morse_diccionario = {"a": [0, 2, 1], "b": [1, 2, 0, 2, 0, 2, 0], "c": [1, 2, 0, 2, 1, 2, 0], "d": [1, 2, 0, 2, 0], "e": [0], "f": [0, 2, 0, 2, 1, 2, 0],
         "g": [1, 2, 1, 2, 0], "h": [0, 2, 0, 2, 0, 2, 0], "i": [0, 2, 0], "j": [0, 2, 1, 2, 1, 2, 1], "k": [1, 2, 0, 2, 1], "l": [0, 2, 1, 2, 0, 2, 0], 
         "m": [1, 2, 1], "n": [1, 2, 0], "ñ": [1, 2, 1, 2, 0, 2, 1, 2, 1], "o": [1, 2, 1, 2, 1],"p": [0, 2, 1, 2, 1, 2, 0], "q": [1, 2, 1, 2, 0, 2, 1], 
         "r": [0, 2, 1, 2, 0], "s": [0, 2, 0, 2, 0], "t": [1], "u": [0, 2, 0, 2, 1], "v": [0, 2, 0, 2, 0, 2, 1], "w": [0, 2, 1, 2, 1], "x": [1, 2, 0, 2, 0, 2, 1], 
         "y": [1, 2, 0, 2, 1, 2, 1], "z": [1, 2, 1, 2, 0, 2, 0], "0": [1, 2, 1, 2, 1, 2, 1, 2, 1], "1": [0, 2, 1, 2, 1, 2, 1, 2, 1], 
         "2": [0, 2, 0, 2, 1, 2, 1, 2, 1], "3": [0, 2, 0, 2, 0, 2, 1, 2, 1], "4": [0, 2, 0, 2, 0, 2, 0, 2, 1], "5": [0, 2, 0, 2, 0, 2, 0, 2, 0], 
         "6": [1, 2, 0, 2, 0, 2, 0, 2, 0], "7": [1, 2, 1, 2, 0, 2, 0, 2, 0], "8": [1, 2, 1, 2, 1, 2, 0, 2, 0], "9": [1, 2, 1, 2, 1, 2, 1, 2, 0],
         "+": [0, 2, 1, 2, 0, 2, 1, 2, 0], "-": [1, 2, 0, 2, 0, 2, 0, 2, 0, 2, 1]}

Matriz_diccionario = {"a": [1, 1, [0,0,0,0,0,0,0,1]], "b": [1, 1, [0,0,0,0,0,0,1,0]], "c": [1, 1, [0,0,0,0,0,1,0,0]], "d": [1, 1, [0,0,0,0,1,0,0,0]], "e": [1, 1, [1,0,0,0,0,0,0,0]],
                      "f": [1, 1, [0,1,0,0,0,0,0,0]], "g": [1, 1, [0,0,1,0,0,0,0,0]], "h": [1, 1, [0,0,0,1,0,0,0,0]], "i": [1, 2, [0,0,0,0,0,0,0,1]], "j": [1, 2, [0,0,0,0,0,0,1,0]],
                      "k": [1, 2, [0,0,0,0,0,1,0,0]], "l": [1, 2, [0,0,0,0,1,0,0,0]], "m": [1, 2, [0,0,1,0,0,0,0,0]], "n": [2, 1, [0,0,0,0,0,0,0,1]], "ñ": [2, 1, [0,0,0,0,0,0,1,0]],
                      "o": [2, 1, [0,0,0,0,0,1,0,0]], "p": [2, 1, [0,0,0,0,1,0,0,0]], "q": [2, 1, [1,0,0,0,0,0,0,0]], "r": [2, 1, [0,1,0,0,0,0,0,0]], "s": [2, 1, [0,0,1,0,0,0,0,0]],
                      "t": [2, 1, [0,0,0,1,0,0,0,0]], "u": [2, 2, [0,0,0,0,0,0,0,1]], "v": [2, 2, [0,0,0,0,0,0,1,0]], "w": [2, 2, [0,0,0,0,0,1,0,0]], "x": [2, 2, [0,0,0,0,1,0,0,0]],
                      "y": [2, 2, [0,0,1,0,0,0,0,0]], "z": [3, 1, [0,0,0,0,0,0,0,1]], "0": [3, 1, [0,0,0,0,0,0,1,0]], "1": [3, 1, [0,0,0,0,0,1,0,0]], "2": [3, 1, [0,0,0,0,1,0,0,0]],
                      "3": [3, 1, [1,0,0,0,0,0,0,0]], "4": [3, 1, [0,1,0,0,0,0,0,0]], "5": [3, 1, [0,0,1,0,0,0,0,0]], "6": [3, 1, [0,0,0,1,0,0,0,0]], "7": [3, 2, [0,0,0,0,0,0,0,1]],
                      "8": [3, 2, [0,0,0,0,0,0,1,0]], "9": [3, 2, [0,0,0,0,0,1,0,0]], "+": [3, 2, [0,0,0,0,1,0,0,0]], "-": [3, 2, [0,0,1,0,0,0,0,0]]}

AB1 = Pin(14, Pin.OUT)
CLK1 = Pin(12, Pin.OUT)
AB2 = Pin(15, Pin.OUT)
CLK2 = Pin(13, Pin.OUT)
led1 = Pin(19, Pin.OUT)
led2 = Pin(20, Pin.OUT)
led3 = Pin(21, Pin.OUT)
buzzer = Pin(27, Pin.OUT)
boton = Pin(28, Pin.IN, Pin.PULL_DOWN)
dip_switch = Pin(16, Pin.IN)



led1.value(0)
led2.value(0)
led3.value(0)
for x in range(8):
    AB1(0)                 
    CLK1(1)                          
    CLK1(0)
for x in range(8):
    AB2(0)                 
    CLK2(1)                          
    CLK2(0)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("Conectando a WiFi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nConectado:", wlan.ifconfig())
    return wlan.ifconfig()[0]

def pasar_a_string(lista):
    string_palabra = ""
    for x in lista:
        string_palabra += str(x)
    return string_palabra

def contar():  #Esto interpreta como el usuario presiona el boton indicado, define cual numero poner.
    lista_jugador_2 = []
    while True:
        conteo = 0
        while boton.value() == 1:
            conteo += 0.01
            time.sleep(0.01)
        if conteo <= 0.30:
            lista_jugador_2.append(0) # 0 indica dot
        elif conteo > 0.30:
            lista_jugador_2.append(1) # 1 indica dash
        conteo = 0
        while conteo <= 1:
            conteo += 0.01
            time.sleep(0.01)
            if boton.value() == 1:
                break
        if conteo <= 0.30:
            lista_jugador_2.append(2) # 2 indica espacio entre dash o dot
        elif 0.30 < conteo <= 1:
            lista_jugador_2.append(3) # 3 indica espacio entre letras
        else:
            print(lista_jugador_2)
            conn.send(pasar_a_string(lista_jugador_2))
            break

def traducir(palabra):
    palabra_morse = []
    for i in range(len(palabra)):
        if palabra[i] == " ":
            palabra_morse += [4]
        else:
            palabra_morse += Morse_diccionario[palabra[i].lower()]
        if palabra[i] != " " and i != (len(palabra)-1):
                palabra_morse += [3]
    return palabra_morse


def start_server(ip):
    global conn
    s = socket.socket()
    s.bind((ip, 1717))
    s.listen(1)
    print("Esperando conexión del cliente...")
    conn, addr = s.accept()
    print("Conectado desde:", addr)
    
    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg = list(data.decode())
        print("Mensaje recibido:", msg)
        
        print(type(msg))
        # Acciones según el mensaje
        if msg[0] == "a":
            rapidez = int(msg[1])
            msg = traducir(msg[2:])
            for x in msg:
                if int(x) == 0:
                    buzzer.value(1)
                    time.sleep(0.3/rapidez)
                if int(x) == 1:
                    buzzer.value(1)
                    time.sleep(0.9/rapidez)
                if int(x) == 2:
                    buzzer.value(0)
                    time.sleep(0.3/rapidez)
                if int(x) == 3:
                    buzzer.value(0)
                    time.sleep(0.9/rapidez)
                if int(x) == 4:
                    buzzer.value(0)
                    time.sleep(2.1/rapidez)
            buzzer.value(0)
        if msg[0] == "b":
            if dip_switch.value() == 0:
                msg = msg[1:]
                for x in msg:
                    if x == " ":
                        led1.value(0)
                        led2.value(0)
                        led3.value(0)
                        for x in range(8):
                            AB1(0)                 
                            CLK1(1)                          
                            CLK1(0)
                        for x in range(8):
                            AB2(0)                 
                            CLK2(1)                          
                            CLK2(0)
                        time.sleep(1)
                        continue
                    letra = Matriz_diccionario[x.lower()]
                    AB = 0
                    CLK = 0
                    if letra[0] == 1:
                        led1.value(1)
                        led2.value(0)
                        led3.value(0)
                    elif letra[0] == 2:
                        led1.value(0)
                        led2.value(1)
                        led3.value(0)
                    else:
                        led1.value(0)
                        led2.value(0)
                        led3.value(1)
                    if letra[1] == 1:
                        AB = AB1
                        CLK = CLK1
                    else:
                        AB = AB2
                        CLK = CLK2
                    for x in letra[2]:
                        AB(x)                 
                        CLK(1)                          
                        CLK(0)
                    time.sleep(2)
                    led1.value(0)
                    led2.value(0)
                    led3.value(0)
                    for x in range(8):
                        AB1(0)                 
                        CLK1(1)                          
                        CLK1(0)
                    for x in range(8):
                        AB2(0)                 
                        CLK2(1)                          
                        CLK2(0)
                    time.sleep(1)
            else:
                msg = traducir(msg[1:])
                for x in msg:
                    if int(x) == 0:
                        buzzer.value(1)
                        time.sleep(0.1)
                    if int(x) == 1:
                        buzzer.value(1)
                        time.sleep(0.3)
                    if int(x) == 2:
                        buzzer.value(0)
                        time.sleep(0.1)
                    if int(x) == 3:
                        buzzer.value(0)
                        time.sleep(0.3)
                    if int(x) == 4:
                        buzzer.value(0)
                        time.sleep(0.7)
                buzzer.value(0)
            while True:
                if boton.value() == 1:
                    print("Hola")
                    contar()
                    break

ip = connect_wifi()
start_server(ip)