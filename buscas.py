# @unisenac - buscas.py
# ============================================================
# AEDII - Trabalho: Rotas do Predio com Grafos
# Etapas 3 e 4 - BFS, DFS, busca gulosa e Dijkstra no grafo do predio
#
# As quatro funcoes tem a MESMA assinatura e o MESMO retorno, exigidos no
# enunciado:
#     caminho, custo, visitados = busca(grafo, origem, destino)
#       caminho   -> lista de portas da origem ate o destino
#       custo     -> soma dos pesos das arestas do caminho
#       visitados -> quantas portas foram examinadas ate achar o destino
#
# A logica e a mesma que usamos no labirinto da aula 9 (BFS = fila, DFS =
# pilha/recursao, gulosa = fila de prioridade pela heuristica). A diferenca
# e que aqui os vizinhos tem PESO (distancia), e por isso tambem calculamos
# o "custo" do caminho, e por isso existe o Dijkstra (que o labirinto nao
# precisava, porque la todo passo "custava" 1).
# ============================================================

from collections import deque   # deque = fila dupla; usamos so o lado "tirar da frente em O(1)" na BFS
import heapq                    # heapq = fila de prioridade; sempre devolve o menor item, usado na gulosa e no Dijkstra

from grafo import carregar_grafo   # importa a funcao que le o arquivo de arestas e monta o dicionario do grafo


def custo_do_caminho(grafo, caminho):                        # funcao auxiliar: soma o peso das arestas de um caminho ja pronto
    total = 0                                                 # comeca o acumulador de custo em zero
    for i in range(len(caminho) - 1):                         # percorre os pares de portas vizinhas no caminho (ultima nao entra, pois nao tem proxima)
        atual, proxima = caminho[i], caminho[i + 1]           # pega a porta atual e a proxima porta do caminho
        for vizinho, peso in grafo[atual]:                    # procura, na lista de vizinhos da porta atual...
            if vizinho == proxima:                            # ...aquele que e exatamente a proxima porta do caminho
                total += peso                                 # soma o peso dessa aresta especifica ao total
                break                                         # ja achou o peso certo, nao precisa continuar procurando
    return total                                              # devolve a soma total dos pesos do caminho


def reconstruir(pai, destino):                        # igual a atividade do labirinto: sobe pelo dicionario "pai" ate o inicio
    caminho = []                                      # lista que vai ser preenchida de tras pra frente (do destino pro inicio)
    v = destino                                        # comeca no destino, que e de onde a gente "sobe"
    while v is not None:                               # repete enquanto ainda existir um "pai" guardado (a origem tem pai None)
        caminho.append(v)                              # guarda a porta atual na lista
        v = pai[v]                                     # troca "v" pelo pai dele, subindo uma porta na cadeia de descobertas
    return caminho[::-1]                               # inverte a lista: agora ela vai da origem ate o destino


# ------------------------------------------------------------
# BFS - busca em largura (acha o caminho com MENOS portas, ignora o peso)
# ------------------------------------------------------------
def bfs(grafo, origem, destino):                       # define a bfs, recebe o grafo, a porta de origem e a de destino
    pai = {origem: None}                               # dicionario de quem descobriu cada porta; a origem nao tem pai (None)
    visitados = []                                     # lista com a ordem em que as portas saíram da fila (foram processadas)
    fila = deque([origem])                             # fila (deque) comeca so com a porta de origem dentro
    while fila:                                        # repete enquanto ainda houver portas pra explorar na fila
        atual = fila.popleft()                         # tira a porta da FRENTE da fila (quem entrou primeiro, sai primeiro)
        visitados.append(atual)                        # registra que essa porta foi visitada agora
        if atual == destino:                           # se essa porta e o destino...
            break                                       # ...ja achamos o caminho com menos arestas possivel, pode parar
        for vizinho, _peso in grafo[atual]:             # percorre os vizinhos da porta atual (o peso nao importa pra BFS)
            if vizinho not in pai:                      # so processa o vizinho se ele ainda nao foi descoberto
                pai[vizinho] = atual                    # marca quem descobriu esse vizinho (evita visitar duas vezes)
                fila.append(vizinho)                    # coloca o vizinho no FIM da fila, pra ser processado depois
    caminho = reconstruir(pai, destino)                 # monta o caminho da origem ate o destino usando o dicionario "pai"
    custo = custo_do_caminho(grafo, caminho)            # calcula o custo real (soma dos pesos) desse caminho encontrado
    return caminho, custo, len(visitados)               # devolve caminho, custo e quantas portas foram visitadas


