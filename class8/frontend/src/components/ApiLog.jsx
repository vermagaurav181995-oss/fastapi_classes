import { Activity, RotateCcw, Trash2, X } from "lucide-react";
import { useEffect, useState } from "react";
import { API_URL, USE_MOCK, onApiCall, tokenStore } from "../api/http";
import { resetDb } from "../api/mock/db";
import { cx } from "../lib/utils";

const METHOD_COLORS = {
  GET: "text-sky-400",
  POST: "text-emerald-400",
  PATCH: "text-amber-400",
  PUT: "text-amber-400",
  DELETE: "text-rose-400",
};

function statusColor(status) {
  if (status === 0 || status >= 500) return "bg-rose-500/20 text-rose-300";
  if (status >= 400) return "bg-amber-500/20 text-amber-300";
  return "bg-emerald-500/20 text-emerald-300";
}

export default function ApiLog() {
  const [open, setOpen] = useState(false);
  const [calls, setCalls] = useState([]);

  useEffect(() => onApiCall((call) => setCalls((all) => [call, ...all].slice(0, 50))), []);

  const resetMockData = () => {
    if (!window.confirm("Reset all mock data (books, users, orders, reviews) and sign out?")) return;
    resetDb();
    tokenStore.clear();
    try {
      localStorage.removeItem("booknest-cart");
    } catch {
      window.location.assign("/login");
      return;
    }
    window.location.assign("/login");
  };

  const errors = calls.filter((c) => c.status === 0 || c.status >= 400).length;

  return (
    <div className="fixed bottom-4 right-4 z-[60] flex flex-col items-end gap-3">
      {open && (
        <div className="flex max-h-[65vh] w-[28rem] max-w-[calc(100vw-2rem)] flex-col overflow-hidden rounded-2xl bg-slate-900 text-slate-100 shadow-2xl ring-1 ring-white/10">
          <div className="flex items-center gap-2 border-b border-white/10 px-4 py-3">
            <Activity className="size-4 text-indigo-400" />
            <p className="text-sm font-semibold">API calls</p>
            <span
              className={cx(
                "rounded px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wider",
                USE_MOCK ? "bg-indigo-500/20 text-indigo-300" : "bg-emerald-500/20 text-emerald-300",
              )}
            >
              {USE_MOCK ? "mock" : "live"}
            </span>
            <div className="ml-auto flex items-center gap-1">
              {USE_MOCK && (
                <button onClick={resetMockData} className="rounded p-1.5 text-slate-400 hover:bg-white/10 hover:text-white" title="Reset mock data">
                  <RotateCcw className="size-4" />
                </button>
              )}
              <button onClick={() => setCalls([])} className="rounded p-1.5 text-slate-400 hover:bg-white/10 hover:text-white" title="Clear log">
                <Trash2 className="size-4" />
              </button>
              <button onClick={() => setOpen(false)} className="rounded p-1.5 text-slate-400 hover:bg-white/10 hover:text-white" title="Close">
                <X className="size-4" />
              </button>
            </div>
          </div>
          <p className="border-b border-white/10 px-4 py-2 text-xs text-slate-400">
            {USE_MOCK ? "Requests are answered by src/api/mock/server.js inside the browser." : `Requests go to ${API_URL}`}
          </p>
          <ul className="flex-1 divide-y divide-white/5 overflow-y-auto font-mono text-xs">
            {calls.length === 0 && <li className="px-4 py-8 text-center text-slate-500">Click around the app to see requests here.</li>}
            {calls.map((c) => (
              <li key={c.id} className="flex items-center gap-3 px-4 py-2">
                <span className={cx("w-12 shrink-0 font-bold", METHOD_COLORS[c.method])}>{c.method}</span>
                <span className="min-w-0 flex-1 truncate text-slate-200" title={c.path}>
                  {c.path}
                </span>
                <span className={cx("shrink-0 rounded px-1.5 py-0.5 font-semibold", statusColor(c.status))}>{c.status || "ERR"}</span>
                <span className="w-12 shrink-0 text-right text-slate-500">{c.ms}ms</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex items-center gap-2 rounded-full bg-slate-900 px-4 py-2.5 text-sm font-medium text-white shadow-lg ring-1 ring-white/10 transition hover:bg-slate-800"
      >
        <Activity className="size-4 text-indigo-400" />
        API
        <span className="rounded-full bg-white/10 px-2 text-xs">{calls.length}</span>
        {errors > 0 && <span className="size-2 rounded-full bg-rose-500" />}
      </button>
    </div>
  );
}
