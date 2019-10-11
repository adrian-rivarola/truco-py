from Juego import juego

if __name__ == '__main__':
	try:
		juego.jugar()
	except KeyboardInterrupt: 
		print("\n\nBye")
		exit()
