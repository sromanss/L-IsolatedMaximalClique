import time
import networkx as nx
import algoritmi as alg

# Importa il grafo eliminando i commenti che iniziano con '%'

#G = nx.read_edgelist("C:/Users/simon/Downloads/out.ucidata-zachary", comments="%")                         #n=34, m=78
#G = nx.read_edgelist("C:/Users/simon/Downloads/out.subelj_euroroad_euroroad", comments="%")                #n=1174, m=1417
#G = nx.read_edgelist("C:/Users/simon/Downloads/out.petster-hamster-household", comments="%")               #n=1576, m=4032
#G = nx.read_edgelist("C:/Users/simon/Downloads/out.opsahl-powergrid", comments="%")                        #n=4941, m=6594
G = nx.read_edgelist("C:/Users/simon/Downloads/out.loc-brightkite_edges", comments="%")                    #n=58228, m=214078
#G = nx.Graph()                                                                                             # Grafo vuoto 

tempi = []                                                                                      # Inizializza lista per contenere i tempi delle diverse esecuzioni
chiamate_ricorsive = []                                                                         # Inizializza lista per contenere il numero dele chiamate ricorsive delle diverse esecuzioni
numero_tagli = []                                                                               # Inizializza lista per contenere il numero dei numeri di tagli delle diverse esecuzioni
L =1                                                                                          # Imposta il valore di isolamento L
euristica = 3                                                                                   # Imposta l'euristica (1 o 2)
numero_ripetizioni = 100                                                                         # Imposta il numero di ripetizioni per il calcolo del tempo medio

for _ in range(numero_ripetizioni):                                                             # Ripeti le esecuzioni tante volte quanto indicato nella variabile numero_ripetizioni
    #alg.chiamate_ricorsive = 0                                                                  # Resetta il contatore delle chiamate ricorsive
    #alg.numero_tagli = 0                                                                        # Resetta il contatore dei tagli
    start_time = time.time()                                                                    # Salva l'istante di tempo in cui comincia un'esecuzione
    
    #cliques = list(alg.trova_clique_massimali2(G))                                             # Trova le clique massimali
    #cliques_isolated = alg.filtra_clique_isolate(G, cliques, L)                                # Filtra le cliques massimali
    #cliques_isolated = alg.trova_clique_massimali_L_isolated(G, L)                             # Con calcolo di AE(C)
    #cliques_isolated = alg.trova_clique_massimali_L_isolated2(G, L)                            # Con calcolo dinamico di AE(C)
    cliques_isolated = alg.trova_clique_massimali_L_isolated3(G, L, euristica)                 # e = 1 -> D = len(P); e = 2 -> D = 1 + grado_massimo_sottografoDiP
    
    end_time = time.time()                                                                      # Salva l'istante di tempo in cui finisce un'esecuzione
    tempi.append(end_time - start_time)                                                         # Memorizza il tempo di esecuzione
    #chiamate_ricorsive.append(alg.chiamate_ricorsive)                                           # Memorizza il numero di chiamate ricorsive
    #numero_tagli.append(alg.numero_tagli)                                                       # Memorizza il numero di tagli

# Calcola il tempo medio e il numero medio di chiamate ricorsive
tempo_medio = sum(tempi) / len(tempi)
#chiamata_ricorsive_medie = sum(chiamate_ricorsive) / len(chiamate_ricorsive)
#numero_tagli_medio = sum(numero_tagli) / len(numero_tagli)

# Stampa i risultati
print(f"Tempo medio di esecuzione dopo {numero_ripetizioni} esecuzioni: {tempo_medio:.6f} secondi")
print(f"Numero totale di clique massimali L-isolated trovate: {len(cliques_isolated)}")
#print(f"Numero totale di chiamate ricorsive: {chiamata_ricorsive_medie}")
#print(f"Numero totale di tagli: {numero_tagli_medio}")

"""
                                           
if alg.verifica_cliques_isolate(cliques_isolated1, cliques_isolated2):
    print("Le clique L-isolated trovate con entrambi i metodi sono identiche.")
else:
    print("Le clique L-isolated trovate con i due metodi sono diverse!")

"""

