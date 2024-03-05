import matplotlib.pyplot as plt
import numpy as np

#Exemple avec une fonction x**2

#Definir la fonction 
def f(x):
    return x**2

#Donné valeur max et min pour x et y
x = np.linspace(-100, 100, 1000)
y = f(x)

#Afficher la fonction 

plt.plot(x, y)
plt.show()
