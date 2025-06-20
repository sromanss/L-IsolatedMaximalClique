import networkx as nx

           
            
# ************************************************************************************************************
# *                                ALGORITMO DI RICERCA STANDARD DA NETWORKX                                 *
# ************************************************************************************************************
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


# ************************************************************************************************************
# *                      VERSIONE ALTERNATIVA SENZA POSSIBILITA' DI FORNIRE CLIQUE INIZIALE                  *
# ************************************************************************************************************
def trova_clique_massimali2(G):
    num_chiamate = 0  # Contatore locale per le chiamate ricorsive
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
        
        # Sceglie un nodo pivot con il massimo numero di vicini in comune con cand
        u = max(subg, key=lambda u: len(cand & adj[u]))
        
        # Itera sui nodi candidati che non sono vicini al pivot
        for q in list(cand - adj[u]):  # Usa una copia per evitare modifiche durante l'iterazione
            nonlocal num_chiamate
            num_chiamate += 1  # Conta la chiamata alla funzione
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

    # Ottieni le clique e converti il generatore in lista
    cliques = list(expand(cand_init, cand_init.copy(), []))

    # Avvia l'espansione con il sottografo e i candidati iniziali
    return cliques, num_chiamate


# ************************************************************************************************************
# *                              ALGORITMO DI FILTRO PER TROVARE CLIQUES L-ISOLATED                          *
# ************************************************************************************************************       
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


# ************************************************************************************************************
# *                   ALGORITMO DI RICERCA DI CLIQUES L-ISOLATED CON EURISTICA PER CALCOLO DI D              *
# *     (e = 1 -> D = len(P); e = 2 -> D = 1 + grado_massimo_sottografoDiP; e = 3 -> maxGradiOrdinati)       *
# ************************************************************************************************************
def trova_clique_massimali_L_isolated(G, L, euristica):

    # Contatore locale per le chiamate ricorsive
    num_chiamate = 0

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

    # Funzione per calcolare D
    def calcola_D(C, P, euristica):
        if euristica == 1:
            return len(P)
        elif euristica == 2:
            # Calcola il grafo indotto da P
            sottografo = G.subgraph(P)
            # Trova il grado massimo del grafo indotto
            grado_massimo = max((sottografo.degree(v) for v in sottografo), default=0)
            return 1 + grado_massimo
        elif euristica == 3:
            # Ordina i nodi di P in ordine decrescente di grado
            gradi = sorted((G.degree[v] for v in P), reverse=True)
            # Trova il massimo numero D di nodi che hanno grado >= D-1
            for i, grado in enumerate(gradi, start=1):
                if grado < i - 1:
                    return i - 1
            return len(gradi) # Se tutti i nodi soddisfano la condizione
        
        else:
            raise ValueError("Euristica non valida per il calcolo di D.")

    # Funzione ricorsiva per espandere le clique
    def expand(C, P, X, somma_gradi):
        nonlocal num_chiamate
        num_chiamate += 1

        # Calcola AE(C)
        archi_interni = len(C) * (len(C) - 1)
        archi_verso_P = sum(len(adj[u] & P) for u in C)
        AE_C = calcola_AE(somma_gradi, archi_interni, archi_verso_P)

        # Calcola D usando l'euristica specificata
        D = calcola_D(C, P, euristica)

        # Test per abortire la computazione AE(C) + |C||P| - L|C| > D(L+|C|).
        if AE_C + len(C)*len(P) - L*len(C) > D*(L + len(C)):
        #if AE_C > L * (len(C) + D):
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
    return clique_isolated, num_chiamate


