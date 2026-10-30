# @unisenac - grafo.py
# ============================================================
# AEDII - Trabalho: Rotas do Predio com Grafos
# Etapa 2 - Lista de adjacencia
#
# Este arquivo pega o arquivo "arestas.txt" (as arestas que a gente mediu
# andando pelo predio) e monta o grafo em Python, no formato de
# "lista de adjacencia": um dicionario onde cada porta aponta pra uma lista
# de (vizinho, peso).
#
# Cada linha do codigo abaixo tem um comentario explicando o que ela faz,
# igual a gente fez na atividade do labirinto (aula 9).
# ============================================================


def carregar_grafo(caminho):                         # define a funcao que le o arquivo de arestas e devolve o grafo pronto
    grafo = {}                                       # dicionario vazio: vai virar a lista de adjacencia (porta -> lista de vizinhos)
    with open(caminho, encoding="utf-8") as arq:     # abre o arquivo de arestas em modo leitura, usando utf-8 (por causa de acentos)
        for linha in arq:                            # percorre o arquivo linha por linha
            linha = linha.strip()                    # tira espacos e quebra de linha do inicio/fim, pra facilitar os testes abaixo
            if not linha:                             # se a linha ficou vazia (era so uma linha em branco)...
                continue                              # ...pula pra proxima linha, nao tenta processar
            if linha.startswith("#"):                 # se a linha comeca com "#", e um comentario/nota nossa (ex: "CONFERIR")
                continue                              # ...entao tambem pula, nao e uma aresta de verdade
            a, b, peso = linha.split()                # quebra a linha em 3 pedacos pelos espacos: porta A, porta B e o peso
            peso = int(peso)                          # o peso vem como texto ("20"); converte pra numero inteiro de verdade
            grafo.setdefault(a, []).append((b, peso)) # garante que "a" existe no dicionario (lista vazia se for a primeira vez) e adiciona o vizinho b
            grafo.setdefault(b, []).append((a, peso)) # faz o mesmo no sentido contrario: de b tambem da pra chegar em a (anda nos dois sentidos)
    return grafo                                      # devolve o dicionario completo, com todas as portas e seus vizinhos


def resumo_do_grafo(grafo):                           # funcao extra (nao pedida, mas ajuda a conferir o grafo) - "Passo 3: confiram o grafo"
    n_portas = len(grafo)                             # numero de chaves do dicionario = numero de portas (vertices) do grafo
    n_arestas = sum(len(vizinhos) for vizinhos in grafo.values()) // 2  # soma todos os vizinhos e divide por 2 (cada aresta foi contada 2x, uma vez de cada lado)
    return n_portas, n_arestas                        # devolve os dois numeros, pra comparar com o desenho do caderno


if __name__ == "__main__":                            # so roda o bloco abaixo se este arquivo for executado diretamente (nao quando for importado)
    grafo = carregar_grafo("arestas.txt")             # carrega o grafo do arquivo de arestas que esta na mesma pasta
    portas, arestas = resumo_do_grafo(grafo)           # calcula quantas portas e quantas arestas o grafo tem
    print(f"Portas carregadas: {portas}")              # mostra o numero de portas encontradas
    print(f"Arestas carregadas: {arestas}")             # mostra o numero de arestas encontradas
    print()                                            # linha em branco, so pra separar visualmente
    for porta in sorted(grafo):                        # percorre as portas em ordem alfabetica, pra ficar facil de ler
        vizinhos = ", ".join(f"{p}({peso})" for p, peso in grafo[porta])  # monta um texto tipo "202(20), CANTINA(10)" com todos os vizinhos e pesos
        print(f"{porta:<12} -> {vizinhos}")             # imprime a porta e a lista de vizinhos formatada
