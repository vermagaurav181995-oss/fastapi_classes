import { ChevronLeft, ChevronRight, Pencil, Plus, Search, SearchX, ShoppingCart, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { booksApi } from "../api/endpoints";
import BookCover from "../components/BookCover";
import BookFormModal from "../components/BookFormModal";
import ConfirmModal from "../components/ConfirmModal";
import { Alert, Badge, Button, Card, EmptyState, Input, PageHeader, Select, Skeleton, Stars } from "../components/ui";
import { useAuth } from "../context/AuthContext";
import { useCart } from "../context/CartContext";
import { useToast } from "../context/ToastContext";
import { formatMoney, useApi, useDebounce } from "../lib/utils";

const PAGE_SIZE = 8;

const SORTS = [
  { value: "title", label: "Title A–Z" },
  { value: "-title", label: "Title Z–A" },
  { value: "price", label: "Price: low to high" },
  { value: "-price", label: "Price: high to low" },
  { value: "-rating", label: "Top rated" },
  { value: "-published_year", label: "Newest first" },
];

export function StockLabel({ stock }) {
  if (stock === 0) return <span className="text-xs font-medium text-rose-600">Out of stock</span>;
  if (stock <= 3) return <span className="text-xs font-medium text-amber-600">Only {stock} left</span>;
  return <span className="text-xs font-medium text-emerald-600">In stock</span>;
}

export function useAddToCart() {
  const cart = useCart();
  const toast = useToast();
  return (book, quantity = 1) => {
    const inCart = cart.quantityOf(book.id);
    if (inCart + quantity > book.stock) {
      toast.info(`You already have all ${book.stock} available copies in your cart.`);
      return;
    }
    cart.add(book, quantity);
    toast.success(`Added "${book.title}" to your cart`);
  };
}

function BookCard({ book, isAdmin, onAdd, onEdit, onDelete }) {
  return (
    <Card className="group flex flex-col overflow-hidden transition hover:shadow-md">
      <Link to={`/books/${book.id}`} className="block p-3 pb-0">
        <BookCover book={book} className="aspect-[16/9] transition duration-300 sm:aspect-[4/5] group-hover:scale-[1.02]" />
      </Link>
      <div className="flex flex-1 flex-col p-4">
        <div className="flex items-center justify-between gap-2">
          <Badge tone="indigo">{book.genre}</Badge>
          <span className="flex items-center gap-1 text-xs text-slate-500">
            <Stars value={book.avg_rating} className="size-3" />
            {book.review_count > 0 && `(${book.review_count})`}
          </span>
        </div>
        <Link to={`/books/${book.id}`} className="mt-3 line-clamp-1 font-semibold text-slate-900 hover:text-indigo-600">
          {book.title}
        </Link>
        <p className="line-clamp-1 text-sm text-slate-500">{book.author}</p>
        <div className="mt-auto flex items-end justify-between pt-4">
          <div>
            <p className="text-lg font-semibold text-slate-900">{formatMoney(book.price)}</p>
            <StockLabel stock={book.stock} />
          </div>
          <div className="flex items-center gap-1">
            {isAdmin && (
              <>
                <Button variant="ghost" size="icon" onClick={() => onEdit(book)} aria-label={`Edit ${book.title}`}>
                  <Pencil className="size-4" />
                </Button>
                <Button variant="ghost" size="icon" onClick={() => onDelete(book)} aria-label={`Delete ${book.title}`} className="hover:text-rose-600">
                  <Trash2 className="size-4" />
                </Button>
              </>
            )}
            <Button size="icon" disabled={book.stock === 0} onClick={() => onAdd(book)} aria-label={`Add ${book.title} to cart`}>
              <ShoppingCart className="size-4" />
            </Button>
          </div>
        </div>
      </div>
    </Card>
  );
}

export default function Books() {
  const { isAdmin } = useAuth();
  const toast = useToast();
  const addToCart = useAddToCart();
  const [params, setParams] = useSearchParams();

  const q = params.get("q") ?? "";
  const genre = params.get("genre") ?? "";
  const sort = params.get("sort") ?? "title";
  const page = Math.max(1, Number(params.get("page") ?? 1) || 1);

  const [search, setSearch] = useState(q);
  const debouncedSearch = useDebounce(search, 350);
  const [editing, setEditing] = useState(null);
  const [deleting, setDeleting] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const update = (changes) =>
    setParams(
      (prev) => {
        const next = new URLSearchParams(prev);
        for (const [key, value] of Object.entries(changes)) {
          if (value === null || value === "" || value === undefined) next.delete(key);
          else next.set(key, String(value));
        }
        return next;
      },
      { replace: true },
    );

  useEffect(() => {
    if (debouncedSearch !== q) update({ q: debouncedSearch, page: null });
  }, [debouncedSearch]);

  const books = useApi(() => booksApi.list({ search: q, genre, sort, page, size: PAGE_SIZE }), [q, genre, sort, page]);
  const genres = useApi(() => booksApi.genres(), []);

  const onSaved = () => {
    setEditing(null);
    books.reload();
    genres.reload();
  };

  const confirmDelete = async () => {
    setDeleteLoading(true);
    try {
      await booksApi.remove(deleting.id);
      toast.success(`Deleted "${deleting.title}"`);
      setDeleting(null);
      if (books.data?.items.length === 1 && page > 1) update({ page: page - 1 === 1 ? null : page - 1 });
      else books.reload();
      genres.reload();
    } catch (err) {
      toast.error(err.message);
    } finally {
      setDeleteLoading(false);
    }
  };

  const data = books.data;
  const filtersActive = q || genre;

  return (
    <>
      <PageHeader
        title="Books"
        subtitle={data ? `${data.total} book${data.total === 1 ? "" : "s"} in the catalog` : "Browse the catalog"}
        actions={
          isAdmin && (
            <Button onClick={() => setEditing("new")}>
              <Plus className="size-4" />
              Add book
            </Button>
          )
        }
      />

      <Card className="mb-6 p-3">
        <div className="flex flex-col gap-3 md:flex-row">
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
            <Input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search by title or author…" className="pl-9" aria-label="Search books" />
          </div>
          <Select value={genre} onChange={(e) => update({ genre: e.target.value, page: null })} className="md:w-48" aria-label="Genre">
            <option value="">All genres</option>
            {genres.data?.map((g) => (
              <option key={g} value={g}>
                {g}
              </option>
            ))}
          </Select>
          <Select value={sort} onChange={(e) => update({ sort: e.target.value === "title" ? null : e.target.value, page: null })} className="md:w-52" aria-label="Sort">
            {SORTS.map((s) => (
              <option key={s.value} value={s.value}>
                {s.label}
              </option>
            ))}
          </Select>
        </div>
      </Card>

      {books.error && <Alert>{books.error.message}</Alert>}

      {!data && !books.error ? (
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {Array.from({ length: PAGE_SIZE }, (_, i) => (
            <Skeleton key={i} className="h-[440px] rounded-2xl" />
          ))}
        </div>
      ) : data?.items.length === 0 ? (
        <Card>
          <EmptyState
            icon={SearchX}
            title="No books found"
            text={filtersActive ? "Try a different search or clear the filters." : "The catalog is empty."}
            action={
              filtersActive && (
                <Button
                  variant="secondary"
                  onClick={() => {
                    setSearch("");
                    update({ q: null, genre: null, page: null });
                  }}
                >
                  Clear filters
                </Button>
              )
            }
          />
        </Card>
      ) : (
        data && (
          <div className={books.loading ? "opacity-60 transition-opacity" : "transition-opacity"}>
            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {data.items.map((book) => (
                <BookCard key={book.id} book={book} isAdmin={isAdmin} onAdd={addToCart} onEdit={setEditing} onDelete={setDeleting} />
              ))}
            </div>

            {data.pages > 1 && (
              <div className="mt-8 flex items-center justify-between">
                <p className="text-sm text-slate-500">
                  Page <span className="font-medium text-slate-900">{data.page}</span> of {data.pages}
                </p>
                <div className="flex gap-2">
                  <Button variant="secondary" size="sm" disabled={page <= 1} onClick={() => update({ page: page - 1 === 1 ? null : page - 1 })}>
                    <ChevronLeft className="size-4" />
                    Previous
                  </Button>
                  <Button variant="secondary" size="sm" disabled={page >= data.pages} onClick={() => update({ page: page + 1 })}>
                    Next
                    <ChevronRight className="size-4" />
                  </Button>
                </div>
              </div>
            )}
          </div>
        )
      )}

      {editing && (
        <BookFormModal
          open
          book={editing === "new" ? null : editing}
          genres={genres.data ?? []}
          onClose={() => setEditing(null)}
          onSaved={onSaved}
        />
      )}

      <ConfirmModal
        open={Boolean(deleting)}
        title="Delete this book?"
        message={deleting ? `"${deleting.title}" and all of its reviews will be removed from the catalog. Past orders keep their copy of the title.` : ""}
        confirmLabel="Delete book"
        loading={deleteLoading}
        onConfirm={confirmDelete}
        onClose={() => setDeleting(null)}
      />
    </>
  );
}