# ************************************************************************************************************
# *           ALGORITMO DI RICERCA DI CLIQUES L-ISOLATED CON EURISTICA PER CALCOLO DI D (versione 2)         *
# ************************************************************************************************************
def trova_clique_massimali_L_isolated2(G, L, euristica):
    
    # Contatore locale per le chiamate ricorsive
    num_chiamate = 0

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

    # Funzione per calcolare D
    def calcola_D(C, P, euristica):
        if euristica == 1:
            return len(P)
        elif euristica == 2:
            # Trova il grado massimo del grafo indotto
            # grado_massimo = max((sottografo.degree(v) for v in P), default=0)
            grado_massimo = max((G.degree(v) for v in P), default=0) 
            return min(max(0, grado_massimo - len(C) + 1), len(P))
        elif euristica == 3:
            # Ordina i nodi del sottografo in ordine decrescente di grado
            # gradi = sorted((sottografo.degree[v] for v in P), reverse=True)
            gradi = sorted((G.degree[v] for v in P), reverse=True)
            # Trova il massimo numero D di nodi che hanno grado >= D-1
            for i, grado in enumerate(gradi, start=1):
                #if grado < i - 1:
                if grado - len(C) < i - 1:
                    return i - 1
            return len(gradi) # Se tutti i nodi soddisfano la condizione
        elif euristica==4:
            # 4.1) Creo una lista L con tanti elementi quanti i nodi di P, che contiene per ogni nodo di P, il grado del nodo (in G) meno len(C)
            L = [G.degree[v] - len(C) for v in P]
            if not L:  # Se P è vuoto
                return 0
            # 4.2) Mi calcolo il grado massimo nella lista sopra e creo un array di contatori C[grado] indicizzato sul grado dei nodi e inizializzato con zeri.
            grado_max = max(L)
            C = [0] * (grado_max + 1)  # +1 per includere lo zero
            # 4.3) Itero sulla lista L dei gradi e incremento il contatore C[grado] in base al grado del nodo corrente.
            for grado in L:
                C[grado] += 1   
            # 4.4)  Itero sui contatori al contrario (partendo dal contatore del grado massimo) e sommo il numero dei nodi trovati fino ad adesso
            # All'inizio considero grado=gradoMax e somma=C[gradoMax]
            somma = C[grado_max]
            for grado in range(grado_max-1, -1, -1): #inizia da grado_max-1 fino a 0, decrementando di 1
                # Se il grado_corrente < somma-1 allora ritorno somma all'iterazione precedente 
                if grado < somma - 1:
                    return somma
                somma += C[grado]
            return somma
        else:
            raise ValueError("Euristica non valida per il calcolo di D.")
    
    def expand_simple(C, P, X, somma_gradi):
        nonlocal num_chiamate
        num_chiamate += 1

        # Calcola AE(C)
        archi_interni = len(C) * (len(C) - 1)
        archi_verso_P = sum(len(adj[u] & P) for u in C)
        AE_C = calcola_AE(somma_gradi, archi_interni, archi_verso_P)
        
        D = calcola_D(C, P, euristica)  # D è uguale alla lunghezza di P

        if AE_C + len(C)*len(P) - L*len(C) > D*(L + len(C)):
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
            expand_simple(new_C, new_P, new_X, new_somma_gradi)

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
    
    # Funzione ricorsiva per espandere le clique
    def expand(C, P, X, somma_gradi, sottografo):
        nonlocal num_chiamate
        num_chiamate += 1

        # Calcola AE(C)
        archi_interni = len(C) * (len(C) - 1)
        archi_verso_P = sum(len(adj[u] & P) for u in C)
        AE_C = calcola_AE(somma_gradi, archi_interni, archi_verso_P)

        # Calcola D usando l'euristica specificata
        D = calcola_D(C, P, euristica, sottografo)
        
        # Test per abortire la computazione AE(C) + |C||P| - L|C| > D(L+|C|).
        if AE_C + len(C)*len(P) - L*len(C) > D*(L + len(C)):
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
            #new_sottografo = sottografo.subgraph(new_P)
            new_sottografo = G.subgraph(new_P) 
            #new_sottografo = G.subgraph(new_P).copy()  # Aggiorna il sottografo indotto
            
            # Espande ricorsivamente
            expand(new_C, new_P, new_X, new_somma_gradi, new_sottografo)

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

    expand_simple([], candidati_iniziali, set(), 0)
    # In base al valore dell'euristica, chiama la funzione di espansione appropriata
    #if (euristica == 1):
    #    expand_simple([], candidati_iniziali, set(), 0)
    #else:
    #    sottografo_iniziale = G.subgraph(candidati_iniziali)  
    #    #sottografo_iniziale = G.subgraph(candidati_iniziali).copy()
    #    expand([], candidati_iniziali, set(), 0, sottografo_iniziale)

    # Restituisce la lista delle clique massimali L-isolated
    return clique_isolated, num_chiamate


# ************************************************************************************************************
# *                     VERIFICA CHE DUE LISTE DI CLIQUES CONTENGANO LE STESSE CLIQUES                       *
# ************************************************************************************************************
def verifica_cliques_isolate(cliques1, cliques2):
    
    # Converte le clique in insiemi per ignorare l'ordine dei nodi
    set_cliques1 = {frozenset(clique) for clique in cliques1}
    set_cliques2 = {frozenset(clique) for clique in cliques2}

    # Confronta i due insiemi
    return set_cliques1 == set_cliques2

# ************************************************************************************************************
# ************************************************************************************************************

