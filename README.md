# Projeto Telemetria IA (MVP)

Sistema acadêmico para **gerar insights de corrida** a partir de dados de telemetria.  
O MVP foca em **simular “tempo real”** lendo CSV/JSON, processar métricas com Python e expor uma **API/WS** para consumo por um dashboard futuro.

> Estado atual: **estrutura inicial** + `requirements.txt`. Implementações virão nas próximas etapas.

---

## Objetivos do MVP
- Ingerir dados (CSV/JSON) e simular streaming;
- Calcular métricas básicas (ritmo, rpm máx., etc);
- Gerar insights inteligêntes com base nas métricas;
- Gerar reposta de voz dos insights (Piper/Coqui/Kokoro);
- Persistir histórico local (SQLite);

---

## Arquitetura (visão rápida)
- **collect/** — ingesta de telemetria (simulada ou memória compartilhada do simulador).
- **service/** — regra de negócios (análise com pandas/numpy, integração com LLM/TTS).
- **controllers/** — orquestra o fluxo (coleta → análise → insight).
- **api/** — rotas HTTP/WS (FastAPI).
- **infraestrutura/** — DB e repositórios.
- **models/** — modelos de dados (telemetria/insight com Pydantic).

---

## Stack
- **Python 3.11+**, **FastAPI** (HTTP/WS), **Uvicorn** (ASGI)
- **pandas** + **NumPy** (análise)
- **Pydantic** + **pydantic-settings** (modelos e config)
- **SQLAlchemy** + **aiosqlite** (persistência local — opcional)
- **HTTPX** (integrações externas, ex. LLM)
- **pytest** (testes)

## Convenção de Commits

Consulte a [Convenção de Commits](docs/CONVENCAO-DE-COMMITS.md).


## Como rodar

1. Clone o repositório e entre na pasta:
```
git clone git@github.com:SEU_USUARIO/motorsport_elite_finder.git
cd motorsport_elite_finder
```
2. Crie e ative o ambiente virtual (opcional, mas recomendado):

```
python3 -m venv .venv
source .venv/bin/activate
```
3. Instale as dependências:


```bash
pip install -r requirements.txt
```

4. Crie um arquivo .env (copie de .env.example):

```bash
DATABASE_URL=sqlite:///./app.db
API_PREFIX=/api
ENV=dev

```

5. Rode o servidor:

```bash
uvicorn src.projeto.api.main:app --reload
```
---

## Testando a aplicação

### Front-end
Acesse no navegador:  
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)  

Isso abre o `index.html` (SPA com CSS/JS).

### API básica
Você pode testar usando **Postman** ou **curl**.

#### 1. Ping do DB
```bash
curl http://127.0.0.1:8000/api/db/ping
```
#### 2. Criar sessão
```bash
curl -X POST http://127.0.0.1:8000/api/sessoes \
  -H "Content-Type: application/json" \
  -d '{"driver_name":"Piloto Teste","track_name":"Interlagos","vehicle":"GT3"}'
```
#### 3. Inserir telemetria (lote)
```bash
curl -X POST http://127.0.0.1:8000/api/telemetria/batch \
  -H "Content-Type: application/json" \
  -d '[{"sessao_id":1,"rpm":6800,"coolant_temp":92.5},{"sessao_id":1,"rpm":7100,"coolant_temp":93.0}]'
```
#### 4. Listar últimas amostras
```bash
curl "http://127.0.0.1:8000/api/telemetria/ultimas?sessao_id=1&limit=5"
```