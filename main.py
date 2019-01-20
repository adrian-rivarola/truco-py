from Juego import Juego
import time

juego = Juego()

#Jugar hasta 9 puntos
while max(juego.puntos) < 9:

	juego.repartir()
	while juego.ganadorMano is None:
		juego.jugarRonda()
	
	juego.info()
	time.sleep(3)
