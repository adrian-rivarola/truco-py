from Diccionarios import diccJugadores,diccEnvido,diccTruco
import random

class Jugador:

	def __init__(self, ident):
		"""
		La variable ident sirve como identificador del jugador(0-1).
		"""
		self.ident = ident
		self. cartas = []

	def __gt__(self, jugador):
		"""
		Retorna True o False segun el tanto de este jugador sea mayor al de otro jugador.
		"""
		return self.tanto > jugador.tanto

	def addCarta(self,carta):
		"""
		Recibe una carta como parametro, y la agrega a la lista de cartas del jugador
		"""
		self.cartas.append(carta)
		if len(self.cartas) == 3:
			self.ordenarCartas()

	def ordenarCartas(self):
		"""
		Ordena las cartas de mas debiles a mas fuertes, comprueba si el jugador tiene Flor, y calcula el tanto.
		"""
		self.cartas = sorted(self.cartas)
		
		if self.cartas[0].palo == self.cartas[1].palo and self.cartas[1].palo == self.cartas[2].palo:
			self.flor = True
		else: self.flor = False
		
		self.tanto = self.calcularTanto()
	
	def calcularTanto(self):
		"""
		Calcula el tanto si hay flor o dos cartas del mismo palo, de lo contrario retorna la carta mas alta.
		"""
		tanto = 20
		
		if self.flor:
			for cart in self.cartas:
				tanto += cart.valorE
		else:
			if self.cartas[0].palo == self.cartas[1].palo:
				tanto += self.cartas[0] + self.cartas[1]
			
			elif self.cartas[0].palo == self.cartas[2].palo:
				tanto += self.cartas[0] + self.cartas[2]
			
			elif self.cartas[1].palo == self.cartas[2].palo:
				tanto += self.cartas[1] + self.cartas[2]
			
			else:
				tanto = 0
				for cart in self.cartas:
					if cart.valorE > tanto:
						tanto = cart.valorE
		return tanto

class Humano(Jugador):
	"""
	Crea un jugador que es controlado por el usuario.
	"""

	def responderTruco(self, juego):
		"""
		Retorna 1 para aceptar
		"""
		print('---------------')
		print(' 1. Quiero\n 2. No quiero')
		try:
			print(' 3. {}'.format(diccTruco[juego.truco+1]))
		except:
			pass
		inp = int(input('> '))
		if inp in range(1,4):
			return inp
		else: return 2

	def responderEnvido(self, env):
		"""
		Retorna 0 para aceptar, 1 para rechazar, o bien una opcion de Envido(segun el diccionario)
		"""
		if env == 2: env = 1
		print('---------------')
		print('Tanto {}'.format(self.tanto))
		print('1. No quiero\n2. Quiero')
		
		for i in range(env+1,5):
			print('{}. {}'.format(i+1,diccEnvido[i]))
		
		if self.flor:
			print('6. Flor')

		inp = int(input('> '))
		while inp not in range(1,6):
			inp = int(input('> '))
		
		return inp-1
		#Retorna el numero ingresado por el usuario menos uno, ya que en pantalla las opciones se enumeran del 1 al 5-6.

	def pedirEnvido(self, juego):
		"""
		Retorna el numero de envido a pedir(segun el diccionario).
		"""
		print('---------------')
		for i in range(2,5):
			print('{}. {}'.format(i-1,diccEnvido[i]))
		
		inp = int(input('> '))
		while inp not in range(1,5):
			inp = int(input('> '))

		juego.pedirEnvido(self.ident, inp+1)

	def jugar(self, juego):
		"""
		Muestra en pantalla todas las opciones que el usuario puede jugar, y las almacena en un diccionario.
		El usuario ingresa el numero de la opcion a jugar, y el metodo de esta opcion es ejecutado
		"""
		self.opciones = dict()
		print('-----------------')
		print('Cartas:')
		i = 1
		for cart in self.cartas:
			print(' {}. {}'.format(i,cart))
			i += 1

		if self.ident in juego.palabraTruco:
			print(' {}. {}'.format(i,diccTruco[juego.truco]))
			self.opciones[i] = 'Truco'
			i += 1

		if juego.ronda == 1:
			if self.flor:
				print(' {}. Flor'.format(i))
				self.opciones[i] = 'Flor'
				i += 1
			elif juego.envido == 0:
				print(' {}. Envido'.format(i))
				self.opciones[i] = 'Envido'
				i += 1

		print(' {}. Mazo'.format(i))
		self.opciones[i] = 'Mazo'
		print('-----------------')

		inp = int(input('> '))
		while inp > len(self.cartas):
			if self.opciones[inp] == 'Truco':
				juego.pedirTruco(self.ident)

			elif self.opciones[inp] == 'Envido':
				self.pedirEnvido(juego)
			
			elif self.opciones[inp] == 'Flor':
				juego.pedirFlor(self.ident)
			
			elif self.opciones[inp] == 'Mazo':
				print('Jugador: Me voy al Mazo')
				juego.ganadorMano = 1-self.ident
				return
			
			if juego.ganadorMano: return
			else: inp = int(input('> '))

		print('Jugador: {}'.format(self.cartas[inp-1]))
		juego.cartasJugadas[self.ident] = self.cartas.pop(inp-1)

class Cpu(Jugador):
	"""
	Crea un jugador que es controlado por la CPU
	"""
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
		else:
			if juego.cartasJugadas[self.ident]:
				fuerza = juego.cartasJugadas[self.ident].valor
		
		if fuerza < 12:
			return 2
		
		elif fuerza > 20 and juego.truco<3:
			return 3
		
		else: 
			return 1

	def responderEnvido(self, env):
		"""
		Retorna: 1, para aceptar, 0 para rechazar, o bien una opcion de Envido(segun el diccionario)
		"""
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

	def pedirEnvido(self):
		"""
		Retorna el numero de envido a pedir(segun el diccionario). False en caso de que no se pida nada.
		"""
		if self.tanto > 31: return 4
		elif self.tanto > 29: return 3
		elif self.tanto > 24: return 2
		elif self.tanto > 21: return random.choice([2,False,False,False])
		else: return False

	def jugar(self, juego):
		"""
		Determina si pedir Envido/Truco o no, y elije cual carta jugar. 
		"""
		if juego.ronda == 1 and juego.envido == 0: 
			env = self.pedirEnvido()
			if env:
				juego.pedirEnvido(self.ident, env)
		
		# Si hay una ronda del juego empatada, la cpu jugara su carta mas fuerte.
		if 'Empate' in juego.ganadores:
			if juego.cartasJugadas[1-self.ident] and self.cartas[-1] > juego.cartasJugadas[1-self.ident]:
				juego.pedirTruco(self.ident)

			juego.cartasJugadas[self.ident] = self.cartas.pop() if not juego.ganadorMano else None

		# Si el jugador ya jugo una carta, la cpu intentara jugar una mas fuerte.
		elif juego.cartasJugadas[1-self.ident]:

			for i in range(len(self.cartas)-1):
				if  self.cartas[i] > juego.cartasJugadas[1-self.ident]:
					
					if self.ident in juego.ganadores and self.ident in juego.palabraTruco: 
						juego.pedirTruco(self.ident)
					
					juego.cartasJugadas[self.ident] = self.cartas.pop(i) if not juego.ganadorMano else None
					break
		
		if not juego.cartasJugadas[self.ident]:
			juego.cartasJugadas[self.ident] = self.cartas.pop(0)

		if not juego.ganadorMano: 
			print('{}: {}'.format(diccJugadores[self.ident],juego.cartasJugadas[self.ident]))
