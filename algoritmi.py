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

            
            # ***********************************************************************************************
            # *         ALGORITMO DI RICERCA E FILTRO PER CLIQUE MASSIMALI L-ISOLATED  (VERSIONE 1)         *
            # *                               (con calcolo di AE(C))                                        *
            # ***********************************************************************************************


def trova_clique_massimali_L_isolated(G, L):
    # Controlla se il grafo è vuoto
    if len(G) == 0:
        print("Il grafo è vuoto. Nessuna clique trovata.")
        return []

    # Crea un dizionario di adiacenza, dove ogni nodo è associato ai suoi vicini
    adj = {u: set(G[u]) for u in G}

    # Inizializza i candidati iniziali con tutti i nodi del grafo
    candidati_iniziali = set(G)

    # Lista per memorizzare le clique massimali L-isolated
    clique_isolated = []

    # Funzione per calcolare AE(C)
    def calcola_AE(C, P):
        # Somma i gradi dei nodi in C
        somma_gradi = sum(G.degree[u] for u in C)
        # Sottrai gli archi interni a C
        archi_interni = len(C) * (len(C) - 1)
        # Sottrai gli archi che vanno verso P
        # Per ogni nodo u nella clique corrente C, calcola il numero di vicini di u che si trovano in P
        archi_verso_P = sum(len(adj[u] & P) for u in C)
        # Calcola AE(C)
        return somma_gradi - archi_interni - archi_verso_P

    # Funzione ricorsiva per espandere le clique
    # C: clique corrente; P: candidati; X: esclusi
    def expand(C, P, X):
        global chiamate_ricorsive
        chiamate_ricorsive += 1

        # Calcola AE(C) [Archi esterni di C]
        AE_C = calcola_AE(C, P)

        # Test per abortire la computazione
        if AE_C > L * (len(C) + len(P)):
            return

        # Sceglie un nodo pivot con il massimo numero di vicini in comune con P
        if P:
            u = max(P, key=lambda x: len(P & adj[x]))
        # Se P è vuoto, non c'è un nodo pivot
        else:
            u = None

        # Itera sui nodi candidati che non sono vicini al pivot 
        for v in list(P - (adj[u] if u else set())):
            # Aggiorna C, P e X
            # Aggiunge v alla clique corrente
            new_C = C + [v]
            # Rimuove v dai candidati e ci lascia solamente i suoi vicini intersecati a P
            new_P = P & adj[v]
            # Aggiorna X con i nodi esclusi
            new_X = X & adj[v]

            # Espande ricorsivamente
            expand(new_C, new_P, new_X)

            # Sposta v da P a X
            P.remove(v)
            X.add(v)

        # Se P e X sono vuoti, verifica se C è L-isolated
        if not P and not X:
            AE_C_finale = calcola_AE(C, set())
            # Se rispetta la condizione di isolamento, aggiungi C alla lista
            if AE_C_finale <= len(C) * L:
                clique_isolated.append(C)

    # Avvia l'espansione con la lista vuota come clique corrente, candidati iniziali e lista vuota per i nodi esclusi
    expand([], candidati_iniziali, set())

    # Restituisce la lista delle clique massimali L-isolated
    return clique_isolated

            
            # **********************************************************************************************************************************
            # *                  ALGORITMO DI RICERCA E FILTRO PER CLIQUE MASSIMALI L-ISOLATED  (VERSIONE 2)                                   *
            # *        (con calcolo dinamico di AE(C), aggiornando il valore somma dei gradi dei nodi in C quando ci si aggiunge v)            *
            # **********************************************************************************************************************************


def trova_clique_massimali_L_isolated2(G, L):
    # Controlla se il grafo è vuoto
    if len(G) == 0:
        print("Il grafo è vuoto. Nessuna clique trovata.")
        return []

    # Crea un dizionario di adiacenza, dove ogni nodo è associato ai suoi vicini
    adj = {u: set(G[u]) for u in G}

    # Inizializza i candidati iniziali con tutti i nodi del grafo
    candidati_iniziali = set(G)

    # Lista per memorizzare le clique massimali L-isolated
    clique_isolated = []

    # Funzione per calcolare AE(C)
    def calcola_AE(somma_gradi, archi_interni, archi_verso_P):
        # Calcola AE(C) utilizzando i parametri aggiornati dinamicamente
        return somma_gradi - archi_interni - archi_verso_P

    # Funzione ricorsiva per espandere le clique
    # C: clique corrente; P: candidati; X: esclusi; somma_gradi: somma dei gradi dei nodi in C
    def expand(C, P, X, somma_gradi):
        global chiamate_ricorsive
        chiamate_ricorsive += 1

        # Calcola AE(C) 
        archi_interni = len(C) * (len(C) - 1)
        archi_verso_P = sum(len(adj[u] & P) for u in C)
        AE_C = calcola_AE(somma_gradi, archi_interni, archi_verso_P)

        # Test per abortire la computazione
        if AE_C > L * (len(C) + len(P)):
            return

        # Sceglie un nodo pivot con il massimo numero di vicini in comune con P
        if P:
            u = max(P, key=lambda x: len(P & adj[x]))
        else:
            u = None

        # Itera sui nodi candidati che non sono vicini al pivot
        for v in list(P - adj[u] if u else set()):
            # Aggiorna i valori
            new_C = C + [v]
            new_P = P & adj[v]
            new_X = X & adj[v]
            new_somma_gradi = somma_gradi + G.degree[v]  # Aggiorna la somma dei gradi aggiungendo il grado di v
        
            # Espande ricorsivamente
            expand(new_C, new_P, new_X, new_somma_gradi)

            # Sposta v da P a X
            P.remove(v)
            X.add(v)

        # Se P e X sono vuoti, verifica se C è L-isolated
        if not P and not X:
            archi_interni_finale = len(C) * (len(C) - 1)
            AE_C_finale = somma_gradi - archi_interni_finale  # Non ci sono più archi verso P quindi archi_verso_P = 0
            # Se rispetta la condizione di isolamento, aggiungi C alla lista
            if AE_C_finale <= len(C) * L:
                clique_isolated.append(C)

    
    # Avvia l'espansione con la lista vuota come clique corrente, candidati iniziali, lista vuota per i nodi esclusi e 0 come valore iniziale della somma dei gradi
    expand([], candidati_iniziali, set(), 0)

    # Restituisce la lista delle clique massimali L-isolated
    return clique_isolated