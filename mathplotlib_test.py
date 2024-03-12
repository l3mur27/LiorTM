import matplotlib.pyplot as plt
import numpy as np

#Exemple avec une fonction x**2

#Definir la fonction 
def f(x):
    return -x**2+3*x+1

#Donné valeur max et min pour x et y
x = np.linspace(100, -100, 100)
y = f(x)

#Afficher la fonction 

plt.plot(x, y)
plt.show()
