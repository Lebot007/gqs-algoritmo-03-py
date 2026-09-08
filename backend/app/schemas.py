"""Modelos de entrada/saída da API (Pydantic)."""
from pydantic import BaseModel, Field


class LoginEntrada(BaseModel):
    """Credenciais do administrador."""
    email: str = Field(min_length=5)
    senha: str = Field(min_length=6)


class MovimentacaoEntrada(BaseModel):
    """Registro de entrada de veículo."""
    placa: str
    cor: str
    vaga: int
    sessao: int = 1


class SaidaEntrada(BaseModel):
    """Registro de saída de veículo."""
    placa: str
    sessao: int = 1