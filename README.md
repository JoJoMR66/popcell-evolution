# Stochastic Dynamics of Cell Division: Euler-Maruyama vs. Gillespie

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Ce dépôt contient les codes de simulation numérique développés dans le cadre d'un projet de Complex Matter en Master 2 de Physique Fondamentale et Applications. 

L'objectif est d'étudier le temps de fixation et la probabilité d'extinction de deux populations (A et B) soumises à une sélection $s$ permettant de différencier l'espèce "mutante" de l'espèce "sauvage" et des ressources naturelles limitées.

## 🧬 Contexte Scientifique

Le modèle décrit l'évolution de deux populations en compétition pour une ressource limitée, suivant une dynamique de type logistique stochastique. 
- **Population A** : Taux de naissance avantageux $b_A = b_{max}(1+s)(1 - N_{tot}/K)$
- **Population B** : Taux de naissance standard $b_B = b_{max}(1 - N_{tot}/K)$

Nous comparons deux méthodes de résolution numérique pour explorer les échelles de temps du système.

## 💻 Méthodes Numériques

### 1. Intégration d'Euler-Maruyama (SDE)
Situé dans `src/euler_maruyama.py`, ce script résout "The Chemical Langevin Equation" associée au modèle.
- **Optimisation :** Utilisation de `numba.jit` pour des performances proches du C.
- **Innovation :** Implémentation d'un **pas de temps adaptatif** ($\epsilon$-control) permettant de capturer les dynamiques rapides près des seuils d'extinction tout en accélérant la simulation en phase stationnaire.

### 2. Algorithme de Gillespie (Monte-Carlo Exact)
Situé dans `src/monte-carlo.py`, ce script réalise une simulation exacte de la chaîne de Markov à temps continu.
- **Précision :** Contrairement à Euler-Maruyama, cette méthode est exacte et traite les individus comme des entités discrètes.
- **Usage :** Idéal pour valider les résultats de l'approche continue sur de petites populations ($N_m$).

## 🚀 Installation

1. Cloner le dépôt :
```bash
git clone [https://github.com/JoJoMR66/popcell-evolution.git](https://github.com/JoJoMR66/popcell-evolution.git)
cd projet-cellule

"Pour installer les bibliothèques nécessaires, tapez la commande suivante : pip install -r requirements.txt"