# ------------------------------------------------------------
# DFS - busca em profundidade (mergulha no primeiro vizinho que encontra)
# ------------------------------------------------------------
def dfs(grafo, origem, destino):                        # define a dfs, recebe o grafo, a origem e o destino
    pai = {origem: None}                                # dicionario de quem descobriu cada porta; origem sem pai
    visitados = []                                      # lista com a ordem em que as portas foram visitadas

    def visitar(atual):                                 # funcao interna recursiva: avanca o mais fundo possivel a partir de "atual"
        visitados.append(atual)                         # registra a visita da porta atual
        if atual == destino:                            # se chegou no destino...
            return True                                 # ...avisa quem chamou (True) pra parar toda a recursao
        for vizinho, _peso in grafo[atual]:              # percorre os vizinhos na ordem em que aparecem no arquivo de arestas
            if vizinho not in pai:                       # so desce por esse vizinho se ele ainda nao foi descoberto
                pai[vizinho] = atual                     # registra que foi "atual" quem descobriu esse vizinho
                if visitar(vizinho):                     # chama a funcao de novo, agora a partir do vizinho (mergulha mais fundo)
                    return True                          # se a chamada de baixo achou o destino, propaga o aviso pra cima
        return False                                     # nenhum vizinho levou ao destino: devolve False (a recursao volta sozinha, backtracking)

    visitar(origem)                                      # dispara a busca recursiva a partir da porta de origem
    caminho = reconstruir(pai, destino)                  # monta o caminho encontrado usando o dicionario "pai"
    custo = custo_do_caminho(grafo, caminho)             # calcula o custo (soma dos pesos) desse caminho
    return caminho, custo, len(visitados)                # devolve caminho, custo e quantas portas foram visitadas


# ------------------------------------------------------------
# Busca gulosa (greedy best-first) - sempre vai pro vizinho mais PERTO
# (olhando so o peso da proxima aresta, sem pensar la na frente)
# ------------------------------------------------------------
def gulosa(grafo, origem, destino):                      # define a busca gulosa, recebe o grafo, a origem e o destino
    pai = {origem: None}                                 # dicionario de quem descobriu cada porta; origem sem pai
    visitados = []                                       # lista com a ordem em que as portas foram expandidas (tiradas da fila)
    # a fila de prioridade guarda (peso_da_aresta_que_levou_ate_aqui, porta)
    fronteira = [(0, origem)]                             # comeca com a origem, "custo pra chegar nela" = 0 (ja estamos nela)
    while fronteira:                                      # repete enquanto houver candidatos na fila de prioridade
        _peso, atual = heapq.heappop(fronteira)           # tira o candidato com MENOR peso de aresta (o "_peso" descarta o valor, so usamos "atual")
        if atual in visitados:                            # como a gulosa pode inserir a mesma porta mais de uma vez na fila...
            continue                                       # ...se ela ja foi visitada antes, ignora essa entrada repetida
        visitados.append(atual)                           # registra a visita da porta atual
        if atual == destino:                               # se chegou no destino...
            break                                           # ...a busca gulosa termina aqui
        for vizinho, peso in grafo[atual]:                  # percorre os vizinhos da porta atual, com o peso de cada aresta
            if vizinho not in pai:                          # so processa o vizinho se ele ainda nao foi descoberto
                pai[vizinho] = atual                        # registra quem descobriu esse vizinho
                heapq.heappush(fronteira, (peso, vizinho))  # insere o vizinho na fila, com prioridade = peso DESSA aresta (olha so 1 passo a frente)
    caminho = reconstruir(pai, destino)                     # monta o caminho encontrado usando "pai"
    custo = custo_do_caminho(grafo, caminho)                # calcula o custo (soma dos pesos) do caminho
    return caminho, custo, len(visitados)                   # devolve caminho, custo e quantas portas foram visitadas


