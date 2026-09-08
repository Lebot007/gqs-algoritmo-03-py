# DOSSIÊ DE VALIDAÇÃO TÉCNICA
## ParkSim — Sistema Simulador de Estacionamento Inteligente (A3)

**Disciplina:** Gestão e Qualidade de Software  
**Professor:** Daniel Henrique Matos de Paiva  
**Instituição:** UNA Barreiro  
**Data da auditoria:** 07/09/2026

### Equipe

| Integrante | RA |
|---|---|
| João Vitor | 32513480 |
| Rafael Luiz Ferreira de Souza | 32511503 |
| Pietro Cardoso de Oliveira | 32515280 |

---

## 1. Resumo executivo

A auditoria confrontou o código e a documentação local do ParkSim com o PDF **01.avaliacao_a3.pdf**, considerando somente evidências disponíveis na entrega local. Itens que dependem de publicação no GitHub ou de histórico remoto não foram considerados comprovados.

| Classificação | Quantidade | Percentual |
|---|---:|---:|
| ✅ Atendido | 8 | 57,1% |
| ⚠️ Parcial | 4 | 28,6% |
| ⏳ Pendente de upload | 2 | 14,3% |
| **Total** | **14** | **100%** |

**Conclusão executiva:** o projeto está **apto com ressalvas**. A base técnica atende aos principais requisitos de código, testes, API, banco e tratamento de erros. Antes da entrega final, é necessário comprovar o repositório remoto, completar os entregáveis acadêmicos e documentar a estrutura SQL do banco.

---

## 2. Matriz de validação

