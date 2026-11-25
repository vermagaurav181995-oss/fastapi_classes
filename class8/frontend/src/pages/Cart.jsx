import { ArrowRight, Lock, Minus, Plus, ShoppingBag, Trash2 } from "lucide-react";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ordersApi } from "../api/endpoints";
import BookCover from "../components/BookCover";
import { Alert, Button, Card, EmptyState, PageHeader } from "../components/ui";
import { useCart } from "../context/CartContext";
import { useToast } from "../context/ToastContext";
import { formatMoney } from "../lib/utils";

export default function Cart() {
  const cart = useCart();
  const toast = useToast();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [placing, setPlacing] = useState(false);

  const checkout = async () => {
    setError("");
    setPlacing(true);
    try {
      const order = await ordersApi.create(cart.items.map((i) => ({ book_id: i.book_id, quantity: i.quantity })));
      cart.clear();
      toast.success(`Order #${order.id} placed. Total ${formatMoney(order.total)}`);
      navigate("/orders");
    } catch (err) {
      setError(err.message);
      setPlacing(false);
    }
  };

  if (cart.items.length === 0) {
    return (
      <>
        <PageHeader title="Your cart" />
        <Card>
          <EmptyState
            icon={ShoppingBag}
            title="Your cart is empty"
            text="Books you add from the catalog will wait for you here."
            action={
              <Button onClick={() => navigate("/books")}>
                Browse books <ArrowRight className="size-4" />
              </Button>
            }
          />
        </Card>
      </>
    );
  }

  return (
    <>
      <PageHeader title="Your cart" subtitle={`${cart.count} item${cart.count === 1 ? "" : "s"} ready for checkout`} />

      <div className="grid items-start gap-8 lg:grid-cols-[1fr_340px]">
        <Card>
          <ul className="divide-y divide-slate-100">
            {cart.items.map((item) => (
              <li key={item.book_id} className="flex gap-4 p-5">
                <Link to={`/books/${item.book_id}`} className="shrink-0">
                  <BookCover book={{ id: item.book_id }} compact className="h-24 w-[72px] rounded-lg" />
                </Link>
                <div className="flex min-w-0 flex-1 flex-col">
                  <div className="flex items-start justify-between gap-4">
                    <div className="min-w-0">
                      <Link to={`/books/${item.book_id}`} className="line-clamp-1 font-semibold text-slate-900 hover:text-indigo-600">
                        {item.title}
                      </Link>
                      <p className="text-sm text-slate-500">{item.author}</p>
                    </div>
                    <p className="shrink-0 font-semibold text-slate-900">{formatMoney(item.price * item.quantity)}</p>
                  </div>
                  <div className="mt-auto flex items-center justify-between pt-3">
                    <div className="flex items-center rounded-lg ring-1 ring-slate-300">
                      <button
                        className="p-2 text-slate-500 hover:text-slate-900 disabled:opacity-40"
                        onClick={() => cart.setQuantity(item.book_id, item.quantity - 1)}
                        disabled={item.quantity <= 1}
                        aria-label="Decrease quantity"
                      >
                        <Minus className="size-3.5" />
                      </button>
                      <span className="w-8 text-center text-sm font-semibold">{item.quantity}</span>
                      <button
                        className="p-2 text-slate-500 hover:text-slate-900 disabled:opacity-40"
                        onClick={() => cart.setQuantity(item.book_id, item.quantity + 1)}
                        disabled={item.quantity >= item.stock}
                        aria-label="Increase quantity"
                      >
                        <Plus className="size-3.5" />
                      </button>
                    </div>
                    <span className="hidden text-xs text-slate-400 sm:inline">{formatMoney(item.price)} each</span>
                    <button onClick={() => cart.remove(item.book_id)} className="flex items-center gap-1 text-sm text-slate-500 hover:text-rose-600">
                      <Trash2 className="size-4" />
                      Remove
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </Card>

        <Card className="h-fit p-6 lg:sticky lg:top-8">
          <h2 className="font-semibold text-slate-900">Order summary</h2>
          <dl className="mt-5 space-y-3 text-sm">
            <div className="flex justify-between">
              <dt className="text-slate-500">Subtotal</dt>
              <dd className="font-medium text-slate-900">{formatMoney(cart.total)}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-500">Shipping</dt>
              <dd className="font-medium text-emerald-600">Free</dd>
            </div>
            <div className="flex justify-between border-t border-slate-100 pt-3 text-base">
              <dt className="font-semibold text-slate-900">Total</dt>
              <dd className="font-semibold text-slate-900">{formatMoney(cart.total)}</dd>
            </div>
          </dl>
          {error && (
            <div className="mt-5">
              <Alert>{error}</Alert>
            </div>
          )}
          <Button size="lg" className="mt-6 w-full" loading={placing} onClick={checkout}>
            Place order
          </Button>
          <p className="mt-3 flex items-center justify-center gap-1.5 text-xs text-slate-400">
            <Lock className="size-3" />
            Mock checkout: no payment is taken
          </p>
        </Card>
      </div>
    </>
  );
}
