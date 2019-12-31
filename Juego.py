from Diccionarios import diccJugadores,diccEnvido,diccTruco
from Jugador import Humano, Cpu
from Carta import Carta
import random
import time
import os

class Juego:
	"""
	Esta clase se encarga de controlar toda la lógica y las funciones del Juego.
	Crea un jugador Humano y uno controlado por la CPU.
	"""
	def __init__(self):
		self.jugadores = [Humano(0), Cpu(1)]
		self.puntos = [0,0]
		self.mano = random.choice([0,1])

	def info(self):
		""" Imprime el resultado parcial del juego. """
		clear()
		
		print("┌─────────────────────────────────────────┐")
		print("│"   +  "Puntuaciones".center(41, " ") + "│")
		print("├────────┬────────────────────────────────┤")
		print("│" + diccJugadores[0].center(8, " ") + "│" + f" {self.puntos[0]} puntos".center(32, " ") + "│")
		print("├────────┼────────────────────────────────┤")
		print("│" + diccJugadores[1].center(8, " ") + "│" + f" {self.puntos[1]} puntos".center(32, " ") + "│")
		print("└────────┴────────────────────────────────┘")

	def repartir(self):
		"""
		Es ejecutado al comienzo de cada mano, crea una mazo de cartas, lo mezcla y reparte 3 cartas a cada jugador.
		También resetea todas las variables utilizadas durante el desarrollo de la mano.
		"""
		self.ganadores, self.cartasJugadas, self.ganadorMano = [None, None, None], [None,None], None
		self.ronda = self.truco = 1
		self.palabraTruco = [0,1]
		self.mano = 1 - self.mano
		self.turno = self.mano
		self.envido = 0

		for jug in self.jugadores:
			jug.cartas = []

		mazo = [Carta(n,p) for n in [1,2,3,4,5,6,7,10,11,12] for p in ["Espada","Oro","Basto","Copa"]]
		random.shuffle(mazo)

		for i in range(1,4):
			for jugador in self.jugadores:
				clear()
				print("┌────────────────────────┐")
				print("|"+("."*i+"Repartiendo"+"."*i).center(24)+"|")
				print("└────────────────────────┘")
				
				jugador.addCarta(mazo.pop())
				
				time.sleep(.3)
	
	def pedirTruco(self, ident):
		"""
		Recibe por parámetro el identificador del jugador que pide Truco, y pide una respuesta (1,2 o 3) al otro jugador.
		"""
		print("┌────────────────────────┐")
		print("|"+f"{ diccJugadores[ident] }: { diccTruco[self.truco] }".center(24)+"|")
		print("└────────────────────────┘")

		respuesta = self.jugadores[1-ident].responderTruco(self)
		
		if respuesta == 2:
			self.ganadorMano = ident
			
			print("┌────────────────────────┐")
			print("|"+f"{ diccJugadores[1-ident] }: No quiero".center(24)+"|")
			print("└────────────────────────┘")
		
		elif respuesta == 1:
			self.truco += 1
			self.palabraTruco = [1-ident] if self.truco < 3 else []
			
			print("┌────────────────────────┐")
			print("|"+f"{ diccJugadores[1-ident] }: Quiero".center(24)+"|")
			print("└────────────────────────┘")
		
		elif respuesta == 3 and self.truco < 3:
			self.truco += 1
			self.palabraTruco = [ident] if self.truco < 3 else []

			print()
			
			self.pedirTruco(1-ident)

	def pedirEnvido(self, ident, env):
		"""
		Recibe el identificador del jugador que pide el Envido, y el número de envido según el diccionario(0-4).
		La respuesta puede ser: 0 para rechazar, 1 para aceptar, 2-4 para cantar otro Envido.
		"""
		
		print("┌────────────────────────┐")
		print("|"+f"{ diccJugadores[ident] }: { diccEnvido[env] }".center(24)+"|")
		print("├────────────────────────┤")

		respuesta = self.jugadores[1-ident].responderEnvido(env)
		
		if respuesta < 2:
			if ident == 1: print("┌────────────────────────┐")
			print("|"+f"{ diccJugadores[1-ident] }: { diccEnvido[respuesta] }".center(24)+"|")
			print("└────────────────────────┘")

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
		Calcula cuántos puntos se deben asignar al ganador del Envido.
		Puede ser: envido(2), real envido(3), falta envido, o una combinación de estos.
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
		Si el oponente también tiene flor, el que tenga mayor tanto se lleva 3 puntos.
		Funciones de Contra Flor y Contra Flor al resto aún no han sido implementadas.
		"""
		print("┌────────────────────────┐")
		print("|"+f"{ diccJugadores[ident] }: Flor".center(24)+"|")
		print("└────────────────────────┘")
		
		if self.jugadores[1-ident].flor:
			self.envido = 3
			self.ganadorEnvido()
		else:
			self.puntos[ident] += 3
			self.envido = 3

	def ganadorEnvido(self):
		""" Determina cual jugador posee el tanto más alto, y le asigna los puntos correspondientes. """
		print("┌────────────────────────┐")
		print("|"+f"{ diccJugadores[self.mano] }: { self.jugadores[self.mano].tanto }".center(24)+"|")
		print("├────────────────────────┤")		
		
		if self.jugadores[1-self.mano] > self.jugadores[self.mano]:
			print("|"+f"{ diccJugadores[1-self.mano] }: { self.jugadores[1-self.mano].tanto } son mejores".center(24)+"|")
			ganadorE = 1-self.mano
		else:
			print("|"+f"{ diccJugadores[1-self.mano] }: Son buenas".center(24)+"|")
			ganadorE = self.mano

		print("└────────────────────────┘")
		self.puntos[ganadorE] += self.envido

	def jugarRonda(self):
		""" Llama al método jugar() de cada jugador, comprueba que se haya jugado una carta o si hay un ganador. """
		clear()
		
		print("┌────────────────────────┐")
		print("│                        │")
		print(f"│        Ronda {self.ronda}         │")
		print("│                        │")
		print("└────────────────────────┘")
		
		self.jugadores[self.turno].jugar(self)
		
		if self.ganadorMano not in [0,1]:
			self.jugadores[1-self.turno].jugar(self)

		if all(self.cartasJugadas) and self.ganadorMano not in [0,1]:
			self.ganadorRonda()

		self.ronda += 1
		self.cartasJugadas = [None, None]
		
		if self.ganadorMano in [0,1]:
			self.puntos[self.ganadorMano] += self.truco

		time.sleep(3)

	def ganadorRonda(self):
		"""
		El jugador que haya jugado la carta más fuerte es el ganador de la ronda.
		Un jugador debe ganar dos Rondas para ganar la Mano.
		En caso de que haya 1 o 2 empates, el ganador de la siguiente ronda gana la Mano.
		En caso de que hayan 3 empates el jugador que haya tirado la primera carta gana la Mano.
		"""
		if self.cartasJugadas[0] > self.cartasJugadas[1]:
			self.turno = 0
			self.ganadores[self.ronda-1] = 0

		elif self.cartasJugadas[1] > self.cartasJugadas[0]:
			self.turno = 1
			self.ganadores[self.ronda-1] = 1
		
		else:
			self.turno = self.mano
			self.ganadores[self.ronda-1] = 'Empate'

			if self.ronda == 2:
				self.ganadorMano = self.ganadores[0] if self.ganadores[0] != 'Empate' else None
				return

			elif self.ronda == 3:
				self.ganadorMano = self.ganadores[0] if self.ganadores[0] != 'Empate' else self.mano
				return

		if self.ronda == 1: return
		
		elif self.ganadores.count(self.turno) > 1 or self.ganadores.count('Empate') > 0:
				self.ganadorMano = self.turno

	def jugar(self):
		clear()
		
		print("┌──────────────────────────┐")
		print("│                          │")
		print("│       TRUCO - PY         │")
		print("│                          │")
		print("├──────────────────────────┤")
		print("│   Jugar hasta:           │")
		print("├──────────────────────────┤")
		print("│ 1. 18 puntos             │")
		print("├──────────────────────────┤")
		print("│ 2. 9  puntos             │")
		print("└──────────────────────────┘")

		while 1:
			inp = input("> ")
			if inp == "1":
				max_puntos = 18
				break
			elif inp == "2":
				max_puntos = 9
				break

		while max(self.puntos) < max_puntos:
			self.repartir()
			
			while self.ganadorMano not in [0,1]:
				self.jugarRonda()

			self.info()
			pausa()

juego = Juego()

if os.name == "nt":
	pausa = lambda : os.system("pause")
	clear = lambda : os.system("cls")
else:
	pausa = lambda : input("Presione Enter para continuar . . .")
	clear = lambda : os.system("clear")