| Critério do professor | Exigência | Status | Evidência | Observações |
|---|---|---|---|---|
| 1. Solução em Python | Usar C#, Java ou Python | ✅ **ATENDIDO** | `backend/app/main.py`: criação da aplicação FastAPI e endpoints; `backend/app/regras.py`: regras de negócio Python | A solução principal do backend está escrita em Python. |
| 2. Indentação dos algoritmos | Código devidamente indentado | ✅ **ATENDIDO** | `backend/app/main.py`, `backend/app/regras.py`, `backend/tests/`: funções e classes com blocos indentados | A organização segue o padrão esperado de Python. Não foi executado um linter PEP 8 formal nesta auditoria. |
| 3. Nome e RA dos integrantes | Identificar todos os integrantes na entrega | ✅ **ATENDIDO** | `README.md`, seção **Equipe** | Os três integrantes e respectivos RAs estão identificados. |
| 4. Problema do mundo real | Resolver ou refatorar solução para problema real | ✅ **ATENDIDO** | `README.md`, seção **Problema e solução** | O problema declarado é a falta de visibilidade do fluxo de vagas em estacionamentos. |
| 5. Associação a uma ODS | Associar a solução a uma ODS com justificativa coerente | ✅ **ATENDIDO** | `README.md`: ODS 11; `backend/app/main.py`: descrição da API vinculada à ODS 11 | A associação com Cidades e Comunidades Sustentáveis é coerente com o tema de mobilidade/gestão urbana. |
| 6. Clean Code | Nomes claros, funções pequenas, documentação e responsabilidades separadas | ✅ **ATENDIDO** | `backend/app/main.py`, `regras.py`, `repositorio.py`, `schemas.py`: separação entre API, regras, persistência e modelos; docstrings nas funções | A divisão em camadas e os nomes em português são claros. Recomenda-se complementar com lint/formatador no CI. |
| 7. Refatoração | Demonstrar evolução/refatoração da solução | ⚠️ **PARCIAL** | `js/banco.js`: chamadas `fetch` para a API; `js/config.js`: `API_URL`; `backend/app/`: nova camada FastAPI; `estrutura.txt`: arquitetura atual | A arquitetura atual evidencia a separação frontend → API → banco. A versão anterior e um diff/histórico formal da refatoração não estão na entrega local. |
| 8. Testes unitários/TDD | Testar regras e usar dublês/mocks sem depender da rede | ✅ **ATENDIDO** | `backend/tests/test_regras.py`: validações, tempo e agregações; `backend/tests/test_api.py`: `RepoFalso`; execução local registrada: **28 passed** | Há testes unitários das regras e testes da API com repositório falso, sem rede. |
| 9. CI/CD | Configurar mecanismo de CI/CD | ⏳ **PENDENTE DE UPLOAD** | `.github/workflows/ci.yml`: workflow para Python 3.12 e `pytest -v` em push/PR | O arquivo está configurado localmente. Execução na nuvem e status do workflow dependem do upload para GitHub e não foram comprovados. |
| 10. Tratamento de erros | Usar try/except, códigos HTTP e mensagens amigáveis | ⚠️ **PARCIAL** | `backend/app/main.py`: `HTTPException` 401, 404, 422 e 503; `js/banco.js`: mensagens como “API indisponível” e “Falha ao registrar” | O tratamento está implementado. Porém, o endpoint `/relatorio/resumo` não envolve a consulta em `try/except`, e a proteção de autenticação não é uniforme em todas as operações de escrita/limpeza. |
| 11. Aplicação roda/funciona | Instruções completas e evidências de execução | ⚠️ **PARCIAL** | `README.md`, seção **Como executar**: venv, `.env`, pytest, Uvicorn e Live Server; execução local: `28 passed` | O backend e os testes foram validados localmente. Falta anexar evidência formal do fluxo completo da interface e do banco durante a apresentação. |
| 12. Integração com banco | Usar Supabase/PostgreSQL, tabela e trigger | ⚠️ **PARCIAL** | `backend/app/repositorio.py`: operações na tabela `movimentacoes`; `main.py`/`regras.py`: referência a `tempo_minutos` e à trigger `trg_calcular_tempo`; `backend/.env.example`: conexão Supabase | A integração com Supabase está implementada. O SQL de criação da tabela e da trigger não está entre os arquivos da entrega local, portanto a trigger não pode ser auditada diretamente. |
| 13. Integração com serviço externo/API | Integrar API e/ou serviço externo | ✅ **ATENDIDO** | `backend/app/main.py`: endpoints REST FastAPI; `js/banco.js`: `fetch` para `/auth/login`, `/movimentacoes` e `/movimentacoes/saida` | Há API REST própria e consumo efetivo pelo frontend. O Supabase é acessado pelo backend. |
| 14. Entregáveis acadêmicos | Word, código versionado, PowerPoint, relatório final e vídeo pitch | ⏳ **PENDENTE DE UPLOAD** | `README.md` documenta o projeto; o PDF exige Word, código, PowerPoint, relatório final e vídeo pitch | Não foram identificados, dentro da entrega local auditada, o documento Word, o relatório final e o link do vídeo pitch. A apresentação também precisa ser anexada/publicada junto ao código para comprovação da entrega. |

---

## 3. Pontos fortes

- Arquitetura clara em três camadas: frontend JavaScript, API FastAPI e Supabase/PostgreSQL.
- Regras de negócio isoladas em `backend/app/regras.py`, facilitando testes e manutenção.
- Testes sem dependência de rede em `backend/tests/test_api.py`, com o dublê `RepoFalso`.
- Suíte local executada com resultado comprovado de **28 testes aprovados**.
- Validações explícitas de placa, cor e vaga, além de cálculo de permanência e agregações.
- Tratamento de erros com códigos HTTP distintos e mensagens de retorno para o frontend.
- Documentação local com equipe, arquitetura, execução, versionamento e relação com a ODS 11.
- Workflow de CI preparado para instalar dependências e executar `pytest` em Python 3.12.

---

## 4. Riscos e recomendações

### Riscos técnicos

