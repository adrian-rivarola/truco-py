class Carta:
	
	def __init__(self,num,palo):
		
		self.num = num
		self.palo = palo
		self.valorE = num if num < 8 else 0
		self.valor = self.__setV__()

	def __setV__(self):
		"""
			Calcula el valor de la carta 
		"""
		if self.num == 1:
			if self.palo == "Espada": return 50
			elif self.palo == "Basto": return 45
			else: return 13
		
		elif self.num == 7:
			if self.palo == "Espada": return 40
			elif self.palo == "Oro": return 35
			else: return 7
		
		elif self.num == 2 or self.num == 3: return self.num * 7
		
		else: return self.num

	def __add__(self,carta):
		return self.valorE + carta.valorE

	def __gt__(self,carta):
		return self.valor > carta.valor

	def __str__(self):
		return '{} de {}'.format(self.num, self.palo)
	
	def __repr__(self):
		return '{} de {}'.format(self.num, self.palo)