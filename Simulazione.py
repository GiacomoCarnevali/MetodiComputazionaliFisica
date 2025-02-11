import numpy as np
import sys
import random

def simula_sciame(E_iniziale, E_critica, perdita_ionizzazione_X0, passo):
    soglia_produzione_coppie = 1.02 
    
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
                    perdita_ionizzazione += random.uniform(0, energia) # Se l'energia è sotto dE/dX0 la particella viena assorbita per ionizzazione. Non può compiere bremsstrahlung.
            elif tipo == 'fotone':
                if energia > soglia_produzione_coppie:
                    if random.random() < (1 - np.exp(-(7/9) * passo)):
                        nuove_particelle.append({'tipo': 'e', 'energia': energia / 2})
                        nuove_particelle.append({'tipo': 'p', 'energia': energia / 2})
                    else:
                        nuove_particelle.append({'tipo': 'fotone', 'energia': energia})
                else:
                     perdita_ionizzazione += random.uniform(0, energia)

        # Aggiornamento dei valori totali e per step
        perdita_ionizzazione_totale += perdita_ionizzazione
        perdita_ionizzazione_step.append(perdita_ionizzazione)
        conteggio_particelle_step.append(len(nuove_particelle))
        particelle = nuove_particelle

    print("\nSimulazione terminata.")
    print(f"Energia totale persa per ionizzazione: {perdita_ionizzazione_totale:.2f} MeV")
    print("Numero di particelle dello sciame ad ogni step:")
    for i, num in enumerate(conteggio_particelle_step, start=1):
        print(f"Step {i}: {num} particelle")
    print("\nEnergia persa per ionizzazione ad ogni step:")
    for i, energia in enumerate(perdita_ionizzazione_step, start=1):
        print(f"Step {i}: {energia} MeV")

if __name__ == "__main__":
    # Input dei parametri da parte dell'utente
    E_iniziale = float(input("Inserisci l'energia iniziale della particella (MeV): "))
    E_critica = float(input("Inserisci l'energia critica del materiale (MeV): "))
    perdita_ionizzazione_X0 = float(input("Inserisci la perdita per ionizzazione in X_0 (MeV/cm): "))
    passo = float(input("Inserisci il passo di avanzamento (frazione di X_0, [0,1]): "))
    if not (0 <= passo <= 1):
        print("Errore: Il valore del passo deve essere compreso tra 0 e 1.")
        sys.exit(1)  # Termina il programma con codice di errore
    
    # Esecuzione della simulazione
    simula_sciame(E_iniziale, E_critica, perdita_ionizzazione_X0, passo
