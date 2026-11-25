import { CalendarDays, KeyRound, Mail, UserRound } from "lucide-react";
import { useState } from "react";
import { usersApi } from "../api/endpoints";
import PasswordInput from "../components/PasswordInput";
import { Alert, Badge, Button, Card, Field, Input, PageHeader } from "../components/ui";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { formatDate, initials } from "../lib/utils";

function DetailsForm() {
  const { user, setUser } = useAuth();
  const toast = useToast();
  const [fullName, setFullName] = useState(user.full_name);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    if (!fullName.trim()) {
      setError("Name cannot be empty");
      return;
    }
    setError("");
    setSaving(true);
    try {
      setUser(await usersApi.updateMe({ full_name: fullName.trim() }));
      toast.success("Profile updated");
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <Card>
      <form onSubmit={submit} noValidate>
        <div className="border-b border-slate-100 px-6 py-4">
          <h2 className="flex items-center gap-2 font-semibold text-slate-900">
            <UserRound className="size-4 text-indigo-600" />
            Personal details
          </h2>
        </div>
        <div className="grid gap-5 p-6 sm:grid-cols-2">
          <Field label="Full name" error={error}>
            {({ id, invalid }) => <Input id={id} invalid={invalid} value={fullName} onChange={(e) => setFullName(e.target.value)} />}
          </Field>
          <Field label="Email" hint="Email changes are not supported yet.">
            {({ id }) => <Input id={id} value={user.email} disabled />}
          </Field>
        </div>
        <div className="flex justify-end border-t border-slate-100 bg-slate-50/60 px-6 py-3 rounded-b-2xl">
          <Button type="submit" loading={saving} disabled={fullName.trim() === user.full_name}>
            Save changes
          </Button>
        </div>
      </form>
    </Card>
  );
}

function PasswordForm() {
  const toast = useToast();
  const empty = { current: "", next: "", confirm: "" };
  const [form, setForm] = useState(empty);
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState("");
  const [saving, setSaving] = useState(false);

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const submit = async (e) => {
    e.preventDefault();
    const found = {};
    if (!form.current) found.current = "Enter your current password";
    if (form.next.length < 8) found.next = "Use at least 8 characters";
    if (form.next && form.next === form.current) found.next = "New password must be different";
    if (form.confirm !== form.next) found.confirm = "Passwords do not match";
    setErrors(found);
    setServerError("");
    if (Object.keys(found).length) return;

    setSaving(true);
    try {
      await usersApi.changePassword(form.current, form.next);
      setForm(empty);
      toast.success("Password changed");
    } catch (err) {
      setServerError(err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <Card>
      <form onSubmit={submit} noValidate>
        <div className="border-b border-slate-100 px-6 py-4">
          <h2 className="flex items-center gap-2 font-semibold text-slate-900">
            <KeyRound className="size-4 text-indigo-600" />
            Change password
          </h2>
        </div>
        <div className="space-y-5 p-6">
          {serverError && <Alert>{serverError}</Alert>}
          <Field label="Current password" error={errors.current}>
            {({ id, invalid }) => <PasswordInput id={id} invalid={invalid} autoComplete="current-password" value={form.current} onChange={set("current")} />}
          </Field>
          <div className="grid gap-5 sm:grid-cols-2">
            <Field label="New password" error={errors.next}>
              {({ id, invalid }) => <PasswordInput id={id} invalid={invalid} autoComplete="new-password" value={form.next} onChange={set("next")} />}
            </Field>
            <Field label="Confirm new password" error={errors.confirm}>
              {({ id, invalid }) => <PasswordInput id={id} invalid={invalid} autoComplete="new-password" value={form.confirm} onChange={set("confirm")} />}
            </Field>
          </div>
        </div>
        <div className="flex justify-end border-t border-slate-100 bg-slate-50/60 px-6 py-3 rounded-b-2xl">
          <Button type="submit" loading={saving}>
            Update password
          </Button>
        </div>
      </form>
    </Card>
  );
}

export default function Profile() {
  const { user, isAdmin } = useAuth();

  return (
    <>
      <PageHeader title="Profile" subtitle="Manage your account details and password." />
      <div className="grid gap-6 lg:grid-cols-[300px_1fr]">
        <Card className="h-fit overflow-hidden">
          <div className="h-24 bg-gradient-to-br from-indigo-500 to-violet-600" />
          <div className="-mt-10 px-6 pb-6">
            <span className="grid size-20 place-items-center rounded-2xl bg-white text-2xl font-semibold text-indigo-600 shadow-md ring-4 ring-white">
              {initials(user.full_name)}
            </span>
            <p className="mt-4 text-lg font-semibold text-slate-900">{user.full_name}</p>
            <Badge tone={isAdmin ? "violet" : "indigo"} className="mt-1 capitalize">
              {user.role}
            </Badge>
            <dl className="mt-6 space-y-3 text-sm">
              <div className="flex items-center gap-2 text-slate-600">
                <Mail className="size-4 text-slate-400" />
                <span className="truncate">{user.email}</span>
              </div>
              <div className="flex items-center gap-2 text-slate-600">
                <CalendarDays className="size-4 text-slate-400" />
                Member since {formatDate(user.created_at)}
              </div>
            </dl>
          </div>
        </Card>
        <div className="space-y-6">
          <DetailsForm />
          <PasswordForm />
        </div>
      </div>
    </>
  );
}
