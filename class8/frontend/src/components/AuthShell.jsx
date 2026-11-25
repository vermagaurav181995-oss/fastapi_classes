import { BookMarked, ShieldCheck, Sparkles, Truck } from "lucide-react";
import { Logo } from "./Layout";

const FEATURES = [
  { icon: BookMarked, title: "Curated catalog", text: "Hand-picked books across sci-fi, classics, tech and more." },
  { icon: Truck, title: "Track every order", text: "From pending to delivered, see exactly where your books are." },
  { icon: ShieldCheck, title: "Secure accounts", text: "Token-based sign in with user and admin roles." },
];

export default function AuthShell({ title, subtitle, children, footer }) {
  return (
    <div className="grid min-h-screen bg-white lg:grid-cols-[1.05fr_1fr]">
      <section className="relative hidden overflow-hidden bg-slate-950 p-12 text-white lg:flex lg:flex-col">
        <div className="absolute -left-24 -top-24 size-96 rounded-full bg-indigo-600/40 blur-3xl" />
        <div className="absolute -bottom-32 right-0 size-[28rem] rounded-full bg-violet-600/30 blur-3xl" />
        <div className="relative">
          <Logo light />
        </div>
        <div className="relative my-auto max-w-md">
          <span className="inline-flex items-center gap-1.5 rounded-full bg-white/10 px-3 py-1 text-xs font-medium text-indigo-200 ring-1 ring-white/15">
            <Sparkles className="size-3.5" />
            Your next favourite book is waiting
          </span>
          <h2 className="mt-6 font-display text-4xl font-semibold leading-tight">
            A cosy corner of the internet for people who love books.
          </h2>
          <ul className="mt-10 space-y-6">
            {FEATURES.map(({ icon: Icon, title: t, text }) => (
              <li key={t} className="flex gap-4">
                <span className="grid size-10 shrink-0 place-items-center rounded-xl bg-white/10 ring-1 ring-white/15">
                  <Icon className="size-5 text-indigo-300" />
                </span>
                <div>
                  <p className="font-medium">{t}</p>
                  <p className="text-sm text-slate-400">{text}</p>
                </div>
              </li>
            ))}
          </ul>
        </div>
        <p className="relative text-xs text-slate-500">All data is mocked in the browser. No real accounts or payments.</p>
      </section>

      <section className="flex items-center justify-center px-4 py-12 sm:px-8">
        <div className="w-full max-w-sm">
          <div className="mb-10 lg:hidden">
            <Logo />
          </div>
          <h1 className="font-display text-3xl font-semibold tracking-tight text-slate-900">{title}</h1>
          <p className="mt-2 text-sm text-slate-500">{subtitle}</p>
          <div className="mt-8">{children}</div>
          {footer && <div className="mt-8 text-center text-sm text-slate-500">{footer}</div>}
        </div>
      </section>
    </div>
  );
}
