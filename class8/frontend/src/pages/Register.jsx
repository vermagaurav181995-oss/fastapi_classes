import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthShell from "../components/AuthShell";
import PasswordInput from "../components/PasswordInput";
import { Alert, Button, Field, Input } from "../components/ui";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { cx, firstName } from "../lib/utils";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function strength(password) {
  let score = 0;
  if (password.length >= 8) score += 1;
  if (password.length >= 12) score += 1;
  if (/[A-Z]/.test(password) && /[a-z]/.test(password)) score += 1;
  if (/\d/.test(password) && /[^A-Za-z0-9]/.test(password)) score += 1;
  return score;
}

const STRENGTH = [
  { label: "Too short", color: "bg-rose-500" },
  { label: "Weak", color: "bg-rose-500" },
  { label: "Fair", color: "bg-amber-500" },
  { label: "Good", color: "bg-emerald-500" },
  { label: "Strong", color: "bg-emerald-600" },
];

function validate(form) {
  const errors = {};
  if (!form.full_name.trim()) errors.full_name = "Tell us your name";
  if (!EMAIL_RE.test(form.email.trim())) errors.email = "Enter a valid email address";
  if (form.password.length < 8) errors.password = "Use at least 8 characters";
  if (form.confirm !== form.password) errors.confirm = "Passwords do not match";
  return errors;
}

export default function Register() {
  const { register } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();
  const [form, setForm] = useState({ full_name: "", email: "", password: "", confirm: "" });
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState("");
  const [loading, setLoading] = useState(false);

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));
  const score = strength(form.password);

  const submit = async (e) => {
    e.preventDefault();
    const found = validate(form);
    setErrors(found);
    setServerError("");
    if (Object.keys(found).length) return;

    setLoading(true);
    try {
      const me = await register({ full_name: form.full_name.trim(), email: form.email.trim(), password: form.password });
      toast.success(`Account created. Welcome, ${firstName(me.full_name)}!`);
      navigate("/", { replace: true });
    } catch (err) {
      setErrors(err.fieldErrors());
      setServerError(err.message);
      setLoading(false);
    }
  };

  return (
    <AuthShell
      title="Create your account"
      subtitle="It takes less than a minute. No credit card needed."
      footer={
        <>
          Already have an account?{" "}
          <Link to="/login" className="font-semibold text-indigo-600 hover:text-indigo-500">
            Sign in
          </Link>
        </>
      }
    >
      <form onSubmit={submit} className="space-y-5" noValidate>
        {serverError && <Alert>{serverError}</Alert>}
        <Field label="Full name" error={errors.full_name}>
          {({ id, invalid }) => <Input id={id} invalid={invalid} autoComplete="name" value={form.full_name} onChange={set("full_name")} placeholder="Jane Doe" />}
        </Field>
        <Field label="Email" error={errors.email}>
          {({ id, invalid }) => (
            <Input id={id} invalid={invalid} type="email" autoComplete="email" value={form.email} onChange={set("email")} placeholder="you@example.com" />
          )}
        </Field>
        <Field label="Password" error={errors.password}>
          {({ id, invalid }) => (
            <>
              <PasswordInput id={id} invalid={invalid} autoComplete="new-password" value={form.password} onChange={set("password")} />
              {form.password && (
                <div className="mt-2 flex items-center gap-3">
                  <div className="flex flex-1 gap-1">
                    {[1, 2, 3, 4].map((n) => (
                      <span key={n} className={cx("h-1.5 flex-1 rounded-full", n <= score ? STRENGTH[score].color : "bg-slate-200")} />
                    ))}
                  </div>
                  <span className="w-16 text-right text-xs text-slate-500">{STRENGTH[score].label}</span>
                </div>
              )}
            </>
          )}
        </Field>
        <Field label="Confirm password" error={errors.confirm}>
          {({ id, invalid }) => <PasswordInput id={id} invalid={invalid} autoComplete="new-password" value={form.confirm} onChange={set("confirm")} />}
        </Field>
        <Button type="submit" size="lg" className="w-full" loading={loading}>
          Create account
        </Button>
      </form>
    </AuthShell>
  );
}
