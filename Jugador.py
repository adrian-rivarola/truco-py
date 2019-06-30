from Diccionarios import diccJugadores,diccEnvido,diccTruco
import random

class Jugador:
	def __init__(self, ident):
		self.ident = ident
		self. cartas = []

	def __gt__(self, jugador):
		return self.tanto > jugador.tanto

	def addCarta(self,carta):
		self.cartas.append(carta)
		if len(self.cartas) == 3:
			self.ordenarCartas()

	def ordenarCartas(self):
		"""Ordena las cartas de más débiles a más fuertes, comprueba si el jugador tiene Flor, y calcula el tanto."""
		self.cartas.sort()
		self.flor = self.cartas[0]==self.cartas[1] and self.cartas[1]==self.cartas[2]
		self.calcularTanto()
	
	def calcularTanto(self):
		"""Calcula el tanto si hay flor o dos cartas del mismo palo, de lo contrario retorna la carta mas alta."""
		if self.flor:
			self.tanto = self.cartas[0] + self.cartas[1] + self.cartas[2].valorE + 20
		else:
			if self.cartas[0] == self.cartas[1]:
				self.tanto = self.cartas[0] + self.cartas[1] + 20

			elif self.cartas[0] == self.cartas[2]:
				self.tanto = self.cartas[0] + self.cartas[2] + 20

			elif self.cartas[1] == self.cartas[2]:
				self.tanto = self.cartas[1] + self.cartas[2] + 20

			else:
				self.tanto = self.cartas[0].valorE
				for cart in self.cartas[1:]:
					if cart.valorE > self.tanto:
						self.tanto = cart.valorE

class Humano(Jugador):

	def responderTruco(self, juego):
		print('---------------')
		print(' 1. Quiero\n 2. No quiero')
		try:
			print(f' 3. { diccTruco[juego.truco+1] }')
		except: pass
		
		while 1:
			try: inp = int(input('> '))
			except ValueError: continue
			if inp in range(1,4): break

		return inp if inp in range(1,4) else 2

	def responderEnvido(self, env):
		""" Retorna 0 para aceptar, 1 para rechazar, o bien una opcion de Envido(segun el diccionario) """
		if env == 2: env = 1
		print('---------------')
		print(f'Tanto: { self.tanto }')
		print('1. No quiero\n2. Quiero')
		
		for i in range(env+1,5):
			print(f'{ i+1 }. { diccEnvido[i] }')
		
		if self.flor:
			print('6. Flor')

		while 1:
			try: inp = int(input('> '))
			except ValueError: continue
			if inp in range(1,6): break
		
		return inp-1
		#Retorna el numero ingresado por el usuario menos uno, ya que en pantalla las opciones se enumeran del 1 al 5-6.

	def pedirEnvido(self, juego):
		"""Retorna el numero de envido a pedir(segun el diccionario)."""
		print('---------------')
		for i in range(2,5):
			print(f'{ i-1 }. { diccEnvido[i] }')
		
		while 1:
			try: inp = int(input('> '))
			except ValueError: continue
			if inp in range(1,5): break

		juego.pedirEnvido(self.ident, inp+1) 
		#El dicc Envido empieza en 2, por lo que se añade 1 al input del usuario.

	def jugar(self, juego):
		"""
		Muestra en pantalla todas las opciones que el usuario puede jugar, y las almacena en un diccionario.
		El usuario ingresa el numero de la opcion a jugar, y el metodo de esta opcion es ejecutado
		"""
		self.opciones = dict()
		print('-----------------\nCartas:')
		i = 1
		for carta in self.cartas:
			print(f' { i }. { carta }')
			i += 1

		if self.ident in juego.palabraTruco:
			print(f' { i }. { diccTruco[juego.truco] }')
			self.opciones[i] = 'Truco'
			i += 1

		if juego.ronda == 1:
			if self.flor:
				print(f' { i }. Flor')
				self.opciones[i] = 'Flor'
				i += 1
			elif juego.envido == 0:
				print(f' { i }. Envido')
				self.opciones[i] = 'Envido'
				i += 1

		print(f' { i }. Mazo \n-----------------')
		self.opciones[i] = 'Mazo'

		while 1:
			try: inp = int(input('> '))
			except ValueError: continue

			if inp > len(self.cartas):
				if inp > i+1: continue

				if self.opciones[inp] == 'Truco': juego.pedirTruco(self.ident)

				elif self.opciones[inp] == 'Envido': self.pedirEnvido(juego)
				
				elif self.opciones[inp] == 'Flor': juego.pedirFlor(self.ident)
				
				elif self.opciones[inp] == 'Mazo':
					print('Jugador: Me voy al Mazo')
					juego.ganadorMano = 1-self.ident
				
				if juego.ganadorMano in [0,1]: return
			
			else: break

		print(f'Jugador: { self.cartas[inp-1] }')
		juego.cartasJugadas[self.ident] = self.cartas.pop(inp-1)

