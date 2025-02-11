import numpy as np
import random
import matplotlib.pyplot as plt
import argparse

class Materiale:
    def __init__(self, nome, X0, E_critica_e, E_critica_p, perdita_ionizzazione_X0):
        self.nome = nome
        self.X0 = X0
        self.E_critica_e = E_critica_e
        self.E_critica_p = E_critica_p
        self.perdita_ionizzazione_X0 = perdita_ionizzazione_X0
        
materiali = {
    "SiO2": Materiale("SiO2", 12.29, 50.58, 49.17, 3.737),
    "H2O_ghiaccio": Materiale("H2O_ghiaccio", 39.31, 78.60, 76.50, 1.822)
    }

#Argparse per selezionare il materiale
parser = argparse.ArgumentParser(description="Simulazione di sciami elettromagnetici in materiali differenti.")
parser.add_argument("-m","--materiale",required=True, help="Materiale per la simulazione (SiO2 o H2O in forma di ghiaccio)")
args = parser.parse_args()

# Selezione dei parametri del materiale scelto
if args.materiale not in materiali:
    print("Errore: Materiale non valido. Scegliere tra SiO2 o H2O_ghiaccio.")
    exit(1)
X0 = materiali[args.materiale].X0
E_critica_e = materiali[args.materiale].E_critica_e
E_critica_p = materiali[args.materiale].E_critica_p
perdita_ionizzazione_X0 = materiali[args.materiale].perdita_ionizzazione_X0
passo = 0.1
#Conferma del materiale scelto
print(f"Materiale selezionato: {args.materiale}")
print(f"X0:{X0} cm, E_critica elettroni: {E_critica_e} MeV, E_critica positroni: {E_critica_p} MeV, Perdita ionizzazione: {perdita_ionizzazione_X0} MeV/cm")

#Energie iniziali da testare
E_iniziali = [500,1000,2000,4000] #MeV
num_simulazioni = 1000

def simula_sciame(E_iniziale):
    
    soglia_produzione_coppie = 1.02 #MeV
    
    # Inizializzazione delle particelle con l'energia iniziale
    particelle = [{'tipo': 'e', 'energia': E_iniziale}]
    perdita_ionizzazione_totale = 0
    perdita_ionizzazione_step = []
    conteggio_particelle_step = []
    
    while particelle:
        nuove_particelle = []
        perdita_ionizzazione = 0
        
        for particella in particelle:
            energia = particella['energia']
            tipo = particella['tipo']
            if tipo == 'e':
                E_critica = E_critica_e
            elif tipo == "p":
                E_critica = E_critica_p
            
            if tipo in ['e', 'p']:
                if energia > perdita_ionizzazione_X0 * passo:
                    perdita_energia = perdita_ionizzazione_X0 * passo
                    energia -= perdita_energia
                    perdita_ionizzazione += perdita_energia
                    if energia > E_critica: # Possibilità di emettere un fotone per bremsstrahlung.
                        if random.random() < (1 - np.exp(-passo)):
                            if tipo == 'e':
                                nuove_particelle.append({'tipo': 'fotone', 'energia': energia / 2})
                                nuove_particelle.append({'tipo': 'e', 'energia': energia / 2})
                            elif tipo == 'p':
                                nuove_particelle.append({'tipo': 'fotone', 'energia': energia / 2})
                                nuove_particelle.append({'tipo': 'p', 'energia': energia / 2})       
                        else:
                             if tipo == 'e':
                                nuove_particelle.append({'tipo': 'e', 'energia': energia})
                             elif tipo == 'p':
                                nuove_particelle.append({'tipo': 'p', 'energia': energia})
                    else:
                         if tipo == 'e':
                             nuove_particelle.append({'tipo': 'e', 'energia': energia})
                         elif tipo == 'p':
                             nuove_particelle.append({'tipo': 'p', 'energia': energia})               
                else:
                    perdita_ionizzazione += random.uniform(0, energia)

            elif tipo == 'fotone':
                if energia > soglia_produzione_coppie:
                    if random.random() < (1 - np.exp(-(7/9) * passo)):
                        nuove_particelle.append({'tipo': 'e', 'energia': energia / 2})
                        nuove_particelle.append({'tipo': 'p', 'energia': energia / 2})
                    else:
                        nuove_particelle.append({'tipo': 'fotone', 'energia': energia})
                else:
                     perdita_ionizzazione += random.uniform(0, energia)
        
        # Aggiornamento dei valori
        perdita_ionizzazione_totale += perdita_ionizzazione
        perdita_ionizzazione_step.append(perdita_ionizzazione)
        conteggio_particelle_step.append(len(nuove_particelle))
        particelle = nuove_particelle

    return conteggio_particelle_step, perdita_ionizzazione_step, perdita_ionizzazione_totale

