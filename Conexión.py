# main.py (MicroPython)
import network
import socket
import time
from machine import Pin


SSID = "Leo" #No debe tener caracteres especiales
PASSWORD = "l3575592l"



buzzer = Pin(15, Pin.OUT)
boton = Pin(14, Pin.IN)

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