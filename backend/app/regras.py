"""Regras de negócio puras do ParkSim (alvo dos testes TDD)."""
import re
from datetime import datetime

PLACA_MERCOSUL = re.compile(r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$")
CORES_PERMITIDAS = {"azul", "vermelho", "preto", "branco", "prata", "verde"}
TOTAL_VAGAS = 8


def validar_placa(placa: str) -> bool:
    """Retorna True se a placa segue o padrão Mercosul (LLLNLNN)."""
    return bool(PLACA_MERCOSUL.match(placa or ""))


def validar_cor(cor: str) -> bool:
    """Retorna True se a cor está na paleta configurada."""
    return cor in CORES_PERMITIDAS


def validar_vaga(vaga: int) -> bool:
    """Retorna True se a vaga está no intervalo 1..8."""
    return isinstance(vaga, int) and 1 <= vaga <= TOTAL_VAGAS


def calcular_tempo_minutos(entrada: datetime, saida: datetime) -> int:
    """Espelha a trigger trg_calcular_tempo: permanência mínima de 1 minuto."""
    if saida < entrada:
        raise ValueError("hora_saida não pode ser anterior à hora_entrada")
    segundos = (saida - entrada).total_seconds()
    return max(1, round(segundos / 60))


def calcular_media_minutos(tempos: list) -> int:
    """Média aritmética dos tempos de permanência (0 se vazio)."""
    if not tempos:
        return 0
    return round(sum(tempos) / len(tempos))


def calcular_frequencia(registros: list, chave: str) -> str:
    """Agregação estilo GROUP BY: valor mais frequente e contagem."""
    if not registros:
        return "—"
    contagem = {}
    for registro in registros:
        contagem[registro[chave]] = contagem.get(registro[chave], 0) + 1
    melhor = max(contagem, key=contagem.get)
    return f"{melhor} ({contagem[melhor]}x)"