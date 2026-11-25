import { handle } from "./mock/server";

export const USE_MOCK = import.meta.env.VITE_USE_MOCK !== "false";
export const API_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, "");

const TOKEN_KEY = "booknest-token";

export const tokenStore = {
  get() {
    try {
      return localStorage.getItem(TOKEN_KEY);
    } catch {
      return null;
    }
  },
  set(token) {
    try {
      localStorage.setItem(TOKEN_KEY, token);
    } catch {
      return;
    }
  },
  clear() {
    try {
      localStorage.removeItem(TOKEN_KEY);
    } catch {
      return;
    }
  },
};

export function formatDetail(detail) {
  if (Array.isArray(detail)) return detail.map((d) => `${d.loc?.at(-1) ?? "field"}: ${d.msg}`).join(" · ");
  if (typeof detail === "string" && detail) return detail;
  return "Something went wrong. Please try again.";
}

export class ApiError extends Error {
  constructor(status, detail) {
    super(formatDetail(detail));
    this.status = status;
    this.detail = detail;
  }

  fieldErrors() {
    if (!Array.isArray(this.detail)) return {};
    return Object.fromEntries(this.detail.map((d) => [d.loc?.at(-1), d.msg]));
  }
}

const listeners = new Set();

export function onApiCall(listener) {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function cleanQuery(query) {
  if (!query) return {};
  return Object.fromEntries(
    Object.entries(query)
      .filter(([, v]) => v !== undefined && v !== null && v !== "")
      .map(([k, v]) => [k, String(v)]),
  );
}

async function sendMock(method, path, { query, body, form, token }) {
  await sleep(200 + Math.random() * 350);
  const payload = form ?? (body === undefined ? undefined : JSON.parse(JSON.stringify(body)));
  return handle(method, path, { query, body: payload, token });
}

async function sendHttp(method, url, { body, form, token }) {
  const headers = { Accept: "application/json" };
  let payload;
  if (token) headers.Authorization = `Bearer ${token}`;
  if (form) {
    payload = new URLSearchParams(form);
  } else if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }
  try {
    const res = await fetch(url, { method, headers, body: payload });
    const data = res.status === 204 ? null : await res.json().catch(() => null);
    return { status: res.status, data };
  } catch {
    return { status: 0, data: { detail: `Cannot reach the API at ${API_URL}. Is the FastAPI server running?` } };
  }
}

export async function request(method, path, { query, body, form } = {}) {
  const params = cleanQuery(query);
  const qs = new URLSearchParams(params).toString();
  const fullPath = qs ? `${path}?${qs}` : path;
  const token = tokenStore.get();
  const started = performance.now();

  const { status, data } = USE_MOCK
    ? await sendMock(method, path, { query: params, body, form, token })
    : await sendHttp(method, `${API_URL}${fullPath}`, { body, form, token });

  for (const listener of listeners) {
    listener({ id: crypto.randomUUID(), method, path: fullPath, status, ms: Math.round(performance.now() - started), at: new Date() });
  }

  if (status === 0 || status >= 400) {
    if (status === 401 && token) window.dispatchEvent(new Event("booknest:unauthorized"));
    throw new ApiError(status, data?.detail);
  }
  return data;
}
