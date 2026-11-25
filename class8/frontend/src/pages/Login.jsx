import { ShieldCheck, UserRound } from "lucide-react";
import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import AuthShell from "../components/AuthShell";
import PasswordInput from "../components/PasswordInput";
import { Alert, Button, Field, Input } from "../components/ui";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { firstName } from "../lib/utils";

const DEMO_ACCOUNTS = [
  { label: "Reader", email: "reader@booknest.dev", password: "reader123", icon: UserRound },
  { label: "Admin", email: "admin@booknest.dev", password: "admin123", icon: ShieldCheck },
];

export default function Login() {
  const { login } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    if (!form.email.trim() || !form.password) {
      setError("Enter your email and password.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const me = await login(form.email.trim(), form.password);
      toast.success(`Welcome back, ${firstName(me.full_name)}!`);
      navigate(location.state?.from?.pathname ?? "/", { replace: true });
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <AuthShell
      title="Welcome back"
      subtitle="Sign in to browse the catalog, manage your cart and track orders."
      footer={
        <>
          New to BookNest?{" "}
          <Link to="/register" className="font-semibold text-indigo-600 hover:text-indigo-500">
            Create an account
          </Link>
        </>
      }
    >
      <form onSubmit={submit} className="space-y-5" noValidate>
        {error && <Alert>{error}</Alert>}
        <Field label="Email">
          {({ id }) => (
            <Input
              id={id}
              type="email"
              autoComplete="email"
              placeholder="you@example.com"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          )}
        </Field>
        <Field label="Password">
          {({ id }) => (
            <PasswordInput
              id={id}
              autoComplete="current-password"
              placeholder="••••••••"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
          )}
        </Field>
        <Button type="submit" size="lg" className="w-full" loading={loading}>
          Sign in
        </Button>
      </form>

      <div className="mt-8">
        <div className="relative text-center">
          <div className="absolute inset-x-0 top-1/2 border-t border-slate-200" />
          <span className="relative bg-white px-3 text-xs font-medium uppercase tracking-wider text-slate-400">Demo accounts</span>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-3">
          {DEMO_ACCOUNTS.map(({ label, email, password, icon: Icon }) => (
            <button
              key={label}
              type="button"
              onClick={() => {
                setForm({ email, password });
                setError("");
              }}
              className="flex items-center gap-3 rounded-xl p-3 text-left ring-1 ring-slate-200 transition hover:bg-slate-50 hover:ring-indigo-300"
            >
              <span className="grid size-9 place-items-center rounded-lg bg-indigo-50 text-indigo-600">
                <Icon className="size-4" />
              </span>
              <span className="min-w-0">
                <span className="block text-sm font-semibold text-slate-900">{label}</span>
                <span className="block truncate text-xs text-slate-500">{password}</span>
              </span>
            </button>
          ))}
        </div>
      </div>
    </AuthShell>
  );
}
