import networkx as nx

global chiamate_ricorsive      # Inizializzazione variabile globale per contare le chiamate ricorsive
chiamate_ricorsive = 0
            
            # *********************************************************************
            # *                VERSIONE STANDARD DA NETWORKX                      *
            # *********************************************************************

# Passa come parametro il grafo e, opzionalmente, una clique; se fornita troverà tutte le clique massimali contenenti la clique data
def trova_clique_massimali(G, nodes=None):
    # Controlla se il grafo è vuoto
    if len(G) == 0:
        print("Il grafo è vuoto. Nessuna clique trovata.")
        exit()

    # Crea un dizionario di adiacenza, dove ogni nodo è associato ai suoi vicini
    adj = {u: {v for v in G[u] if v != u} for u in G}

    # Inizializza Q con i nodi forniti (se specificati), altrimenti come lista vuota
    Q = nodes[:] if nodes is not None else []
    # Inizializza cand_init con tutti i nodi del grafo
    cand_init = set(G)
    
    # Verifica che i nodi forniti (se specificati) formino una clique
    for node in Q:
        if node not in cand_init:
            raise ValueError(f"The given `nodes` {nodes} do not form a clique")
        # Aggiorna cand_init con l'intersezione dei vicini dei nodi in Q
        cand_init &= adj[node]

    # Se non ci sono candidati, restituisce un iteratore con la clique corrente
    if not cand_init:
        return iter([Q])

    # Inizializza subg_init con i candidati iniziali
    subg_init = cand_init.copy()

    # Funzione ricorsiva per espandere le clique
    def expand(subg, cand):
        global chiamate_ricorsive     # Dichiarazione globale per accedere alla variabile e modificarla
        chiamate_ricorsive += 1       # Incrementa il contatore
        # Sceglie un nodo pivot con il massimo numero di vicini in comune con cand
        u = max(subg, key=lambda u: len(cand & adj[u]))
        # Itera sui nodi candidati che non sono vicini al pivot
        for q in cand - adj[u]:
            # Rimuove il nodo q dai candidati
            cand.remove(q)
            # Aggiunge q alla clique corrente
            Q.append(q)
            # Calcola i vicini di q
            adj_q = adj[q]
            # Calcola il sottografo dei vicini di q
            subg_q = subg & adj_q
            # Se il sottografo è vuoto, restituisce la clique corrente
            if not subg_q:
                yield Q[:]
            else:
                # Calcola i nuovi candidati
                cand_q = cand & adj_q
                # Se ci sono candidati, continua l'espansione ricorsiva
                if cand_q:
                    yield from expand(subg_q, cand_q)
            # Rimuove q dalla clique corrente (backtracking)
            Q.pop()

    # Avvia l'espansione con il sottografo e i candidati iniziali
    return expand(subg_init, cand_init)

            # ************************************************************************
            # *  VERSIONE ALTERNATIVA SENZA POSSIBILITA' DI FORNIRE CLIQUE INIZIALE  *
            # ************************************************************************

def trova_clique_massimali2(G):
    # Controlla se il grafo è vuoto
    if len(G) == 0:
        print("Il grafo è vuoto. Nessuna clique trovata.")
        exit()

    # Crea un dizionario di adiacenza, dove ogni nodo è associato ai suoi vicini
    adj = {u: set(G[u]) for u in G}

    # Inizializza i candidati con tutti i nodi del grafo
    cand_init = set(G)

    # Funzione ricorsiva per espandere le clique
    def expand(subg, cand, Q):
        global chiamate_ricorsive     # Dichiarazione globale per accedere alla variabile e modificarla
        chiamate_ricorsive += 1       # Incrementa il contatore 
        # Sceglie un nodo pivot con il massimo numero di vicini in comune con cand
        u = max(subg, key=lambda u: len(cand & adj[u]))
        # Itera sui nodi candidati che non sono vicini al pivot
        for q in list(cand - adj[u]):  # Usa una copia per evitare modifiche durante l'iterazione
            # Rimuove il nodo q dai candidati
            cand.remove(q)
            # Aggiunge q alla clique corrente
            Q.append(q)
            # Calcola i vicini di q
            adj_q = adj[q]
            # Calcola il sottografo dei vicini di q
            subg_q = subg & adj_q
            # Se il sottografo è vuoto, restituisce la clique corrente
            if not subg_q:
                yield Q[:]
            else:
                # Calcola i nuovi candidati
                cand_q = cand & adj_q
                # Se ci sono candidati, continua l'espansione ricorsiva
                if cand_q:
                    yield from expand(subg_q, cand_q, Q)
            # Rimuove q dalla clique corrente (backtracking)
            Q.pop()

    # Avvia l'espansione con il sottografo e i candidati iniziali
    return expand(cand_init, cand_init.copy(), [])

           
            # ************************************************************************
            # *         ALGORITMO DI FILTRO PER CLIQUE MASSIMALI L-ISOLATED          *
            # ************************************************************************
            
def filtra_clique_isolate(G, cliques, L):
    
    # Filtra le clique massimali per mantenere solo quelle che sono L-isolated
    # G: Grafo originale
    # cliques: Lista delle clique massimali
    # L: Valore di isolamento
    # return: Lista delle clique L-isolated
    
    clique_isolate = []

    for clique in cliques:
        k = len(clique)  # Numero di nodi nella clique
        
        # Calcola la somma dei gradi dei nodi nella clique
        S = sum(G.degree[node] for node in clique) 

        # Calcola il numero di estremi di arco interni alla clique
        estremi_interni = k*(k - 1)  

        # Calcola il numero di estremi di arco uscenti dalla clique
        estremi_uscenti = S - estremi_interni

        # Verifica la condizione di isolamento
        if estremi_uscenti <= k * L:
            clique_isolate.append(clique)

    return clique_isolate



