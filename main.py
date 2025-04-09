import time
import networkx as nx
import algoritmi as alg

# Importa il grafo eliminando i commenti che iniziano con '%'
#G = nx.read_edgelist("C:/Users/simon/Downloads/out.ucidata-zachary", comments="%")                      #n=34, m=78
#G = nx.read_edgelist("C:/Users/simon/Downloads/out.subeji_euroroad_euroroad", comments="%")             #n=1174, m=1417
#G = nx.read_edgelist("C:/Users/simon/Downloads/out.petster-hamster-household", comments="%")            #n=1576, m=4032
G = nx.read_edgelist("C:/Users/simon/Downloads/out.opsahl-powergrid", comments="%")                     #n=4941, m=6594
#G = nx.read_edgelist("C:/Users/simon/Downloads/out.loc-brightkite_edges", comments="%")                 #n=58228, m=214078
#G = nx.Graph()                                                                                          # Grafo vuoto per testare la funzione

# Salva time prima di inziare l'algoritmo di ricerca e filtro
start1 = time.time()

# Algoritmo di ricerca delle clique massimali
#cliques = list(nx.find_cliques_recursive(G))           # Versione standard di NetworkX (dalla libreria) (Nota che in qusto caso non conterà il numero di chiamate ricorsive)
#cliques = list(alg.trova_clique_massimali(G))          # Versione standard di NetworkX (dalla funzione nel codice) 
#cliques = list(alg.trova_clique_massimali2(G))         # Versione alternativa senza possibilità di fornire clique iniziale
            

# Stampa le clique massimali enumerandole a partire da 1
#print("\nClique massimali trovate:")
#for i, clique in enumerate(cliques, start=1):
#    print("%d: %s" %(i, clique))


# Algoritmo di filtro per clique massimali L-isolated
L=3  # Imposta il valore di isolamento L
#cliques_isolated = list(alg.filtra_clique_isolate(G, cliques, L))      # Filtra le clique massimali per mantenere solo quelle che sono L-isolated
#cliques_isolated = list(alg.trova_clique_massimali_L_isolated(G, L))    # Trova le clique massimali L-isolated direttamente senza passare per il filtro
cliques_isolated = list(alg.trova_clique_massimali_L_isolated2(G, L))  # Trova le clique massimali L-isolated direttamente senza passare per il filtro (con calcolo dinamico di AE(C))

# Salva time dopo l'esecuzione dell'algoritmo
end1 = time.time()


# Stampa le clique massimali L-isolated
#print("\nClique massimali L-isolated trovate:")
#for i, clique in enumerate(cliques_isolated, start=1):
#    print("%d: %s" %(i, clique))

# Stampa il numero di chiamate ricorsive
print("\nNumero di chiamate ricorsive per l'algoritmo di ricerca: ", alg.chiamate_ricorsive)

# Stampa il numero totale di clique massimali trovate
#print("\nNumero totale di clique massimali trovate: ", len(cliques))

# Stampa il numero totale di clique massimali L-isolated trovate
print("\nNumero totale di clique massimali L-isolated trovate (con L=", L,"): ", len(cliques_isolated))

# Stampa il tempo di esecuzione dell'algoritmo di filtro
print("\nTempo di esecuzione totale dell'algoritmo:", end1-start1, "secondi")