#Simulazioni multiple per ciascuna energia
risultati = {}

# Dizionario per salvare i valori di X_max per ogni energia iniziale per ogni simulazione (PER ISTOGRAMMA)
xmax_values = {E: [] for E in E_iniziali}
media_perdite_totali = []
dev_perdite_totali = []
for E in E_iniziali:
    all_conteggi = []
    all_perdite = []
    all_perdite_totali = []

    for _ in range(num_simulazioni):
        conteggi,perdite,perdite_tot = simula_sciame(E)
        steps_singolasimulazione = np.arange(len(conteggi)) * passo * X0
        indice_massimo = np.argmax(np.abs(conteggi))
        x_massimo = steps_singolasimulazione[indice_massimo]
        xmax_values[E].append(x_massimo)
        all_conteggi.append(conteggi)
        all_perdite.append(perdite)
        all_perdite_totali.append(perdite_tot)
    max_length_conteggi = max(map(len, all_conteggi))
    max_length_perdite = max(map(len, all_perdite))
    all_conteggi = np.array([np.pad(lst, (0, max_length_conteggi - len(lst))) for lst in all_conteggi])
    all_perdite = np.array([np.pad(lst, (0, max_length_perdite - len(lst))) for lst in all_perdite])
    mean_conteggio = np.mean(all_conteggi, axis=0)
    std_conteggio = np.std(all_conteggi, axis=0) #consapevole che i conteggi sono valori "discreti" ma poi per avere un andamento lineare a livello grafico prendo anche risultati con la virgola
    mean_perdita = np.mean(all_perdite, axis=0)
    std_perdita = np.std(all_perdite, axis=0)
    mean_perdite_tot = np.mean(all_perdite_totali)
    std_perdite_tot = np.std(all_perdite_totali)
    media_perdite_totali.append(mean_perdite_tot)
    dev_perdite_totali.append(std_perdite_tot)

    risultati[E] = {
        "mean_conteggio": mean_conteggio,
        "std_conteggio": std_conteggio,
        "mean_perdita": mean_perdita,
        "std_perdita": std_perdita
    }

# Grafici

# Numero medio di particelle per step in funzione della profondità, grafico unico con tutte e 4 le energie
colori = ("blue","orange","red","green")
plt.figure(figsize=(12, 5))
for i,E in enumerate(E_iniziali):
    steps = np.arange(len(risultati[E]["mean_conteggio"])) * passo * X0  # in cm
    plt.plot(steps, risultati[E]["mean_conteggio"], label=f"{E} MeV",color = colori[i])
plt.xlabel("Profondità (cm)")
plt.ylabel("Numero medio di particelle")
plt.title("Sviluppo longitudinale dello sciame EM")
plt.legend()
plt.grid()
plt.show()

