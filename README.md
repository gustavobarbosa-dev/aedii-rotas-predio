# @unisenac - Trabalho: Rotas do Prédio com Grafos (AEDII)

## Integrantes
- Gustavo Barbosa
- Ryan Garcia
- Giulianna Pereira

## Unidade do peso
As distâncias foram medidas em **passos** (contados porta a porta, sem
acumular — cada aresta tem só a distância entre as duas portas vizinhas).

## Arquivos
- `arestas.txt` — arestas medidas no prédio: `porta porta peso`, uma por linha.
- `grafo.py` — monta a lista de adjacência a partir de `arestas.txt`.
- `buscas.py` — BFS, DFS, busca gulosa e Dijkstra, todas devolvendo `(caminho, custo, visitados)`.
- `api.py` — API FastAPI com os 4 endpoints pedidos.
- `diagramas/` — diagramas do grafo do prédio (draw.io) e a foto do caderno.

## Como rodar

```bash
python3 grafo.py      # confere portas/arestas
python3 buscas.py     # roda as 4 buscas e acha o par divergente
pip install fastapi uvicorn
uvicorn api:app --reload
# depois abrir http://127.0.0.1:8000/docs
```

## Passo 3 — conferência do grafo

`python3 grafo.py` carrega **36 portas e 40 arestas**. A BFS a partir do
`LABTECH` alcança as **36 portas** (nenhuma de fora).

## Tarefa obrigatória — par onde BFS e Dijkstra discordam

Rodando `python3 buscas.py`, a função `encontrar_par_divergente` achou
o par **LABTECH → SALA2**:

- **BFS**: `LABTECH → PATIO1 → PATIO3 → SALA2`, custo **84** (3 arestas).
- **Dijkstra**: `LABTECH → PATIO1 → PATIO3 → BIBLIOTECA → SALA2`, custo **74** (4 arestas).

**Por quê:** existe um ciclo `PATIO3 ↔ BIBLIOTECA ↔ SALA2 ↔ PATIO3`. A
aresta direta `PATIO3–SALA2` tem só 1 aresta de distância (BFS ama isso:
menos arestas = "mais perto"), mas pesa 30 passos. Já o caminho
`PATIO3 → BIBLIOTECA → SALA2` tem 2 arestas, mas custa só 15+5=20 passos —
menos do que a aresta direta. A BFS conta arestas e não enxerga peso,
então fica com a direta (84 no total); o Dijkstra soma os pesos de
verdade e acha o caminho mais barato (74), mesmo com uma porta a mais no
meio.

## Observações sobre pesos estimados

Dois grupos de pesos não apareciam em nenhum dos diagramas e foram
combinados com o Gustavo:

- **LABTECH–PATIO1 = 17** (confirmado no diagrama).
- **Corredor vertical da ala administrativa** (sem peso em nenhum
  diagrama): por decisão do grupo, foi usado o **dobro do peso cruzado
  da mesma linha**:
  - `SECRETARIA–LIDERANCA` = 22 (dobro de `SECRETARIA–PEDAGOGICO`=11)
  - `PEDAGOGICO–COORDENACAO` = 22 (idem)
  - `LIDERANCA–SN1` = 4 (dobro de `LIDERANCA–COORDENACAO`=2)
  - `COORDENACAO–DIRECAO` = 4 (idem)
  - `DIRECAO–PROFESSORES` = 8 (dobro de `SN1–DIRECAO`=4)

  Se alguém conferir essas distâncias de verdade no prédio e os números
  baterem diferente, é só atualizar o `arestas.txt` e rodar
  `python3 buscas.py` de novo pra atualizar os resultados acima.
