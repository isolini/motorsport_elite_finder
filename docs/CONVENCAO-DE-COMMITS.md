# Convenção de Commits e Fluxo de Git — Projeto Telemetria IA

Padronizamos **mensagens de commit** e **fluxo de colaboração** para manter o histórico limpo, facilitar revisão e habilitar automações (changelog/versão).  
Este único documento define **formato de commit**, **tipos/escopos**, **breaking changes** e as **regras práticas de branches/PR/Squash & Merge**.

---

## 1) Formato obrigatório

**Estrutura exata:**

```
<tipo>(<escopo opcional>): <descrição curta no imperativo>

[corpo opcional — o que mudou e por quê]

[rodapé(s) opcional(is) — "Closes #123", "BREAKING CHANGE: ...", "Co-authored-by: ..."]
```

**Regras:**
- **Título (1ª linha)**: até ~72 caracteres, em **voz imperativa** (“adiciona”, “corrige”, “atualiza”).
- **Linha em branco** entre título e corpo.
- **Corpo**: explique o **porquê** e o **contexto** da mudança (não só o “o quê”).
- **Rodapé (opcional)**: issues, avisos de *breaking change*, coautorias etc.

---

## 2) Tipos permitidos

- **feat**: nova funcionalidade.  
- **fix**: correção de bug.  
- **docs**: documentação (README, guias, comentários extensos).  
- **style**: formatação/estilo (linters, espaços), **sem** alterar lógica.  
- **refactor**: refatoração **sem** nova feature ou correção de bug.  
- **test**: inclusão/ajuste de testes.  
- **build**: mudanças de build, dependências, empacotamento (pip/poetry/docker).  
- **chore**: manutenção, tarefas diversas sem impacto de runtime (ex.: renomear pastas, primeiro commit).

> atualizações de dependências usar `chore(deps): ...`.

---

## 3) Escopos

Escolha **um** escopo curto e consistente por commit (crie novos só quando necessário). Exemplos usuais:
`api`, `collect`, `controllers`, `service`, `models`, `infra`, `db`, `websocket`, `ia`, `tts`, `docker`, `tests`, `docs`

Ex.:  

```
feat(service): cálculo de métricas de ritmo
```

---

## 4) Breaking changes

```
Mudanças que quebram compatibilidade (API/contrato/ambiente) **devem** ser explícitas.
```

**Opção A — Exclamação no tipo:**

```
feat!: altera contrato do endpoint /insights
```

**Opção B — Rodapé obrigatório:**

```
BREAKING CHANGE: /insights agora exige header X-Session-ID
```

> Pode usar **ambos** para máxima visibilidade. Descreva impacto e migração.

---

## 5) Boas práticas

- Evitar títulos genéricos (“ajustes”, “mudanças diversas”).  
- **Uma mudança por commit** (evitar commits gigantes).  
- Commits pequenos/atômicos ajudam no review e rollback.  
- Em PRs (pull request) com **Squash & Merge**, garanta que o **título do PR** siga este padrão (ele vira a mensagem final).

---

## 6) Exemplos

**feature (curto)**

```
feat(api): adiciona endpoint GET /corrida/health
```

**fix (com corpo)**

```
fix(service): corrige normalização do rpm máximo

A função calcular_metricas falhava com CSVs sem coluna "rpm".
Agora usamos fallback seguro para rpm_max.
```


**refactor**

```
refactor(models): simplifica Telemetria removendo campo setor_opcional
```

**docs**

```
docs(readme): instruções de execução com Docker
```

**build**

```
build(docker): ajusta base python:3.11-slim e cache do pip
```

**breaking change**

```
feat!: renomeia rota /insights para /v1/insights

BREAKING CHANGE: clientes devem atualizar a URL da API
```

---

## 7) Normas de branching

### 7.1 Padrão de branches
- **main**: estável, pronta para release/demonstração.  
- **dev** (opcional): integração antes de ir para `main`.  
- **feature/<tópico>**: desenvolvimento de features.  
- **fix/<tópico>**: correções de bugs.  
- **chore/<tópico>**: manutenção/infra.

**Exemplos:**

```
feature/ingestao-csv
```
```
fix/ws-timeout
```
```
chore/atualiza-deps
```


### 7.2 Fluxo básico (local)

```
# atualizar a main

git fetch origin
git switch main
git pull
# criar e trabalhar em uma feature

git switch -c feature/<topico>
# ... edições ...

git add -A
git commit -m "feat(service): leitura CSV inicial"
git push -u origin feature/<topico>
```

### 7.3 Manter a branch atualizada (rebase)
Antes do PR, rebaseie sua branch sobre a `main` para reduzir conflitos:

```
git fetch origin
git switch feature/<topico>
git rebase origin/main
# resolva conflitos se houver -> git add <arquivos> && git rebase --continue

git push -f # após rebase, normalmente precisa --force-with-lease
```

> Preferimos **rebase** (histórico linear). Se optar por merge local, mantenha mensagens claras.

---

## 8) Pull Request (PR)

1. Abra PR: **Base** = `main` (ou `dev`) ← **Compare** = sua branch.  
2. **Título do PR** no formato de commit (será usado no Squash & Merge).  
3. Descreva **o que** mudou e **por que** (contexto, riscos, testes).  
4. Marque revisores e ajuste conforme feedback.

---

## 9) Squash & Merge

- Use **“Squash and merge”** no PR para transformar todos os commits em **um único commit** na `main`.
- **Edite a mensagem final** para o formato de commit (inclua `Closes #123` quando aplicável).

**Vantagens:**
- Histórico limpo: 1 PR = 1 commit.  
- Remove ruído de commits intermediários (“wip”, “typo”).  
- O PR continua linkado se precisar consultar os detalhes.

---

## 10) TL;DR

- **Commits**: `tipo(escopo): descrição` + corpo + rodapé.  
- **Tipos**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `build`, `chore`.  
- **Breaking**: `!` no tipo e/ou `BREAKING CHANGE:` no rodapé.  
- **Branches**: `main` estável; crie `feature/<topico>`, rebaseie, PR, **Squash & Merge**.  
- **PR**: título no padrão de commit; review obrigatório; CI verde.