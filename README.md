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
o par **LABTECH → DIRECAO**:

- **BFS**: `LABTECH → PATIO1 → PATIO3 → BIBLIOTECA → PROFESSORES → DIRECAO`,
  custo **107** (5 arestas).
- **Dijkstra**: `LABTECH → PATIO1 → PORTA2CANTINA → PORTA1CANTINA → LIDERANCA → COORDENACAO → DIRECAO`,
  custo **80** (6 arestas).

**Por quê:** a BFS só conta quantas portas (arestas) tem no caminho, não o
quanto cada uma pesa. O caminho pela biblioteca (`PATIO1 → PATIO3 →
BIBLIOTECA → PROFESSORES → DIRECAO`) tem uma aresta a menos (5 contra 6),
então a BFS prefere ele — só que essas 5 arestas são bem pesadas
(37+30+15+8 = 90, +17 do LABTECH–PATIO1 = 107 no total). Já o caminho
pela cantina (`PATIO1 → PORTA2CANTINA → PORTA1CANTINA → LIDERANCA →
COORDENACAO → DIRECAO`) tem uma porta a mais, mas todas as arestas são
leves (33+9+15+2+4 = 63, +17 = 80 no total) — menos passos no fim. A
Dijkstra soma os pesos de verdade e acha esse caminho mais barato (80),
mesmo tendo mais portas no meio.

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
