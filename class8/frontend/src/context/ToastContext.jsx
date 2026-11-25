import { CheckCircle2, Info, X, XCircle } from "lucide-react";
import { createContext, useCallback, useContext, useMemo, useState } from "react";

const ToastContext = createContext(null);

const STYLES = {
  success: { icon: CheckCircle2, color: "text-emerald-500" },
  error: { icon: XCircle, color: "text-rose-500" },
  info: { icon: Info, color: "text-indigo-500" },
};

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const dismiss = useCallback((id) => setToasts((all) => all.filter((t) => t.id !== id)), []);

  const push = useCallback(
    (type, message) => {
      const id = crypto.randomUUID();
      setToasts((all) => [...all.slice(-3), { id, type, message }]);
      setTimeout(() => dismiss(id), 3800);
    },
    [dismiss],
  );

  const toast = useMemo(
    () => ({
      success: (m) => push("success", m),
      error: (m) => push("error", m),
      info: (m) => push("info", m),
    }),
    [push],
  );

  return (
    <ToastContext.Provider value={toast}>
      {children}
      <div className="pointer-events-none fixed inset-x-4 top-4 z-[70] flex flex-col items-end gap-2 sm:left-auto sm:w-96">
        {toasts.map((t) => {
          const { icon: Icon, color } = STYLES[t.type];
          return (
            <div
              key={t.id}
              role="status"
              className="pointer-events-auto flex w-full items-start gap-3 rounded-xl bg-white p-4 shadow-lg ring-1 ring-slate-200 animate-[toast-in_.2s_ease-out]"
            >
              <Icon className={`mt-0.5 size-5 shrink-0 ${color}`} />
              <p className="flex-1 text-sm text-slate-700">{t.message}</p>
              <button onClick={() => dismiss(t.id)} className="text-slate-400 hover:text-slate-600" aria-label="Dismiss">
                <X className="size-4" />
              </button>
            </div>
          );
        })}
      </div>
    </ToastContext.Provider>
  );
}

export const useToast = () => useContext(ToastContext);
