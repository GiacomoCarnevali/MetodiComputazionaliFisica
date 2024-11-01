import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
file_letto = pd.read_csv('kplr010666592-2011240104155_slc.csv')
print(file_letto.columns)
plt.plot(file_letto["TIME"],file_letto["PDCSAP_FLUX"])
plt.show()
plt.plot(file_letto["TIME"],file_letto["PDCSAP_FLUX"])
plt.plot(file_letto["TIME"],file_letto["PDCSAP_FLUX"] , 'o', color='blue')
plt.show()
plt.plot(file_letto["TIME"],file_letto["PDCSAP_FLUX"])
plt.errorbar(file_letto["TIME"],file_letto["PDCSAP_FLUX"], yerr=file_letto["PDCSAP_FLUX_ERR"], fmt='o' )
plt.show()
min_date = file_letto['PDCSAP_FLUX'].idxmin()
t = file_letto["TIME"][min_date]
file_nuovo = file_letto.loc[( file_letto['TIME'] > t-2) & ( file_letto['TIME'] < t+2)]
plt.plot(file_nuovo["TIME"],file_nuovo["PDCSAP_FLUX"])
plt.show()
fig,ax = plt.subplots(1,2, figsize=(12,6))
ax[0].plot(file_letto['TIME'], file_letto['PDCSAP_FLUX'], 's-', color='limegreen')
ax[0].set_title('Grafico Y1', fontsize=15, color='limegreen')

ax.legend()
inset_ax = fig.add_axes([0.6, 0.6, 0.25, 0.25])  # [posizione_x, posizione_y, larghezza, altezza]
inset_ax.plot(file_nuovo['TIME'], file_nuovo['PDCSAP_FLUX'], 'r')  # Inserisci qui i dati del grafico inset
inset_ax.set_title('Inset: Cos(x)')
inset_ax.grid(True)
ax.set_title('Grafico con Inset')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()