class Cpu(Jugador):
	
	def responderTruco(self, juego):
		"""
		Calcula la 'fuerza' de las cartas restantes del jugador, o bien de la ultima carta jugada.
		La fuerza es el promedio de los valores de las cartas del jugador.
		Retorna 1 para aceptar, 2 para rechazar y 3 para pedir Retruco o Vale Cuatro.
		"""
		if len(self.cartas) > 0:
			fuerza = 0
			for cart in self.cartas:
				fuerza += (cart.valor//len(self.cartas))
		
		elif juego.cartasJugadas[self.ident]:
				fuerza = juego.cartasJugadas[self.ident].valor
		
		if fuerza < 12:
			juego.ganadorMano = 1-self.ident
			return 2
		
		elif fuerza > 20 and juego.truco<3:
			return 3
		
		else: 
			return 1

	def responderEnvido(self, env):
		""" Retorna: 1, para aceptar, 0 para rechazar, o bien una opcion de Envido(segun el diccionario) """
		if env < 3:
			if self.tanto < 24: return 0
			elif self.tanto < 28: return 1
			elif self.tanto < 30: return random.choice([3,1])
			else: return random.choice([4,3,3])
		elif env == 3:
			if self.tanto < 28: return 0
			else: return 1
		else:
			return 1 if self.tanto > 30 else 0

	def pedirEnvido(self, juego):
		""" Retorna el numero de envido a pedir(segun el diccionario). False en caso de que no se pida nada."""
		if self.tanto > 31: juego.pedirEnvido(self.ident, 4)
		elif self.tanto > 29: juego.pedirEnvido(self.ident, 3)
		elif self.tanto > 21: juego.pedirEnvido(self.ident, 2)

	def jugar(self, juego):
		"""	Decide si pedir Envido/Truco o no, y elije cual carta jugar. """
		
		if juego.ronda == 1 and juego.envido == 0 and self.tanto > 20: 
			self.pedirEnvido(juego)

		# Si hay una ronda del juego empatada, la cpu jugara su carta mas fuerte.
		if 'Empate' in juego.ganadores:
			if juego.cartasJugadas[1-self.ident] and self.cartas[-1] > juego.cartasJugadas[1-self.ident]:
				juego.pedirTruco(self.ident)

			juego.cartasJugadas[self.ident] = self.cartas.pop()

		# Si el jugador ya jugo una carta, la cpu intentara jugar una mas fuerte.
		elif juego.cartasJugadas[1-self.ident]:

			for i in range(len(self.cartas)-1):
				if  self.cartas[i] > juego.cartasJugadas[1-self.ident]:
					
					if self.ident in juego.ganadores and self.ident in juego.palabraTruco:
						juego.pedirTruco(self.ident)
					
					juego.cartasJugadas[self.ident] = self.cartas.pop(i)
					break
		
		if not juego.cartasJugadas[self.ident]:
			juego.cartasJugadas[self.ident] = self.cartas.pop(0)

		if not juego.ganadorMano: 
			print(f'Cpu: {juego.cartasJugadas[self.ident]}')
