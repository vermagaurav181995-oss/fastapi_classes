import { CalendarDays, Package, UserRound } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
import { ordersApi } from "../api/endpoints";
import ConfirmModal from "../components/ConfirmModal";
import { Alert, Button, Card, EmptyState, PageHeader, Select, Skeleton, StatusBadge } from "../components/ui";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { cx, formatDateTime, formatMoney, useApi } from "../lib/utils";

const STATUSES = ["pending", "paid", "shipped", "delivered", "cancelled"];
const TABS = ["all", ...STATUSES];
const STEPS = ["pending", "paid", "shipped", "delivered"];

function Progress({ status }) {
  if (status === "cancelled") return null;
  const current = STEPS.indexOf(status);
  return (
    <ol className="mt-5 grid grid-cols-4 gap-2">
      {STEPS.map((step, i) => (
        <li key={step}>
          <div className={cx("h-1.5 rounded-full", i <= current ? "bg-indigo-600" : "bg-slate-200")} />
          <p className={cx("mt-1.5 text-xs capitalize", i <= current ? "font-medium text-slate-700" : "text-slate-400")}>{step}</p>
        </li>
      ))}
    </ol>
  );
}

function OrderCard({ order, isAdmin, onCancel, onStatusChange, busy }) {
  return (
    <Card className="overflow-hidden">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 bg-slate-50/60 px-5 py-4">
        <div className="flex flex-wrap items-center gap-x-5 gap-y-1">
          <p className="font-semibold text-slate-900">Order #{order.id}</p>
          <span className="flex items-center gap-1.5 text-sm text-slate-500">
            <CalendarDays className="size-4" />
            {formatDateTime(order.created_at)}
          </span>
          {isAdmin && (
            <span className="flex items-center gap-1.5 text-sm text-slate-500">
              <UserRound className="size-4" />
              {order.user_name}
            </span>
          )}
        </div>
        <StatusBadge status={order.status} />
      </div>

      <div className="px-5 py-4">
        <ul className="space-y-2">
          {order.items.map((item) => (
            <li key={item.book_id} className="flex items-center justify-between gap-4 text-sm">
              <Link to={`/books/${item.book_id}`} className="truncate text-slate-700 hover:text-indigo-600">
                <span className="text-slate-400">{item.quantity} ×</span> {item.title}
              </Link>
              <span className="shrink-0 text-slate-500">{formatMoney(item.price * item.quantity)}</span>
            </li>
          ))}
        </ul>
        <Progress status={order.status} />
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-100 px-5 py-3">
        <p className="text-sm text-slate-500">
          Total <span className="ml-1 text-base font-semibold text-slate-900">{formatMoney(order.total)}</span>
        </p>
        {isAdmin ? (
          <div className="flex items-center gap-2">
            <label htmlFor={`status-${order.id}`} className="text-sm text-slate-500">
              Status
            </label>
            <Select
              id={`status-${order.id}`}
              value={order.status}
              disabled={order.status === "cancelled" || busy}
              onChange={(e) => onStatusChange(order, e.target.value)}
              className="h-9 w-36 capitalize"
            >
              {STATUSES.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </Select>
          </div>
        ) : (
          order.status === "pending" && (
            <Button variant="secondary" size="sm" onClick={() => onCancel(order)} className="text-rose-600">
              Cancel order
            </Button>
          )
        )}
      </div>
    </Card>
  );
}

export default function Orders() {
  const { isAdmin } = useAuth();
  const toast = useToast();
  const [tab, setTab] = useState("all");
  const [cancelling, setCancelling] = useState(null);
  const [cancelLoading, setCancelLoading] = useState(false);
  const [busyId, setBusyId] = useState(null);

  const orders = useApi(() => ordersApi.list({ status: tab === "all" ? undefined : tab }), [tab]);

  const replace = (updated) => {
    orders.setData((list) => {
      const next = list.map((o) => (o.id === updated.id ? updated : o));
      return tab === "all" ? next : next.filter((o) => o.status === tab);
    });
  };

  const confirmCancel = async () => {
    setCancelLoading(true);
    try {
      replace(await ordersApi.cancel(cancelling.id));
      toast.success(`Order #${cancelling.id} cancelled`);
      setCancelling(null);
    } catch (err) {
      toast.error(err.message);
    } finally {
      setCancelLoading(false);
    }
  };

  const changeStatus = async (order, status) => {
    setBusyId(order.id);
    try {
      replace(await ordersApi.updateStatus(order.id, status));
      toast.success(`Order #${order.id} marked as ${status}`);
    } catch (err) {
      toast.error(err.message);
    } finally {
      setBusyId(null);
    }
  };

  return (
    <>
      <PageHeader title={isAdmin ? "All orders" : "My orders"} subtitle={isAdmin ? "Manage and update every customer order." : "Track and manage everything you've ordered."} />

      <div className="mb-6 flex gap-1 overflow-x-auto rounded-xl bg-white p-1 shadow-sm ring-1 ring-slate-200">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={cx(
              "shrink-0 rounded-lg px-4 py-2 text-sm font-medium capitalize transition",
              tab === t ? "bg-indigo-600 text-white shadow-sm" : "text-slate-600 hover:bg-slate-100",
            )}
          >
            {t}
          </button>
        ))}
      </div>

      {orders.error && <Alert>{orders.error.message}</Alert>}

      {orders.loading && !orders.data ? (
        <div className="space-y-4">
          {[1, 2, 3].map((n) => (
            <Skeleton key={n} className="h-48 rounded-2xl" />
          ))}
        </div>
      ) : orders.data?.length === 0 ? (
        <Card>
          <EmptyState
            icon={Package}
            title={tab === "all" ? "No orders yet" : `No ${tab} orders`}
            text={tab === "all" ? "Add some books to your cart and check out." : "Try another status tab."}
            action={
              tab === "all" &&
              !isAdmin && (
                <Link to="/books" className="text-sm font-semibold text-indigo-600">
                  Browse books →
                </Link>
              )
            }
          />
        </Card>
      ) : (
        <div className={cx("space-y-4", orders.loading && "opacity-60")}>
          {orders.data?.map((order) => (
            <OrderCard key={order.id} order={order} isAdmin={isAdmin} busy={busyId === order.id} onCancel={setCancelling} onStatusChange={changeStatus} />
          ))}
        </div>
      )}

      <ConfirmModal
        open={Boolean(cancelling)}
        title="Cancel this order?"
        message={cancelling ? `Order #${cancelling.id} will be cancelled and the books go back into stock.` : ""}
        confirmLabel="Cancel order"
        loading={cancelLoading}
        onConfirm={confirmCancel}
        onClose={() => setCancelling(null)}
      />
    </>
  );
}
