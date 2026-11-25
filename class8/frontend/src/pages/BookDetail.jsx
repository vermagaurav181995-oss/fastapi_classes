import { ArrowLeft, BookX, CalendarDays, MessageSquareText, Minus, Pencil, Plus, ShoppingCart, Trash2 } from "lucide-react";
import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { booksApi } from "../api/endpoints";
import BookCover from "../components/BookCover";
import BookFormModal from "../components/BookFormModal";
import ConfirmModal from "../components/ConfirmModal";
import { Alert, Badge, Button, Card, EmptyState, PageLoader, StarInput, Stars, Textarea } from "../components/ui";
import { useAuth } from "../context/AuthContext";
import { useCart } from "../context/CartContext";
import { useToast } from "../context/ToastContext";
import { formatDate, formatMoney, initials, useApi } from "../lib/utils";
import { StockLabel, useAddToCart } from "./Books";

function ReviewForm({ bookId, onCreated }) {
  const toast = useToast();
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    if (!rating) {
      setError("Pick a star rating first.");
      return;
    }
    setError("");
    setSaving(true);
    try {
      await booksApi.addReview(bookId, { rating, comment: comment.trim() });
      toast.success("Thanks for your review!");
      onCreated();
    } catch (err) {
      setError(err.message);
      setSaving(false);
    }
  };

  return (
    <form onSubmit={submit} className="space-y-4 rounded-xl bg-slate-50 p-5 ring-1 ring-slate-200">
      <p className="text-sm font-semibold text-slate-900">Write a review</p>
      {error && <Alert>{error}</Alert>}
      <StarInput value={rating} onChange={setRating} />
      <Textarea rows={3} maxLength={500} value={comment} onChange={(e) => setComment(e.target.value)} placeholder="What did you think? (optional)" />
      <div className="flex items-center justify-between">
        <span className="text-xs text-slate-400">{comment.length}/500</span>
        <Button type="submit" loading={saving}>
          Post review
        </Button>
      </div>
    </form>
  );
}