# ------------------------------------------------------------
# Dijkstra - acha o caminho de MENOR custo total (o peso todo importa)
# ------------------------------------------------------------
def dijkstra(grafo, origem, destino):                        # define o dijkstra, recebe o grafo, a origem e o destino
    distancia = {porta: float("inf") for porta in grafo}     # comeca todas as portas com distancia "infinita" (ainda nao sabemos o custo ate elas)
    anterior = {}                                             # dicionario de "de onde eu vim" pra cada porta, pra reconstruir o caminho depois
    distancia[origem] = 0                                     # a origem custa 0 pra chegar nela mesma
    fila = [(0, origem)]                                      # fila de prioridade com (distancia_ate_agora, porta); comeca so com a origem
    finalizadas = set()                                       # conjunto das portas cuja menor distancia ja ficou definitiva (nao muda mais)

    while fila:                                               # repete enquanto houver portas na fila de prioridade
        d, atual = heapq.heappop(fila)                        # tira da fila a porta com MENOR distancia acumulada ate agora
        if atual in finalizadas:                              # se essa porta ja foi finalizada antes (entrou na fila mais de uma vez)...
            continue                                          # ...ignora essa entrada repetida e antiga
        finalizadas.add(atual)                                # marca essa porta como finalizada (sua menor distancia nao muda mais)
        if atual == destino:                                  # se a porta finalizada agora e o destino...
            break                                              # ...ja temos o menor caminho ate ele, pode parar
        for vizinho, peso in grafo[atual]:                     # percorre os vizinhos da porta atual, com o peso de cada aresta
            nova_distancia = d + peso                          # calcula quanto custaria chegar no vizinho passando por "atual"
            if nova_distancia < distancia[vizinho]:             # se esse caminho novo for melhor do que o que a gente ja tinha pro vizinho...
                distancia[vizinho] = nova_distancia             # ...atualiza a menor distancia conhecida ate o vizinho
                anterior[vizinho] = atual                       # ...e anota que foi por "atual" que chegamos nele com esse custo menor
                heapq.heappush(fila, (nova_distancia, vizinho)) # insere o vizinho na fila, com a nova distancia como prioridade

    caminho = [destino]                                         # comeca a reconstrucao do caminho pelo destino
    while caminho[-1] != origem:                                # repete ate a reconstrucao chegar de volta na origem
        caminho.append(anterior[caminho[-1]])                   # adiciona, antes da ultima porta, de onde a gente veio ate ela
    caminho.reverse()                                            # a lista estava do destino pra origem; inverte pra ficar origem -> destino

    return caminho, distancia[destino], len(finalizadas)        # devolve caminho, o custo minimo e quantas portas foram finalizadas


# ------------------------------------------------------------
# Ferramenta extra: acha um par de portas onde a BFS e o Dijkstra
# discordam no CAMINHO (nao so no custo). E a "Tarefa obrigatoria" do
# enunciado: achar esse par no grafo do predio e explicar por que no README.
# ------------------------------------------------------------
def encontrar_par_divergente(grafo):                    # funcao que varre o grafo procurando um par origem/destino divergente
    portas = list(grafo)                                # lista com todas as portas (vertices) do grafo
    for origem in portas:                               # tenta cada porta como origem...
        for destino in portas:                          # ...combinada com cada porta como destino
            if origem == destino:                       # se origem e destino forem a mesma porta...
                continue                                 # ...nao faz sentido comparar, pula
            caminho_bfs, custo_bfs, _ = bfs(grafo, origem, destino)       # roda a BFS pra esse par
            caminho_dij, custo_dij, _ = dijkstra(grafo, origem, destino) # roda o Dijkstra pro mesmo par
            if caminho_bfs != caminho_dij:               # se os dois acharam caminhos DIFERENTES...
                return origem, destino, caminho_bfs, custo_bfs, caminho_dij, custo_dij  # ...achamos nosso par, devolve tudo
    return None                                          # se nao achou nenhum par assim, devolve None (nao deveria acontecer se ha ciclo)


if __name__ == "__main__":                                        # so roda a demonstracao abaixo se este arquivo for executado direto
    grafo = carregar_grafo("arestas.txt")                         # carrega o grafo do predio a partir do arquivo de arestas

    origem, destino = "LABTECH", "206"                             # par de exemplo pra demonstrar as 4 buscas (troque se quiser testar outro)
    for nome, busca in [("BFS", bfs), ("DFS", dfs), ("Gulosa", gulosa), ("Dijkstra", dijkstra)]:  # percorre as 4 buscas
        caminho, custo, visitados = busca(grafo, origem, destino)  # roda a busca atual para o par de exemplo
        print(f"{nome:<8} caminho={caminho}  custo={custo}  visitados={visitados}")  # imprime o resultado formatado

    print()                                                        # linha em branco pra separar
    print("Procurando um par onde BFS e Dijkstra discordam...")     # avisa que vai rodar a varredura completa
    resultado = encontrar_par_divergente(grafo)                    # roda a varredura em todos os pares de portas do grafo
    if resultado:                                                  # se achou um par divergente...
        origem, destino, c_bfs, custo_bfs, c_dij, custo_dij = resultado  # desempacota o resultado encontrado
        print(f"Par achado: {origem} -> {destino}")                 # mostra qual par de portas diverge
        print(f"  BFS:      {c_bfs}  (custo {custo_bfs})")          # mostra o caminho e custo que a BFS encontrou
        print(f"  Dijkstra: {c_dij}  (custo {custo_dij})")          # mostra o caminho e custo que o Dijkstra encontrou
    else:                                                           # se nao achou nenhum par divergente...
        print("Nenhum par divergente encontrado neste grafo.")      # avisa (pode acontecer se o grafo nao tiver ciclo nenhum)
