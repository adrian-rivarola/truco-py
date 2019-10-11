from Diccionarios import diccJugadores,diccEnvido,diccTruco, imprimir, imprimir_borde
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
		print("├────────────────────────┤")
		print('│ 1. Quiero              │')
		print('│ 2. No quiero           │')
		try:
			imprimir_borde(f'│ 3. { diccTruco[juego.truco+1] }')
			print("└────────────────────────┘")
			max_truco = 3
		except IndexError: max_truco = 2
		
		while 1:
			try: inp = int(input('> '))
			except ValueError: continue

			if inp in range(1,max_truco+1): break

		return inp

	def responderEnvido(self, env):
		""" Retorna 0 para aceptar, 1 para rechazar, o bien una opcion de Envido(segun el diccionario) """
		if env == 2: env = 1
		
		imprimir_borde(f'│ Tu tanto es : { self.tanto }')
		
		
		print("├────────────────────────┤")
		print('│ 1. No quiero           │')
		print('│ 2. Quiero              │')
		
		for i in range(env+1,5):
			imprimir_borde(f'│ { i+1 }. { diccEnvido[i] }')
			
		
		if self.flor:
			imprimir_borde('│ 6. Flor')
		
		print("└────────────────────────┘")
		
		while 1:
			try: inp = int(input('> '))
			except ValueError: continue
			if inp in range(1,6): break

		return inp-1
		#Retorna el número ingresado por el usuario menos uno, ya que en pantalla las opciones se enumeran del 1 al 5-6.

	def pedirEnvido(self, juego):
		"""Retorna el número de envido a pedir(según el diccionario)."""

		print("┌────────────────────────┐")
		
		for i in range(2,5):
			imprimir_borde(f'│ { i-1 }. { diccEnvido[i] }')

		print("└────────────────────────┘")

		while 1:
			try: inp = int(input('> '))
			except ValueError: continue
			if inp in range(1,4): break
		
		juego.pedirEnvido(self.ident, inp+1) 
		#El dicc Envido empieza en 2, por lo que se añade 1 al input del usuario.

	def jugar(self, juego):
		"""
		Muestra en pantalla todas las opciones que el usuario puede jugar, y las almacena en un diccionario.
		El usuario ingresa el numero de la opcion a jugar, y el metodo de esta opcion es ejecutado
		"""
		self.opciones = dict()

		print("┌────────────────────────┐")
		print("│     Tus cartas:        │")
		print("├────────────────────────┤")
		
		i = 1
		for carta in self.cartas:
			imprimir_borde(f'│ { i }. { carta }')
			i += 1

		print("├────────────────────────┤")

		if self.ident in juego.palabraTruco:
			imprimir_borde(f'│ { i }. { diccTruco[juego.truco] }')
			self.opciones[i] = 'Truco'
			i += 1

		if juego.ronda == 1:
			
			if self.flor:
				imprimir_borde(f'│ { i }. Flor')
				self.opciones[i] = 'Flor'
				i += 1
			
			elif juego.envido == 0:
				imprimir_borde(f'│ { i }. Envido')
				self.opciones[i] = 'Envido'
				i += 1

		self.opciones[i] = 'Mazo'
		imprimir_borde(f'│ { i }. Mazo')
		print("└────────────────────────┘")
		
		while 1:
			try: 
				inp = int(input('> '))
				if inp in range(1, len(self.cartas)+1): break

			except ValueError: continue
			
			if 0 < inp > i: continue
			
			if self.opciones[inp] == 'Truco' and self.ident in juego.palabraTruco: 
				juego.pedirTruco(self.ident)

			elif self.opciones[inp] == 'Envido': 
				self.pedirEnvido(juego)
				self.opciones[inp] = ''
			
			elif self.opciones[inp] == 'Flor': 
				juego.pedirFlor(self.ident)
			
			elif self.opciones[inp] == 'Mazo':
				imprimir('│ J1: Me voy al Mazo.')
				juego.ganadorMano = 1-self.ident
			
			if juego.ganadorMano in [0,1]: return
		
		juego.cartasJugadas[self.ident] = self.cartas.pop(inp-1)

		imprimir(f'│ J1: { juego.cartasJugadas[self.ident] }')

class Cpu(Jugador):
	
	def responderTruco(self, juego):
		"""
		Calcula la 'fuerza' de las cartas restantes del jugador, o bien de la ultima carta jugada.
		La fuerza es el promedio de los valores de las cartas del jugador.
		Retorna 1 4ra aceptar, 2 para rechazar y 3 para pedir Retruco o Vale Cuatro.
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
		
		if self.flor: return 5
		if env < 3:
			if self.tanto < 24: return 0
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
		
		if juego.ronda == 1:
			if self.flor: 
				juego.pedirFlor(self.ident)
			
			elif juego.envido == 0 and self.tanto > 20: 
				self.pedirEnvido(juego)

		# Si hay una ronda del juego empatada, la cpu jugará su carta más fuerte.
		if 'Empate' in juego.ganadores:
			if juego.cartasJugadas[1-self.ident] and self.cartas[-1] > juego.cartasJugadas[1-self.ident]:
				juego.pedirTruco(self.ident)

			juego.cartasJugadas[self.ident] = self.cartas.pop()

		# Si el oponente ya jugó una carta, la cpu intentará jugar una más fuerte.
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
			imprimir(f'│ CPU: { juego.cartasJugadas[self.ident] }')
		
