"""Testes de integração da API com repositório falso (sem rede)."""
from fastapi.testclient import TestClient

from app import main


class RepoFalso:
    """Dublê de teste do repositório (injeção de dependência)."""

    def __init__(self):
        self.registros = []

    def listar_movimentacoes(self, sessao):
        return [r for r in self.registros if r["sessao"] == sessao]

    def inserir_movimentacao(self, dados):
        self.registros.append({**dados, "id": len(self.registros) + 1})
        return self.registros[-1]

    def registrar_saida(self, placa, sessao, hora_saida):
        achados = [
            r for r in self.registros
            if r["placa"] == placa and r["sessao"] == sessao and r["status"] == "ESTACIONADO"
        ]
        for registro in achados:
            registro.update({"status": "SAIU", "hora_saida": hora_saida})
        return achados

    def limpar_movimentacoes(self):
        self.registros.clear()


main.repositorio = RepoFalso()

client = TestClient(main.app)
client.app.dependency_overrides[main.exigir_admin] = lambda: "admin@parksim.com"


def test_health_disponivel():
    assert client.get("/health").status_code == 200


def test_cria_movimentacao_valida():
    resposta = client.post(
        "/movimentacoes",
        json={"placa": "ABC1D23", "cor": "azul", "vaga": 1, "sessao": 1},
    )
    assert resposta.status_code == 201
    assert resposta.json()["status"] == "ESTACIONADO"


def test_rejeita_placa_invalida():
    resposta = client.post(
        "/movimentacoes", json={"placa": "XXX", "cor": "azul", "vaga": 1}
    )
    assert resposta.status_code == 422


def test_rejeita_vaga_fora_do_limite():
    resposta = client.post(
        "/movimentacoes", json={"placa": "ABC1D23", "cor": "azul", "vaga": 9}
    )
    assert resposta.status_code == 422


def test_saida_atualiza_status():
    client.post(
        "/movimentacoes",
        json={"placa": "ZZZ9W88", "cor": "preto", "vaga": 2, "sessao": 1},
    )
    resposta = client.patch(
        "/movimentacoes/saida", json={"placa": "ZZZ9W88", "sessao": 1}
    )
    assert resposta.status_code == 200


def test_saida_inexistente_retorna_404():
    resposta = client.patch(
        "/movimentacoes/saida", json={"placa": "NAO1E23", "sessao": 1}
    )
    assert resposta.status_code == 404


def test_listar_sem_token_retorna_401():
    client.app.dependency_overrides.clear()
    resposta = client.get("/movimentacoes", params={"sessao": 1})
    client.app.dependency_overrides[main.exigir_admin] = lambda: "admin@parksim.com"
    assert resposta.status_code == 401


def test_listar_retorna_registros():
    resposta = client.get("/movimentacoes", params={"sessao": 1})
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)


def test_limpar_apaga_todos_os_registros():
    client.delete("/movimentacoes")
    resposta = client.get("/movimentacoes", params={"sessao": 1})
    assert resposta.json() == []
