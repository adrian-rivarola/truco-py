from Diccionarios import diccJugadores,diccEnvido,diccTruco
from Jugador import Humano, Cpu
from Carta import Carta
import random
import time
import os

class Juego:
	"""
	Esta clase se encarga de controlar toda la logica y las funciones del Juego.
	Por defecto, crea un jugador Humano y uno controlado por la CPU.
	"""
	def __init__(self):
		
		self.jugadores = [Humano(0), Cpu(1)]
		self.puntos = [0,0]
		self.mano = random.choice([0,1])

	def info(self):
		"""
		Imprime el resultado parcial del juego.
		"""
		os.system('clear')
		print('-----------------')
		for i in range(2):
			print('{}: {} puntos'.format(diccJugadores[i], self.puntos[i]))
		print('-----------------')

	def repartir(self):
		"""
		Es ejecutado al comienzo de cada mano, crea una mazo de cartas, lo mezcla y reparte 3 cartas a cada jugador.
		Tambien resetea todas las variables utilizadas durante el desarrollo de la mano.
		"""
		for jug in self.jugadores:
			jug.cartas = []

		mazo = [Carta(n,p) for n in [1,2,3,4,5,6,7,10,11,12] for p in ["Espada","Oro","Basto","Copa"]]
		random.shuffle(mazo)

		for i in range(3):
			for jugador in self.jugadores:
				jugador.addCarta(mazo.pop())
		
		self.ronda = 1
		self.mano = 1 - self.mano
		self.turno = self.mano
		self.truco = 1
		self.envido = 0
		self.palabraTruco = [0,1]
		self.ganadores = [None, None, None]
		self.cartasJugadas = [None,None]
		self.ganadorMano = None
		
	
	def pedirTruco(self, ident):
		"""
		Recibe por parametro el identificador del jugador que pide Truco, y pide una respuesta(1,2 o 3) al otro jugador.
		En caso de que la respuesta sea 3, esta funcion se llama a si misma, cambiando el identificador.
		"""
		print('-----------------')
		print('{}: {}'.format(diccJugadores[ident], diccTruco[self.truco]))
		
		respuesta = self.jugadores[1-ident].responderTruco(self)
		
		if respuesta == 2:
			self.ganadorMano = ident
			print('{}: No quiero'.format(diccJugadores[1-ident]))
		
		elif respuesta == 1:
			self.truco += 1
			self.palabraTruco = [1-ident] if self.truco < 3 else []
			print('{}: Quiero'.format(diccJugadores[1-ident]))
		
		elif respuesta == 3 and self.truco < 3:
			self.truco += 1
			self.palabraTruco = [ident] if self.truco < 3 else []
			self.pedirTruco(1-ident)

	def pedirEnvido(self, ident, env):
		"""
		Recibe el identificador del jugador que pide el Envido, y el numero de envido segun el diccionario(0-4).
		La respuesta puede ser: 0 para rechazar, 1 para aceptar, 2-4 para cantar otro Envido.
		"""
		print('-----------------')
		print('{}: {}'.format(diccJugadores[ident], diccEnvido[env]))

		respuesta = self.jugadores[1-ident].responderEnvido(env)
		
		print('{}: {}'.format(diccJugadores[1-ident], diccEnvido[respuesta]))
		print('-----------------')
		
		if respuesta == 0:
			self.envido += 1
			self.puntos[ident] += self.envido

		elif respuesta == 1:
			self.envidoAceptado(env)
			self.ganadorEnvido()
		
		elif respuesta < 5:
			self.envidoAceptado(env)
			self.pedirEnvido(1-ident, respuesta)

		elif respuesta == 5:
			self.pedirFlor(1-ident)

	def envidoAceptado(self,env):
		"""
		Calcula cuantos puntos se deben asignar al ganador del Envido.
		Puede ser: envido(2), real envido(3), falta envido, o una combinacion de estos.
		"""
		if env < 4:
				self.envido += env
		else:
				if max(self.puntos) < 9:
					self.envido = 9-max(self.puntos)
				else:
					self.envido = 18-max(self.puntos)

	def pedirFlor(self, ident):
		"""
		Recibe el identificador del jugador con Flor. 
		Si el oponente tambien cuenta con flor, el que tenga mayor tanto se lleva 3 puntos.
		Funciones de Contra Flor y Contra Flor al resto aun no han sido implementadas.
		"""
		print('-----------------')
		print('{}: Flor'.format(diccJugadores[ident]))
		
		if self.jugadores[1-ident].flor:
			self.envido = 3
			self.ganadorEnvido()
		else:
			self.puntos[ident] += 3

	def ganadorEnvido(self):
		"""
		Determina cual jugador posee el tanto mas alto, y le asigna los puntos correspondientes.
		"""
		print('-----------------')
		print('{}: {}'.format(diccJugadores[self.mano], self.jugadores[self.mano].tanto))
		
		if self.jugadores[1-self.mano] > self.jugadores[self.mano]:
			print('{}: {} son mejores'.format(diccJugadores[1-self.mano], self.jugadores[1-self.mano].tanto))
			ganadorE = 1-self.mano
		else:
			print('{}: Son buenas'.format(diccJugadores[1-self.mano]))
			ganadorE = self.mano
		print('-----------------')

		self.puntos[ganadorE] += self.envido
		time.sleep(2)

	def jugarRonda(self):
		"""
		Llama a la funcion jugar() de cada jugador, comprueba que se hayan jugado cartas o si hay una ganador.
		"""
		os.system('clear')
		print('------------------')
		print('-    Ronda {}     -'.format(self.ronda))
		print('------------------')
		
		self.jugadores[self.turno].jugar(self)
		
		if self.cartasJugadas[0] or self.cartasJugadas[1]:
			self.jugadores[1-self.turno].jugar(self)

		if self.cartasJugadas[1] and self.cartasJugadas[0] and not self.ganadorMano:
			self.ganadorRonda()

		self.ronda += 1
		self.cartasJugadas = [None, None]
		if self.ganadorMano:
			self.puntos[self.ganadorMano] += self.truco

		time.sleep(3)

	def ganadorRonda(self):
		"""
		El jugador que haya jugado la carta mas fuerte es el ganador de la ronda.
		Un jugador debe ganar dos Rondas para ganar la Mano.
		En caso de que haiga 1 o 2 empates, el ganador de la siguiente ronda gana la Mano.
		En caso de que haigan 3 empates el jugador que haya tirado la primera carta gana la Mano.
		"""
		if self.cartasJugadas[0] > self.cartasJugadas[1]:
			self.turno = 0
			self.ganadores[self.ronda-1] = 0

		elif self.cartasJugadas[1] > self.cartasJugadas[0]:
			self.turno = 1
			self.ganadores[self.ronda-1] = 1
		
		else:
			print('Resultado: Empate')
			self.turno = self.mano
			self.ganadores[self.ronda-1] = 'Empate'

			if self.ronda == 2:
				self.ganadorMano = self.ganadores[0] if self.ganadores[0] != 'Empate' else None
				return

			elif self.ronda == 3:
				self.ganadorMano = self.ganadores[0] if self.ganadores[0] != 'Empate' else self.mano
				return

		if self.ronda == 1: return
		
		else:
			if self.ganadores.count(self.turno) > 1 or self.ganadores.count('Empate') > 1:
				self.ganadorMano = self.turno
