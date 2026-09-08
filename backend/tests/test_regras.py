"""Testes unitários das regras de negócio (TDD)."""
from datetime import datetime, timedelta

import pytest

from app.regras import (
    calcular_frequencia,
    calcular_media_minutos,
    calcular_tempo_minutos,
    validar_cor,
    validar_placa,
    validar_vaga,
)


class TestValidarPlaca:
    def test_placa_mercosul_valida(self):
        assert validar_placa("ABC1D23") is True

    def test_placa_antiga_invalida(self):
        assert validar_placa("ABC1234") is False

    def test_placa_vazia_invalida(self):
        assert validar_placa("") is False

    def test_placa_minuscula_invalida(self):
        assert validar_placa("abc1d23") is False


class TestValidarCorEVaga:
    def test_cor_permitida(self):
        assert validar_cor("azul") is True

    def test_cor_fora_da_paleta(self):
        assert validar_cor("rosa") is False

    @pytest.mark.parametrize("vaga", [1, 4, 8])
    def test_vagas_validas(self, vaga):
        assert validar_vaga(vaga) is True

    @pytest.mark.parametrize("vaga", [0, 9, -3])
    def test_vagas_invalidas(self, vaga):
        assert validar_vaga(vaga) is False


class TestCalcularTempo:
    def test_permanencia_minima_de_um_minuto(self):
        entrada = datetime(2026, 1, 1, 10, 0, 0)
        assert calcular_tempo_minutos(entrada, entrada + timedelta(seconds=20)) == 1

    def test_arredondamento_de_minutos(self):
        entrada = datetime(2026, 1, 1, 10, 0, 0)
        assert calcular_tempo_minutos(entrada, entrada + timedelta(seconds=90)) == 2

    def test_saida_anterior_gera_erro(self):
        entrada = datetime(2026, 1, 1, 10, 0, 0)
        with pytest.raises(ValueError):
            calcular_tempo_minutos(entrada, entrada - timedelta(minutes=5))


class TestAgregacoes:
    def test_media_vazia(self):
        assert calcular_media_minutos([]) == 0

    def test_media_simples(self):
        assert calcular_media_minutos([2, 4, 6]) == 4

    def test_frequencia_vazia(self):
        assert calcular_frequencia([], "cor") == "—"

    def test_frequencia_de_cor(self):
        registros = [{"cor": "azul"}, {"cor": "azul"}, {"cor": "preto"}]
        assert calcular_frequencia(registros, "cor") == "azul (2x)"