def trova_clique_massimali3(G):
    # Contatore per le chiamate ricorsive
    num_chiamate = 0

    # Controlla se il grafo è vuoto
    if len(G) == 0:
        print("Il grafo è vuoto. Nessuna clique trovata.")
        return [], 0

    # Crea un dizionario di adiacenza, dove ogni nodo è associato ai suoi vicini
    adj = {u: set(G[u]) for u in G}

    # Inizializza i candidati iniziali con tutti i nodi del grafo
    candidati_iniziali = set(G)

    # Lista per memorizzare le clique massimali
    clique_massimali = []

    # Funzione ricorsiva per espandere le clique (algoritmo Bron-Kerbosch)
    def expand(C, P, X):
        nonlocal num_chiamate
        num_chiamate += 1  # Incrementa il contatore delle chiamate ricorsive

         # Sceglie un nodo pivot con il massimo numero di vicini in comune con P
        if P:
            u = max(P, key=lambda x: len(P & adj[x]))
        else:
            u = None

        # Itera sui nodi candidati
        for v in list(P-adj[u] if u else set()):  
            # Aggiorna i valori di P e X
            new_C = C + [v]
            new_P = P & adj[v]
            new_X = X & adj[v]

            # Espande ricorsivamente
            expand(new_C, new_P, new_X)

            # Sposta v da P a X (implementa il backtracking)
            P.remove(v)
            X.add(v)
        
        if not P and not X:
            # Se P e X sono vuoti, aggiungi la clique corrente a clique_massimali
            clique_massimali.append(C)

    # Avvia l'espansione con la lista vuota come clique corrente, candidati iniziali e nessun nodo escluso
    expand([], candidati_iniziali, set())

    # Restituisce la lista delle clique massimali e il numero di chiamate ricorsive
    return clique_massimali, num_chiamate


# ************************************************************************************************************

def trova_clique_massimali_L_isolated3(G, L, euristica):
    # Contatore locale per le chiamate ricorsive
    num_chiamate = 0

    # Controlla se il grafo è vuoto
    if len(G) == 0:
        print("Il grafo è vuoto. Nessuna clique trovata.")
        return [], 0
    
    # Pre-calcolo dei gradi e della cache
    gradi = {node: G.degree[node] for node in G}
    cache_D = {}
    
    # Crea un dizionario di adiacenza, dove ogni nodo è associato ai suoi vicini
    adj = {u: set(G[u]) for u in G}

    # Inizializza i candidati iniziali con tutti i nodi del grafo
    candidati_iniziali = set(G)

    # Lista per memorizzare le clique massimali L-isolated
    clique_isolated = []

    # Funzione ottimizzata per calcolare AE(C)
    def calcola_AE(somma_gradi, archi_interni, archi_verso_P):
        return somma_gradi - archi_interni - archi_verso_P

    # Funzione ottimizzata per calcolare D con caching
    def calcola_D(C, P, euristica):
        key = (len(C), len(P))
        if key in cache_D:
            return cache_D[key]

        result = 0
        if euristica == 1:
            result = len(P)
        elif euristica == 2:
            grado_massimo = max(gradi[v] for v in P)
            result = min(max(0, grado_massimo - len(C) + 1), len(P))
        elif euristica == 3:
            gradi_ordinati = sorted((gradi[v] - len(C) for v in P), reverse=True)
            for i, grado in enumerate(gradi_ordinati, start=1):
                if grado < i - 1:
                    result = i - 1
                    break
            result = len(gradi_ordinati)
        elif euristica == 4:
            L = [gradi[v] - len(C) for v in P]
            grado_max = max(L) if L else 0
            C_count = [0] * (grado_max + 1)
            for grado in L:
                C_count[grado] += 1
            somma = C_count[grado_max]
            for grado in range(grado_max-1, -1, -1):
                if grado < somma - 1:
                    result = somma
                    break
                somma += C_count[grado]
            else:
                result = somma
        else:
            raise ValueError("Euristica non valida per il calcolo di D.")

        cache_D[key] = result
        return result

    def expand_optimized(C, P, X, somma_gradi):
        nonlocal num_chiamate
        num_chiamate += 1

        # Early pruning
        if len(P) == 0:
            if len(X) == 0:
                archi_interni_finale = len(C) * (len(C) - 1)
                AE_C_finale = somma_gradi - archi_interni_finale
                if AE_C_finale <= len(C) * L:
                    clique_isolated.append(C[:])
            return

        # Calcoli base
        archi_interni = len(C) * (len(C) - 1)
        archi_verso_P = sum(len(adj[u] & P) for u in C)
        AE_C = calcola_AE(somma_gradi, archi_interni, archi_verso_P)


        D = calcola_D(C, P, euristica)

        if AE_C + len(C)*len(P) - L*len(C) > D*(L + len(C)):
            return

        # Ottimizzazione scelta pivot
        if len(P) < 10:
            u = next(iter(P))
        else:
            u = max(P, key=lambda x: len(P & adj[x]))

        # Itera sui nodi candidati
        for v in list(P - adj[u] if u else set()):
            new_C = C + [v]
            new_P = P & adj[v]
            new_X = X & adj[v]
            new_somma_gradi = somma_gradi + gradi[v]

            expand_optimized(new_C, new_P, new_X, new_somma_gradi)

            P.remove(v)
            X.add(v)

    # Avvia l'espansione con la configurazione iniziale
    expand_optimized([], candidati_iniziali, set(), 0)

    return clique_isolated, num_chiamate