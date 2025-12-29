import numpy as np
import pandas as pd
import time
from numba import jit

@jit(nopython=True)
def simuler_trajectoire_adaptative(Nm, s, bmax, d, dt_max, max_steps):
    # Paramètres dérivés
    K = Nm / (1 - (d / bmax))
    Na = int(0.9 * Nm / 2)
    Nb = int(0.9 * Nm / 2)
    
    t = 0.0
    
    # Paramètre de sécurité pour le pas de temps adaptatif
    # On ne veut pas que la population change de plus de 10% en un seul pas (partie déterministe)
    epsilon = 0.1 
    
    # Seuil en dessous duquel on force un dt très petit pour la précision finale
    seuil_critique = 10.0 
    
    for _ in range(max_steps): # On utilise _ car i ne correspond plus au temps linéaire
        N_total = Na + Nb
        
        # 1. Calcul des taux instantanés
        b = bmax * (1 - N_total / K)
        if b < 0: b = 0
        a = b * (1 + s)
        
        # Taux de changement net (drift)
        drift_a = (a - d) * Na
        drift_b = (b - d) * Nb
        
        # 2. CALCUL DU DT ADAPTATIF
        # On calcule le dt idéal pour ne pas changer trop vite
        # On ajoute 1e-9 pour éviter la division par zéro
        dt_a = (epsilon * Na) / (abs(drift_a) + 1e-9)
        dt_b = (epsilon * Nb) / (abs(drift_b) + 1e-9)
        
        # On prend le plus petit dt nécessaire, mais on le plafonne à dt_max
        dt_curr = min(dt_max, dt_a, dt_b)
        
        # Sécurité supplémentaire : si on est très proche de 0, on réduit encore
        if Na < seuil_critique or Nb < seuil_critique:
            dt_curr = min(dt_curr, 0.01) # Petit pas fixe proche de l'extinction
            
        # 3. Simulation du pas (Euler-Maruyama avec dt variable)
        sqrt_dt = np.sqrt(dt_curr)
        
        # Termes de bruit
        term_a = (a + d) * Na
        term_b = (b + d) * Nb
        
        dWa = np.sqrt(max(0.0, term_a)) * np.random.randn()
        dWb = np.sqrt(max(0.0, term_b)) * np.random.randn()
        
        Na_new = Na + drift_a * dt_curr + dWa * sqrt_dt
        Nb_new = Nb + drift_b * dt_curr + dWb * sqrt_dt
        
        t += dt_curr
        
        # 4. Conditions d'arrêt
        if Na_new <= 0:
            return t, 0, N_total, 0, Nb_new
        elif Nb_new <= 0:
            return t, 1, N_total, Na_new, 0
            
        Na = Na_new
        Nb = Nb_new
        
    return t, Na/(Na+Nb), Na+Nb, Na, Nb

# --- Configuration et Lancement ---

# On peut maintenant se permettre un T théorique énorme car le code va s'adapter
# Et on peut augmenter dt_max car l'algo le réduira si besoin
dt_max_ref = 0.1 # On peut tenter plus grand que 0.025 pour les phases calmes
T_theorique = 100000 
max_steps_theorique = int(1e8) # Très grand nombre, juste pour ne pas boucler à l'infini

# Paramètres
bmax = 0.4
d = 0.008

# Tes paramètres d'étude
valeurs_s = -np.logspace(-4, -1, 8) 
valeurs_Nm = [2**j for j in range(3, 10)] 
nb_reals = 800 

resultats = []
print(f"Simulation adaptative lancée...")
start_time = time.time()

for Nm in valeurs_Nm:
    print(f"Population {Nm}...")
    for s in valeurs_s:
        Pe = abs(s) * Nm
        for _ in range(nb_reals):
            t_f, x_f, N_f, Na_f, Nb_f = simuler_trajectoire_adaptative(
                Nm, s, bmax, d, dt_max_ref, max_steps_theorique
            )
            
            resultats.append({
                "t": t_f, "x(t)": x_f, "N": N_f, 
                "Na": Na_f, "Nb": Nb_f, "Nmax": Nm, "s": s, "Pe": Pe
            })

end_time = time.time()
print(f"Temps total : {end_time - start_time:.2f} s")

df_adapt = pd.DataFrame(resultats)
save_data(df_adapt)
