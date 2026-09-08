"""Camada de acesso a dados (PostgreSQL/Supabase via service role)."""
from supabase import Client, create_client

from .config import SUPABASE_SERVICE_KEY, SUPABASE_URL

_client: Client | None = None


def obter_client() -> Client:
    """Retorna (e cacheia) o cliente Supabase do backend."""
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    return _client


def listar_movimentacoes(sessao: int) -> list:
    """SELECT da sessão, mais recentes primeiro."""
    resposta = (
        obter_client()
        .table("movimentacoes")
        .select("*")
        .eq("sessao", sessao)
        .order("hora_entrada", desc=True)
        .execute()
    )
    return resposta.data


def inserir_movimentacao(dados: dict) -> dict:
    """INSERT de nova movimentação."""
    resposta = obter_client().table("movimentacoes").insert(dados).execute()
    return resposta.data[0]


def registrar_saida(placa: str, sessao: int, hora_saida: str) -> list:
    """UPDATE de saída apenas para veículos ainda estacionados."""
    resposta = (
        obter_client()
        .table("movimentacoes")
        .update({"hora_saida": hora_saida, "status": "SAIU"})
        .eq("placa", placa)
        .eq("sessao", sessao)
        .is_("hora_saida", "null")
        .execute()
    )
    return resposta.data


def limpar_movimentacoes() -> None:
    """DELETE de todos os registros (reinício de teste)."""
    obter_client().table("movimentacoes").delete().not_("id", "is", None).execute()
