import { Link } from "react-router-dom";
import { Logo } from "../components/Layout";

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-50 px-4 text-center">
      <Logo />
      <p className="mt-12 font-display text-7xl font-semibold text-indigo-600">404</p>
      <h1 className="mt-4 text-2xl font-semibold text-slate-900">This page is not on our shelves</h1>
      <p className="mt-2 text-slate-500">The page you are looking for does not exist or was moved.</p>
      <Link to="/" className="mt-8 rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-indigo-500">
        Back to dashboard
      </Link>
    </div>
  );
}