export default function BookDetail() {
  const { id } = useParams();
  const { user, isAdmin } = useAuth();
  const cart = useCart();
  const toast = useToast();
  const navigate = useNavigate();
  const addToCart = useAddToCart();
  const [quantity, setQuantity] = useState(1);
  const [editing, setEditing] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const book = useApi(() => booksApi.get(id), [id]);
  const reviews = useApi(() => booksApi.reviews(id), [id]);
  const genres = useApi(() => booksApi.genres(), []);

  if (book.loading && !book.data) return <PageLoader />;

  if (book.error) {
    return (
      <Card>
        <EmptyState
          icon={BookX}
          title={book.error.status === 404 ? "Book not found" : "Could not load this book"}
          text={book.error.status === 404 ? "It may have been removed from the catalog." : book.error.message}
          action={
            <Link to="/books" className="text-sm font-semibold text-indigo-600">
              ← Back to books
            </Link>
          }
        />
      </Card>
    );
  }

  const b = book.data;
  const inCart = cart.quantityOf(b.id);
  const available = Math.max(0, b.stock - inCart);
  const alreadyReviewed = reviews.data?.some((r) => r.user_id === user.id);

  const confirmDelete = async () => {
    setDeleteLoading(true);
    try {
      await booksApi.remove(b.id);
      toast.success(`Deleted "${b.title}"`);
      navigate("/books", { replace: true });
    } catch (err) {
      toast.error(err.message);
      setDeleteLoading(false);
    }
  };

  return (
    <>
      <Link to="/books" className="mb-6 inline-flex items-center gap-1.5 text-sm font-medium text-slate-500 hover:text-slate-900">
        <ArrowLeft className="size-4" />
        All books
      </Link>

      <div className="grid gap-8 md:grid-cols-[280px_1fr] lg:gap-12">
        <BookCover book={b} className="aspect-[3/4] w-full max-w-[280px] shadow-xl shadow-slate-900/10" />

        <div>
          <div className="flex flex-wrap items-center gap-2">
            <Badge tone="indigo">{b.genre}</Badge>
            <span className="inline-flex items-center gap-1 text-xs text-slate-500">
              <CalendarDays className="size-3.5" />
              {b.published_year}
            </span>
          </div>
          <h1 className="mt-3 font-display text-4xl font-semibold tracking-tight text-slate-900">{b.title}</h1>
          <p className="mt-1 text-lg text-slate-600">by {b.author}</p>

          <div className="mt-4 flex items-center gap-2">
            <Stars value={b.avg_rating} />
            <span className="text-sm text-slate-600">
              {b.review_count ? `${b.avg_rating} · ${b.review_count} review${b.review_count === 1 ? "" : "s"}` : "No reviews yet"}
            </span>
          </div>

          <p className="mt-6 max-w-2xl leading-relaxed text-slate-600">{b.description || "No description yet."}</p>

          <Card className="mt-8 max-w-xl p-5">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="text-3xl font-semibold text-slate-900">{formatMoney(b.price)}</p>
                <StockLabel stock={b.stock} />
                {inCart > 0 && <p className="mt-1 text-xs text-slate-500">{inCart} already in your cart</p>}
              </div>
              <div className="flex items-center gap-3">
                <div className="flex items-center rounded-lg ring-1 ring-slate-300">
                  <button className="p-2.5 text-slate-500 hover:text-slate-900 disabled:opacity-40" onClick={() => setQuantity((q) => q - 1)} disabled={quantity <= 1} aria-label="Decrease">
                    <Minus className="size-4" />
                  </button>
                  <span className="w-8 text-center text-sm font-semibold">{quantity}</span>
                  <button
                    className="p-2.5 text-slate-500 hover:text-slate-900 disabled:opacity-40"
                    onClick={() => setQuantity((q) => q + 1)}
                    disabled={quantity >= available}
                    aria-label="Increase"
                  >
                    <Plus className="size-4" />
                  </button>
                </div>
                <Button
                  size="lg"
                  disabled={available === 0}
                  onClick={() => {
                    addToCart(b, quantity);
                    setQuantity(1);
                  }}
                >
                  <ShoppingCart className="size-4" />
                  Add to cart
                </Button>
              </div>
            </div>
          </Card>

          {isAdmin && (
            <div className="mt-4 flex gap-2">
              <Button variant="secondary" size="sm" onClick={() => setEditing(true)}>
                <Pencil className="size-4" />
                Edit
              </Button>
              <Button variant="secondary" size="sm" onClick={() => setDeleting(true)} className="text-rose-600">
                <Trash2 className="size-4" />
                Delete
              </Button>
            </div>
          )}
        </div>
      </div>

      <section className="mt-14 max-w-3xl">
        <h2 className="flex items-center gap-2 text-xl font-semibold text-slate-900">
          <MessageSquareText className="size-5 text-indigo-600" />
          Reviews
        </h2>
        <div className="mt-6 space-y-6">
          {reviews.data && !alreadyReviewed && (
            <ReviewForm
              bookId={b.id}
              onCreated={() => {
                reviews.reload();
                book.reload();
              }}
            />
          )}
          {reviews.data?.length === 0 && <p className="text-sm text-slate-500">Be the first to review this book.</p>}
          <ul className="divide-y divide-slate-200">
            {reviews.data?.map((r) => (
              <li key={r.id} className="flex gap-4 py-5">
                <span className="grid size-10 shrink-0 place-items-center rounded-full bg-slate-100 text-sm font-semibold text-slate-600">{initials(r.user_name)}</span>
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
                    <p className="text-sm font-semibold text-slate-900">
                      {r.user_name}
                      {r.user_id === user.id && <span className="ml-2 text-xs font-normal text-indigo-600">(you)</span>}
                    </p>
                    <Stars value={r.rating} className="size-3.5" />
                    <span className="text-xs text-slate-400">{formatDate(r.created_at)}</span>
                  </div>
                  {r.comment && <p className="mt-2 text-sm leading-relaxed text-slate-600">{r.comment}</p>}
                </div>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {editing && (
        <BookFormModal
          open
          book={b}
          genres={genres.data ?? []}
          onClose={() => setEditing(false)}
          onSaved={(saved) => {
            setEditing(false);
            book.setData(saved);
          }}
        />
      )}

      <ConfirmModal
        open={deleting}
        title="Delete this book?"
        message={`"${b.title}" and all of its reviews will be removed from the catalog.`}
        confirmLabel="Delete book"
        loading={deleteLoading}
        onConfirm={confirmDelete}
        onClose={() => setDeleting(false)}
      />
    </>
  );
}
