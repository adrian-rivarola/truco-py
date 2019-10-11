# Diccionarios

diccEnvido = {
	0 : 'No quiero',
	1 : 'Quiero',
	2 : 'Envido',
	3 : 'Real Envido',
	4 : 'Falta Envido',
	5 : 'Flor'
}

diccTruco = {
	1 : 'Truco',
	2 : 'Retruco',
	3 : 'Vale Cuatro'
}

diccJugadores = {
	0 : 'J1 ',
	1 : 'CPU'
}

def imprimir(txt):
	print("┌────────────────────────┐")
	print("│                        │")
	print(txt + ' '*(25-len(txt))+ '│')
	print("│                        │")
	print("└────────────────────────┘")

def imprimir_borde(txt):
	print(txt + ' '*(25-len(txt)) + '│')