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
