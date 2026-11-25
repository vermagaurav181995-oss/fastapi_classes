import { useState } from "react";
import { booksApi } from "../api/endpoints";
import { useToast } from "../context/ToastContext";
import { Alert, Button, Field, Input, Modal, Textarea } from "./ui";

const EMPTY = { title: "", author: "", genre: "", price: "", stock: "", published_year: "", description: "" };

function toForm(book) {
  if (!book) return EMPTY;
  return {
    title: book.title,
    author: book.author,
    genre: book.genre,
    price: String(book.price),
    stock: String(book.stock),
    published_year: String(book.published_year),
    description: book.description ?? "",
  };
}

function validate(form) {
  const errors = {};
  if (!form.title.trim()) errors.title = "Title is required";
  if (!form.author.trim()) errors.author = "Author is required";
  if (!form.genre.trim()) errors.genre = "Genre is required";
  if (!(Number(form.price) > 0)) errors.price = "Price must be greater than 0";
  if (form.stock === "" || !Number.isInteger(Number(form.stock)) || Number(form.stock) < 0) errors.stock = "Stock must be a whole number ≥ 0";
  const year = Number(form.published_year);
  if (!Number.isInteger(year) || year < 1000 || year > new Date().getFullYear()) errors.published_year = "Enter a valid year";
  return errors;
}

export default function BookFormModal({ open, book, genres = [], onClose, onSaved }) {
  const toast = useToast();
  const [form, setForm] = useState(() => toForm(book));
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState("");
  const [saving, setSaving] = useState(false);
  const isEdit = Boolean(book);

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const submit = async (e) => {
    e.preventDefault();
    const found = validate(form);
    setErrors(found);
    setServerError("");
    if (Object.keys(found).length) return;

    const payload = {
      title: form.title.trim(),
      author: form.author.trim(),
      genre: form.genre.trim(),
      price: Number(form.price),
      stock: Number(form.stock),
      published_year: Number(form.published_year),
      description: form.description.trim(),
    };

    setSaving(true);
    try {
      const saved = isEdit ? await booksApi.update(book.id, payload) : await booksApi.create(payload);
      toast.success(isEdit ? `Saved "${saved.title}"` : `Added "${saved.title}" to the catalog`);
      onSaved(saved);
    } catch (err) {
      setErrors(err.fieldErrors());
      setServerError(err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <Modal
      open={open}
      onClose={onClose}
      size="lg"
      title={isEdit ? "Edit book" : "Add a new book"}
      description={isEdit ? `Update the details for "${book.title}".` : "New books appear in the catalog straight away."}
      footer={
        <>
          <Button variant="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="book-form" loading={saving}>
            {isEdit ? "Save changes" : "Add book"}
          </Button>
        </>
      }
    >
      <form id="book-form" onSubmit={submit} className="grid gap-4 sm:grid-cols-2" noValidate>
        {serverError && (
          <div className="sm:col-span-2">
            <Alert>{serverError}</Alert>
          </div>
        )}
        <Field label="Title" error={errors.title} className="sm:col-span-2">
          {({ id, invalid }) => <Input id={id} invalid={invalid} value={form.title} onChange={set("title")} placeholder="e.g. The Left Hand of Darkness" />}
        </Field>
        <Field label="Author" error={errors.author}>
          {({ id, invalid }) => <Input id={id} invalid={invalid} value={form.author} onChange={set("author")} />}
        </Field>
        <Field label="Genre" error={errors.genre}>
          {({ id, invalid }) => (
            <>
              <Input id={id} invalid={invalid} value={form.genre} onChange={set("genre")} list="genre-options" />
              <datalist id="genre-options">
                {genres.map((g) => (
                  <option key={g} value={g} />
                ))}
              </datalist>
            </>
          )}
        </Field>
        <Field label="Price (USD)" error={errors.price}>
          {({ id, invalid }) => <Input id={id} invalid={invalid} type="number" min="0" step="0.01" value={form.price} onChange={set("price")} />}
        </Field>
        <Field label="Stock" error={errors.stock}>
          {({ id, invalid }) => <Input id={id} invalid={invalid} type="number" min="0" step="1" value={form.stock} onChange={set("stock")} />}
        </Field>
        <Field label="Published year" error={errors.published_year}>
          {({ id, invalid }) => <Input id={id} invalid={invalid} type="number" value={form.published_year} onChange={set("published_year")} />}
        </Field>
        <Field label="Description" error={errors.description} hint="Optional, up to 2000 characters." className="sm:col-span-2">
          {({ id, invalid }) => <Textarea id={id} invalid={invalid} rows={4} value={form.description} onChange={set("description")} />}
        </Field>
      </form>
    </Modal>
  );
}
