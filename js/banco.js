import { API_URL } from "./config.js";

/* ---------- sessão (localStorage) ---------- */

export function getSessaoAtual() {
    const s = parseInt(localStorage.getItem("parksim_sessao") || "1", 10);
    return Number.isFinite(s) ? s : 1;
}

export function novaSessao() {
    const s = getSessaoAtual() + 1;
    localStorage.setItem("parksim_sessao", String(s));
    return s;
}

export function resetarSessao() {
    localStorage.setItem("parksim_sessao", "1");
    return 1;
}

/* ---------- autenticação (API Python) ---------- */

let authListener = null;

export function aoMudarAuth(cb) {
    authListener = cb;
}

function sessaoAuthSync() {
    const token = localStorage.getItem("parksim_token");
    if (!token) return null;
    return {
        access_token: token,
        user: { email: localStorage.getItem("parksim_email") || "Admin" },
    };
}

export async function sessaoAtiva() {
    return sessaoAuthSync();
}

function emitirAuth() {
    if (authListener) authListener(sessaoAuthSync());
}

export async function login(email, senha) {
    try {
        const r = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, senha }),
        });

        if (!r.ok) {
            const corpo = await r.json().catch(() => ({}));
            return { data: null, error: { message: corpo.detail || "Email ou senha inválidos." } };
        }

        const corpo = await r.json();
        localStorage.setItem("parksim_token", corpo.access_token);
        localStorage.setItem("parksim_email", corpo.email);
        emitirAuth();
        return { data: { session: sessaoAuthSync() }, error: null };
    } catch (erro) {
        return { data: null, error: { message: "Falha de conexão com a API." } };
    }
}

export async function logout() {
    localStorage.removeItem("parksim_token");
    localStorage.removeItem("parksim_email");
    emitirAuth();
    return { error: null };
}

function headersAdmin() {
    const token = localStorage.getItem("parksim_token");
    return token ? { Authorization: `Bearer ${token}` } : {};
}

/* ---------- dados (API Python) ---------- */

export async function limparMovimentacoes() {
    try {
        const r = await fetch(`${API_URL}/movimentacoes`, { method: "DELETE" });
        return { data: null, error: r.ok ? null : { message: "Falha ao limpar." } };
    } catch (erro) {
        return { data: null, error: { message: "API indisponível." } };
    }
}

export async function registrarEntrada({ placa, cor, vaga, sessao }) {
    try {
        const r = await fetch(`${API_URL}/movimentacoes`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ placa, cor, vaga, sessao }),
        });
        const data = await r.json().catch(() => null);
        return { data, error: r.ok ? null : { message: "Falha ao registrar entrada." } };
    } catch (erro) {
        return { data: null, error: { message: "API indisponível." } };
    }
}

export async function registrarSaida(placa, sessao) {
    try {
        const r = await fetch(`${API_URL}/movimentacoes/saida`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ placa, sessao }),
        });
        const data = await r.json().catch(() => null);
        return { data, error: r.ok ? null : { message: "Falha ao registrar saída." } };
    } catch (erro) {
        return { data: null, error: { message: "API indisponível." } };
    }
}

export async function buscarMovimentacoes(sessao) {
    try {
        const r = await fetch(`${API_URL}/movimentacoes?sessao=${sessao}`, {
            headers: headersAdmin(),
        });

        if (!r.ok) return { data: [], error: { message: "Sem permissão de leitura." } };

        const data = await r.json();
        return { data, error: null };
    } catch (erro) {
        return { data: [], error: { message: "API indisponível." } };
    }
}