1. **Chave secreta fora do controle do repositório:** conferir se `backend/.env` está ignorado e nunca publicar a `service_role`/secret key. Como uma chave secreta foi compartilhada durante a configuração, recomenda-se revogá-la e gerar outra antes da entrega.
2. **Trigger sem fonte SQL na entrega:** adicionar um arquivo de migração ou documentação SQL contendo a tabela `movimentacoes` e a trigger `trg_calcular_tempo`.
3. **Tratamento desigual entre endpoints:** envolver o acesso do endpoint `/relatorio/resumo` em tratamento de erro e avaliar autenticação também nas rotas de criação, saída e limpeza.
4. **Ausência de lint no CI:** adicionar uma etapa de verificação de estilo, por exemplo Ruff ou Flake8, se permitido pela equipe e pelo professor.
5. **Mensagens genéricas de login:** o backend converte qualquer exceção do Supabase em 401 “Email ou senha inválidos”, o que dificulta distinguir credencial inválida de indisponibilidade do serviço.

### Riscos de entrega

1. Publicar o repositório no GitHub e comprovar branches, commits, PRs e execução do workflow.
2. Anexar o Word, o PowerPoint, o relatório final e o link do vídeo pitch de cinco minutos.
3. Preparar uma demonstração com API, Live Server, Supabase e usuário administrador funcionando simultaneamente.
4. Registrar no relatório a saída dos testes e, se possível, uma captura do workflow CI aprovado.

---

## 5. Checklist pendente de GitHub

Estes itens foram deliberadamente excluídos da validação local, conforme a regra desta auditoria.

### Branches GitFlow: mínimo de três

1. Criar ou confirmar a branch `main`.
2. Criar ou confirmar a branch `develop`.
3. Criar uma branch de trabalho, por exemplo `feature/backend-fastapi`.
4. Publicar todas as branches:

```bash
git push -u origin main
git push -u origin develop
git push -u origin feature/backend-fastapi
```

### Commits semânticos

Usar mensagens como:

```text
feat: adiciona API FastAPI do ParkSim
test: cobre regras de validação de vagas
test: adiciona testes de integração com repositório falso
ci: configura workflow de testes Python
docs: atualiza documentação da arquitetura
fix: trata falha de conexão com o Supabase
```

### Pull Requests

1. Abrir PR de `feature/backend-fastapi` para `develop`.
2. Solicitar a revisão de pelo menos um integrante.
3. Aguardar o CI passar.
4. Fazer merge em `develop`.
5. Abrir PR de `develop` para `main` antes da entrega final.

### CI na nuvem

1. Publicar `.github/workflows/ci.yml` no repositório.
2. Fazer push para `develop` ou abrir um PR.
3. Conferir a aba **Actions**.
4. Confirmar o job `testes` como concluído com sucesso.
5. Anexar ao relatório o link do workflow ou uma captura do resultado aprovado.

---

## 6. Conclusão da auditoria

O ParkSim está **APTO COM RESSALVAS PARA A APRESENTAÇÃO**.

A solução atende aos fundamentos técnicos do trabalho: usa Python/FastAPI, possui separação de responsabilidades, regras testadas, integração com banco, consumo de API, tratamento de erros e documentação básica de execução. A suíte local de 28 testes aprovados reforça a estabilidade da camada testada.

A aprovação definitiva da entrega depende de quatro ações: publicar o código no GitHub, comprovar o CI e o fluxo GitFlow, anexar os entregáveis acadêmicos exigidos e incluir a definição SQL da tabela/trigger do Supabase. Sem essas evidências, a parte técnica está funcional, mas a documentação de qualidade e a comprovação formal do processo permanecem incompletas.

---

## 7. Fontes consultadas

- `01.avaliacao_a3.pdf` — documento oficial da avaliação A3.
- `README.md` — documentação local do projeto.
- `backend/app/main.py`, `regras.py`, `repositorio.py`, `schemas.py` e `config.py`.
- `backend/tests/test_regras.py` e `backend/tests/test_api.py`.
- `js/banco.js` e `js/config.js`.
- `.github/workflows/ci.yml`.
- `estrutura.txt`.
