# ParkSim — Sistema Simulador de Estacionamento Inteligente (A3)

Projeto acadêmico da disciplina **Gestão e Qualidade de Software** — UNA Barreiro
**Professor:** Daniel Henrique Matos de Paiva

## Equipe
| Integrante | RA |
|---|---|
| João Vitor | 32513480 |
| Rafael Luiz Ferreira de Souza | 32511503 |
| Pietro Cardoso de Oliveira | 32515280 |

## Problema e solução
Estacionamentos reais sofrem com falta de visibilidade do fluxo de vagas. O ParkSim simula esse fluxo (entrada, permanência e saída de veículos) com persistência real em PostgreSQL (Supabase), backend em **Python (FastAPI)**, testes unitários (TDD) e CI via GitHub Actions. Projeto vinculado à **ODS 11 — Cidades e Comunidades Sustentáveis**.

## Arquitetura (3 camadas)
Navegador (JS) → API Python (FastAPI) → Supabase (PostgreSQL)

## Estrutura de arquivos
- `index.html` / `style.css` — interface da simulação e tema responsivo;
- `js/app.js` — orquestrador (eventos, auth, limpeza do banco);
- `js/simulacao.js` — motor da simulação (requestAnimationFrame, spawn adaptativo);
- `js/ui.js` — DOM, animações (WAAPI), relatório e exportação de PDF;
- `js/banco.js` — camada de dados do front (chamadas fetch à API Python);
- `js/config.js` — constantes da simulação e URL da API;
- `backend/app/main.py` — API FastAPI (endpoints, auth JWT, tratamento de erros);
- `backend/app/regras.py` — regras de negócio puras (validações e cálculos, alvo do TDD);
- `backend/app/repositorio.py` — acesso a dados (Supabase/PostgreSQL);
- `backend/app/schemas.py` — modelos Pydantic de entrada/saída;
- `backend/app/config.py` — variáveis de ambiente (.env);
- `backend/tests/` — testes unitários e de integração (pytest);
- `.github/workflows/ci.yml` — Continuous Integration (roda pytest a cada push/PR).

## Como executar
1. Backend: `cd backend && python -m venv .venv && pip install -r requirements.txt`;
2. Crie `backend/.env` com `SUPABASE_URL` e `SUPABASE_SERVICE_KEY`;
3. Testes: `python -m pytest -v`;
4. Suba a API: `uvicorn app.main:app --reload --port 8000`;
5. Frontend: abra `index.html` com Live Server (VS Code) ou `npx serve`.

## Versionamento
GitFlow (main, develop, feature/*), commits semânticos (feat, fix, test, ci, docs) e PR com aprovação de 1 integrante.

## Fluxo de entrega
As branches `feature/*` devem ser integradas em `develop` por Pull Request após a execução do CI. A entrega final segue por Pull Request de `develop` para `main`, mantendo o histórico de revisão e validação no GitHub.
