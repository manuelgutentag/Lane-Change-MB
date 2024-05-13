import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# CSV-Datei lesen
data = pd.read_csv('~/Documents/MB/Inputdaten.csv', delimiter=';', decimal='.')

# Datenlisten initialisieren
x_ego = data['x_ego']
y_ego = data['y_ego']
w_ego = data['w_ego']
vx_ego = data['vx_ego']
vy_ego = data['vy_ego']
breite_ego = data['width_ego']
x_1 = data['x_1']
y_1 = data['y_1']
vx_1 = data['vx_1']
vy_1 = data['vy_1']
Cycle = data['Cycle']

# Grenzen des ego-Fahrschlauchs definieren
schlauchborderleft = [None] * len(x_ego)
schlauchborderright = [None] * len(x_ego)

# Schlauch definieren
schlauch = False

# Abstand Liste, speichert die berechneten Distanzen
abstand_values = []

# Zeit array, Start bei 0s
frequenz = 0.01  # s/cycle
gesamtzeit = np.arange(len(Cycle)) * frequenz


# Den gesamten Zyklus iterieren
for i in range(len(Cycle)):
    # Grenzen des ego-Fahrschlauchs (ab dem Punkt, wo obj1 vor ego ist)
    if (x_1.iloc[i] - x_ego.iloc[i]) > 0:
        schlauchborderleft[i] = (y_ego.iloc[i] + 0.5 * breite_ego.iloc[i] + abs(x_1.iloc[i] - x_ego.iloc[i]) * np.tan
        (w_ego.iloc[i]))
        schlauchborderright[i] = (y_ego.iloc[i] - 0.5 * breite_ego.iloc[i] + abs(x_1.iloc[i] - x_ego.iloc[i]) * np.tan
        (w_ego.iloc[i]))

        if schlauchborderleft[i] > y_1.iloc[i] > schlauchborderright[i]:
            print("im Schlauch")
            schlauch = True
        else:
            print("nicht im Schlauch")
            schlauch = False

        if schlauch:
            abstand = np.sqrt(np.power(x_1[i] - x_ego[i], 2) + np.power(y_1[i] - y_ego[i], 2))
            vrel_ego = np.sqrt(vx_ego[i] ** 2 + vy_ego[i] ** 2)
            vrel_1 = np.sqrt(vx_1[i] ** 2 + vy_1[i] ** 2)
            ttc = abstand / abs(vrel_ego - vrel_1)

        else:
            abstand = 0
            ttc = 0
            vrel_1 = 0
            vrel_ego = 0

        print("Abstand (in m):", abstand)
        print("Time to collision (in s):", ttc)
        abstand_values.append(abstand)

    else:
        schlauchborderleft[i] = y_ego.iloc[i]
        schlauchborderright[i] = y_ego.iloc[i]
        abstand_values.append(0)

fig, axs = plt.subplots(2)  # Erstellt eine Figure mit 2 Subplots

# Plotting the abstand values over time
axs[0].plot(gesamtzeit, abstand_values)
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Abstand')
axs[0].set_title('Abstand über Zeit')
axs[0].grid()

# Plotting the position values
axs[1].plot(x_ego, y_ego, label='Position ego (t)')
axs[1].plot(x_1, y_1, label='Position obj 1 (t)')
axs[1].plot(x_1, schlauchborderleft, label='Position ego border (t)', color='green')
axs[1].plot(x_1, schlauchborderright, label='Position ego border (t)', color='green')
axs[1].legend()
axs[1].set_xlabel('x(t)')
axs[1].set_ylabel('y(t)')

plt.show()