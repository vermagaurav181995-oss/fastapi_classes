import { AlertTriangle, ArrowRight, BookCopy, Clock, DollarSign, MessageSquareText, Package, Users, Wallet } from "lucide-react";
import { Link } from "react-router-dom";
import { booksApi, dashboardApi, ordersApi } from "../api/endpoints";
import BookCover from "../components/BookCover";
import { Alert, Badge, Card, EmptyState, PageHeader, Skeleton, Stars, StatusBadge } from "../components/ui";
import { useAuth } from "../context/AuthContext";
import { firstName, formatDate, formatMoney, greeting, useApi } from "../lib/utils";

function StatCard({ icon: Icon, label, value, tone }) {
  return (
    <Card className="p-5">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-500">{label}</p>
        <span className={`grid size-9 place-items-center rounded-lg ${tone}`}>
          <Icon className="size-5" />
        </span>
      </div>
      <p className="mt-3 text-3xl font-semibold tracking-tight text-slate-900">{value}</p>
    </Card>
  );
}

function statCards(stats) {
  if (stats.role === "admin") {
    return [
      { icon: DollarSign, label: "Revenue", value: formatMoney(stats.revenue), tone: "bg-emerald-50 text-emerald-600" },
      { icon: Package, label: "Orders", value: stats.orders_count, tone: "bg-indigo-50 text-indigo-600" },
      { icon: BookCopy, label: "Books", value: stats.books_count, tone: "bg-violet-50 text-violet-600" },
      { icon: Users, label: "Customers", value: stats.users_count, tone: "bg-sky-50 text-sky-600" },
    ];
  }
  return [
    { icon: Package, label: "My orders", value: stats.orders_count, tone: "bg-indigo-50 text-indigo-600" },
    { icon: Wallet, label: "Total spent", value: formatMoney(stats.total_spent), tone: "bg-emerald-50 text-emerald-600" },
    { icon: Clock, label: "Pending", value: stats.pending_orders, tone: "bg-amber-50 text-amber-600" },
    { icon: MessageSquareText, label: "Reviews written", value: stats.reviews_count, tone: "bg-violet-50 text-violet-600" },
  ];
}

export default function Dashboard() {
  const { user, isAdmin } = useAuth();
  const stats = useApi(() => dashboardApi.stats(), []);
  const orders = useApi(() => ordersApi.list({ limit: 5 }), []);
  const topBooks = useApi(() => booksApi.list({ sort: "-rating", size: 4 }), []);

  return (
    <>
      <PageHeader
        title={`${greeting()}, ${firstName(user.full_name)}`}
        subtitle={isAdmin ? "Here's how the store is doing today." : "Here's what's happening with your books."}
      />

      {stats.error && <Alert>{stats.error.message}</Alert>}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.data
          ? statCards(stats.data).map((card) => <StatCard key={card.label} {...card} />)
          : [1, 2, 3, 4].map((n) => <Skeleton key={n} className="h-[118px] rounded-2xl" />)}
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <div className="flex items-center justify-between border-b border-slate-100 px-6 py-4">
            <h2 className="font-semibold text-slate-900">{isAdmin ? "Latest orders" : "Recent orders"}</h2>
            <Link to="/orders" className="flex items-center gap-1 text-sm font-medium text-indigo-600 hover:text-indigo-500">
              View all <ArrowRight className="size-4" />
            </Link>
          </div>
          {orders.loading && !orders.data ? (
            <div className="space-y-3 p-6">
              {[1, 2, 3].map((n) => (
                <Skeleton key={n} className="h-10" />
              ))}
            </div>
          ) : orders.data?.length ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-xs uppercase tracking-wider text-slate-500">
                    <th className="px-6 py-3 font-medium">Order</th>
                    {isAdmin && <th className="px-6 py-3 font-medium">Customer</th>}
                    <th className="px-6 py-3 font-medium">Date</th>
                    <th className="px-6 py-3 font-medium">Status</th>
                    <th className="px-6 py-3 text-right font-medium">Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {orders.data.map((o) => (
                    <tr key={o.id} className="hover:bg-slate-50/60">
                      <td className="px-6 py-3.5 font-medium text-slate-900">#{o.id}</td>
                      {isAdmin && <td className="px-6 py-3.5 text-slate-600">{o.user_name}</td>}
                      <td className="whitespace-nowrap px-6 py-3.5 text-slate-500">{formatDate(o.created_at)}</td>
                      <td className="px-6 py-3.5">
                        <StatusBadge status={o.status} />
                      </td>
                      <td className="px-6 py-3.5 text-right font-medium text-slate-900">{formatMoney(o.total)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <EmptyState
              icon={Package}
              title="No orders yet"
              text="When you check out a cart, it will show up here."
              action={
                <Link to="/books" className="text-sm font-semibold text-indigo-600">
                  Browse books →
                </Link>
              }
            />
          )}
        </Card>

        {isAdmin ? (
          <Card>
            <div className="flex items-center gap-2 border-b border-slate-100 px-6 py-4">
              <AlertTriangle className="size-4 text-amber-500" />
              <h2 className="font-semibold text-slate-900">Low stock</h2>
            </div>
            <ul className="divide-y divide-slate-100">
              {stats.data?.low_stock?.length === 0 && <li className="px-6 py-8 text-center text-sm text-slate-500">Everything is well stocked.</li>}
              {stats.data?.low_stock?.map((b) => (
                <li key={b.id}>
                  <Link to={`/books/${b.id}`} className="flex items-center justify-between gap-3 px-6 py-3.5 hover:bg-slate-50/60">
                    <span className="truncate text-sm font-medium text-slate-700">{b.title}</span>
                    <Badge tone={b.stock === 0 ? "rose" : "amber"}>{b.stock === 0 ? "Out of stock" : `${b.stock} left`}</Badge>
                  </Link>
                </li>
              ))}
            </ul>
          </Card>
        ) : (
          <Card className="relative overflow-hidden bg-gradient-to-br from-indigo-600 to-violet-700 p-6 text-white ring-0">
            <div className="absolute -right-10 -top-10 size-40 rounded-full bg-white/10" />
            <p className="text-sm font-medium text-indigo-200">Reading goal</p>
            <p className="mt-2 font-display text-2xl font-semibold">Find your next great read</p>
            <p className="mt-2 text-sm text-indigo-100">Browse {topBooks.data?.total ?? "our"} books across every genre, from timeless classics to modern tech.</p>
            <Link to="/books" className="mt-6 inline-flex items-center gap-2 rounded-lg bg-white px-4 py-2 text-sm font-semibold text-indigo-700 hover:bg-indigo-50">
              Explore catalog <ArrowRight className="size-4" />
            </Link>
          </Card>
        )}
      </div>

      <div className="mt-10">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-900">Top rated</h2>
          <Link to="/books?sort=-rating" className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
            See more
          </Link>
        </div>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          {topBooks.data
            ? topBooks.data.items.map((b) => (
                <Link key={b.id} to={`/books/${b.id}`} className="group">
                  <BookCover book={b} className="aspect-[4/5] transition group-hover:-translate-y-1 group-hover:shadow-lg" />
                  <p className="mt-3 truncate text-sm font-semibold text-slate-900">{b.title}</p>
                  <div className="mt-1 flex items-center gap-2">
                    <Stars value={b.avg_rating} className="size-3.5" />
                    <span className="text-xs text-slate-500">{b.avg_rating || "–"}</span>
                  </div>
                </Link>
              ))
            : [1, 2, 3, 4].map((n) => <Skeleton key={n} className="aspect-[4/5] rounded-xl" />)}
        </div>
      </div>
    </>
  );
}