# Numero medio particelle per step in funzione della profondità, subplot con barre errore
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
for i, E in enumerate(E_iniziali):
    steps = np.arange(len(risultati[E]["mean_conteggio"])) * passo * X0
    ax = axs[i//2, i%2]
    ax.errorbar(steps, risultati[E]["mean_conteggio"], yerr=risultati[E]["std_conteggio"], fmt='-', label=f"{E} MeV",color = colori[i]) 
    ax.set_title(f"Grafico per {E} MeV")
    ax.set_xlabel("Profondità (cm)")
    ax.set_ylabel("Numero medio di particelle")
    ax.legend()
plt.tight_layout()
plt.show()

#  Energia depositata per ionizzazione per step in funzione della profondità per le 4 energie
plt.figure(figsize=(12, 5))
for i,E in enumerate(E_iniziali):
    steps = np.arange(len(risultati[E]["mean_conteggio"])) * passo * X0
    plt.plot(steps, risultati[E]["mean_perdita"], label=f"{E} MeV",color = colori[i])
plt.xlabel("Profondità (cm)")
plt.ylabel("Energia media persa per ionizzazione (MeV)")
plt.title("Energia depositata per ionizzazione")
plt.legend()
plt.grid()
plt.show()

# Energia depositata per ionizzazione per step in funzione della profondità per le 4 energie,subplot con barre errore
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
for i, E in enumerate(E_iniziali):
    steps = np.arange(len(risultati[E]["mean_conteggio"])) * passo * X0
    ax = axs[i//2, i%2]
    ax.errorbar(steps, risultati[E]["mean_perdita"], yerr=risultati[E]["std_perdita"], fmt='-', label=f"{E} MeV",color = colori[i]) 
    ax.set_title(f"Grafico per {E} MeV")
    ax.set_xlabel("Profondità (cm)")
    ax.set_ylabel("Energia media persa per ionizzazione(MeV)")
    ax.legend()
plt.tight_layout()
plt.show()

# Media delle perdite totali rispetto alle simulazioni per ciascuna energia in funzione dell'energia iniziale
plt.figure(figsize=(12, 5))
plt.scatter(E_iniziali,media_perdite_totali,color="red",linestyle = "None")
plt.errorbar(E_iniziali, media_perdite_totali,yerr = dev_perdite_totali,color ="red",linestyle = "None")
plt.xlabel("Energie iniziali dei 4 set (MeV) ")
plt.ylabel("Energia media persa totale per i 4 set (MeV)")
plt.title("Energia ")
plt.grid()
plt.show()
    


# X_max ottenuto dalla media delle simulazioni per ciascuna energia in funzione delle energie iniziali
x_massimi=[]
devstand_massimi=[]
for E in E_iniziali:
    mean_conteggio = risultati[E]["mean_conteggio"]
    indice_massimo = np.argmax(np.abs(mean_conteggio))
    x_massimo = steps[indice_massimo]
    x_massimi.append(x_massimo)
    std_conteggio=risultati[E]["std_conteggio"]
    devstand_massimo= std_conteggio[indice_massimo]
    devstand_massimi.append(devstand_massimo)
plt.figure(figsize=(12, 5))
plt.scatter(E_iniziali,x_massimi,color="blue",linestyle = "None")
plt.errorbar(E_iniziali,x_massimi,yerr=devstand_massimi,color="blue",linestyle = "None")
plt.xlabel("Energia iniziale (MeV)")
plt.ylabel("X_max(cm)")
plt.title("Fluttuazioni di X_max in funzione di E_0")
plt.grid()
plt.show()


# Istogramma che mi va a rappresentare la distribuzione dei valori di X_max per ciascuna energia
fig, axes = plt.subplots(2, 2, figsize=(10, 8))  # 2 righe, 2 colonne

for i, (E, ax) in enumerate(zip(E_iniziali, axes.flat)):
    data = xmax_values[E]
    ax.hist(data, bins=50, edgecolor='black', alpha=0.7)
    ax.set_title(f"$E_0 = {E}$ MeV", fontsize=14)
    ax.set_xlabel("$X_{max}$ (cm)")
    ax.set_ylabel("Frequenza")
    mean_X_max = np.mean(data)
    std_X_max = np.std(data)
    ax.axvline(mean_X_max, color='r', linestyle='dashed', linewidth=2, label=f'Media: {mean_X_max:.2f} cm')
    ax.axvline(mean_X_max + std_X_max, color='g', linestyle='dashed', linewidth=2, label=f'+1 std: {mean_X_max + std_X_max:.2f} cm')
    ax.axvline(mean_X_max - std_X_max, color='g', linestyle='dashed', linewidth=2, label=f'-1 std: {mean_X_max - std_X_max:.2f} cm')
    ax.legend()  
plt.tight_layout()
plt.show(
