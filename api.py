# @unisenac - api.py
# ============================================================
# AEDII - Trabalho: Rotas do Predio com Grafos
# Etapa 5 - API com FastAPI
#
# Expoe o grafo do predio por HTTP. Pra rodar:
#   pip install fastapi uvicorn
#   uvicorn api:app --reload
# Depois abra http://127.0.0.1:8000/docs pra testar cada endpoint.
# ============================================================

from fastapi import FastAPI, HTTPException     # FastAPI monta a API; HTTPException devolve erros HTTP (ex: 404) do jeito certo

from grafo import carregar_grafo                 # funcao que le o arquivo de arestas e monta o dicionario do grafo
from buscas import bfs, dfs, gulosa, dijkstra    # as 4 funcoes de busca, todas com a mesma assinatura (grafo, origem, destino)

app = FastAPI()                                  # cria a aplicacao FastAPI (e o objeto que o uvicorn vai rodar)
grafo = carregar_grafo("arestas.txt")            # carrega o grafo do predio UMA VEZ, quando a API sobe (fica guardado em memoria)

# dicionario que liga o nome do algoritmo (texto que vem na URL) com a funcao de verdade
ALGORITMOS = {                                   # assim o endpoint /rota consegue escolher a funcao certa a partir de uma string
    "bfs": bfs,                                  # "bfs" na URL chama a funcao bfs
    "dfs": dfs,                                  # "dfs" na URL chama a funcao dfs
    "gulosa": gulosa,                            # "gulosa" na URL chama a funcao gulosa
    "dijkstra": dijkstra,                        # "dijkstra" na URL chama a funcao dijkstra
}


@app.get("/portas")                              # define o endpoint GET /portas
def portas():                                    # funcao chamada quando alguem acessa /portas
    return sorted(grafo.keys())                  # devolve todas as portas (chaves do dicionario) em ordem alfabetica


@app.get("/vizinhos/{porta}")                    # define o endpoint GET /vizinhos/{porta}, onde {porta} vem da URL
def vizinhos(porta: str):                        # funcao chamada com o valor de {porta} ja como texto (str)
    if porta not in grafo:                       # se a porta pedida nao existe no grafo...
        raise HTTPException(404, "Porta nao encontrada")  # ...devolve erro 404 com essa mensagem, como pedido no enunciado
    return [{"porta": p, "peso": peso} for p, peso in grafo[porta]]  # devolve a lista de vizinhos dessa porta, com o peso de cada aresta


@app.get("/rota")                                                    # define o endpoint GET /rota
def rota(origem: str, destino: str, algoritmo: str):                  # os 3 parametros vem como "?origem=...&destino=...&algoritmo=..." na URL
    if origem not in grafo or destino not in grafo:                   # se a origem ou o destino nao existirem no grafo...
        raise HTTPException(404, "Porta nao encontrada")               # ...devolve erro 404
    if algoritmo not in ALGORITMOS:                                   # se o nome do algoritmo pedido nao for um dos 4 que a gente tem...
        raise HTTPException(400, "Algoritmo invalido. Use: bfs, dfs, gulosa ou dijkstra")  # ...devolve erro 400 (pedido invalido)

    busca = ALGORITMOS[algoritmo]                                     # pega a funcao de verdade correspondente ao nome pedido
    caminho, custo, visitados = busca(grafo, origem, destino)          # roda a busca escolhida para o par origem/destino

    return {                                                           # monta a resposta no formato pedido pelo enunciado
        "algoritmo": algoritmo,                                        # devolve de volta qual algoritmo foi usado
        "caminho": caminho,                                            # a lista de portas do caminho encontrado
        "custo": custo,                                                # a soma dos pesos do caminho
        "unidade": "passos",                                          # a unidade usada nas medidas (ver README)
        "visitados": visitados,                                        # quantas portas foram examinadas ate achar o destino
    }


@app.get("/comparar")                                                  # define o endpoint GET /comparar
def comparar(origem: str, destino: str):                               # recebe origem e destino como "?origem=...&destino=..." na URL
    if origem not in grafo or destino not in grafo:                    # se a origem ou o destino nao existirem no grafo...
        raise HTTPException(404, "Porta nao encontrada")                # ...devolve erro 404

    resultado = {}                                                      # dicionario que vai juntar o resultado dos 4 algoritmos
    for nome, busca in ALGORITMOS.items():                              # percorre os 4 algoritmos (bfs, dfs, gulosa, dijkstra)
        caminho, custo, visitados = busca(grafo, origem, destino)       # roda cada algoritmo para o mesmo par origem/destino
        resultado[nome] = {                                             # guarda o resultado desse algoritmo dentro do dicionario final
            "caminho": caminho,                                        # caminho encontrado por esse algoritmo
            "custo": custo,                                            # custo (soma dos pesos) desse caminho
            "visitados": visitados,                                    # quantas portas esse algoritmo examinou
        }
    return resultado                                                    # devolve os 4 resultados lado a lado, como pedido no enunciado
