"""API ParkSim — backend em Python (FastAPI) sobre PostgreSQL/Supabase.

Projeto acadêmico vinculado à ODS 11 (Cidades e Comunidades Sustentáveis).
"""
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from . import repositorio
from .regras import (
    calcular_frequencia,
    calcular_media_minutos,
    validar_cor,
    validar_placa,
    validar_vaga,
)
from .schemas import LoginEntrada, MovimentacaoEntrada, SaidaEntrada

app = FastAPI(
    title="ParkSim API",
    description="Backend em Python do simulador de estacionamento (ODS 11).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

seguranca = HTTPBearer(auto_error=False)


def exigir_admin(
    credenciais: HTTPAuthorizationCredentials | None = Depends(seguranca),
) -> str:
    """Garante que só admin autenticado consulte os dados (equivalente ao RLS)."""
    if credenciais is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token não informado.")
    try:
        usuario = repositorio.obter_client().auth.get_user(credenciais.credentials)
    except Exception as erro:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sessão inválida.") from erro
    return usuario.user.email


@app.get("/health")
def health() -> dict:
    """Endpoint de saúde usado pelo CI/CD e monitoramento."""
    return {"status": "ok"}


@app.post("/auth/login")
def login(dados: LoginEntrada) -> dict:
    """Autentica o admin no Supabase Auth e devolve o token JWT."""
    try:
        resposta = repositorio.obter_client().auth.sign_in_with_password(
            {"email": dados.email, "password": dados.senha}
        )
    except Exception as erro:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Email ou senha inválidos."
        ) from erro
    return {"access_token": resposta.session.access_token, "email": dados.email}


@app.get("/movimentacoes")
def listar(sessao: int, _email: str = Depends(exigir_admin)) -> list:
    """Relatório da sessão (restrito ao admin)."""
    try:
        return repositorio.listar_movimentacoes(sessao)
    except Exception as erro:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, "Falha ao consultar o banco."
        ) from erro


@app.get("/relatorio/resumo")
def resumo(sessao: int, _email: str = Depends(exigir_admin)) -> dict:
    """Agregações (COUNT/AVG/GROUP BY) calculadas em Python."""
    registros = repositorio.listar_movimentacoes(sessao)
    tempos = [r["tempo_minutos"] for r in registros if r.get("tempo_minutos") is not None]
    return {
        "total": len(registros),
        "estacionados": sum(1 for r in registros if r["status"] == "ESTACIONADO"),
        "saidas": sum(1 for r in registros if r["status"] == "SAIU"),
        "tempo_medio_min": calcular_media_minutos(tempos),
        "cor_frequente": calcular_frequencia(registros, "cor"),
        "vaga_frequente": calcular_frequencia(registros, "vaga"),
    }


@app.post("/movimentacoes", status_code=status.HTTP_201_CREATED)
def criar(dados: MovimentacaoEntrada) -> dict:
    """Registra entrada validando placa, cor e vaga (regras em Python)."""
    if not validar_placa(dados.placa):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Placa fora do padrão Mercosul."
        )
    if not validar_cor(dados.cor):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Cor não permitida."
        )
    if not validar_vaga(dados.vaga):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Vaga deve estar entre 1 e 8."
        )
    try:
        return repositorio.inserir_movimentacao(
            {
                "placa": dados.placa,
                "cor": dados.cor,
                "vaga": dados.vaga,
                "sessao": dados.sessao,
                "status": "ESTACIONADO",
            }
        )
    except Exception as erro:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, "Falha ao gravar no banco."
        ) from erro


@app.patch("/movimentacoes/saida")
def sair(dados: SaidaEntrada) -> dict:
    """Registra a saída; a trigger do banco calcula tempo_minutos."""
    hora_saida = datetime.now(timezone.utc).isoformat()
    try:
        alterados = repositorio.registrar_saida(dados.placa, dados.sessao, hora_saida)
    except Exception as erro:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, "Falha ao atualizar o banco."
        ) from erro
    if not alterados:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Veículo estacionado não encontrado."
        )
    return {"atualizados": len(alterados), "hora_saida": hora_saida}


@app.delete("/movimentacoes")
def limpar() -> dict:
    """Limpa a tabela (reiniciar teste / recarregar página)."""
    try:
        repositorio.limpar_movimentacoes()
    except Exception as erro:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, "Falha ao limpar o banco."
        ) from erro
    return {"limpo": True}
