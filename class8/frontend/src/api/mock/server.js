import { loadDb, nextId, saveDb } from "./db";

class HttpError extends Error {
  constructor(status, detail) {
    super(typeof detail === "string" ? detail : "Validation error");
    this.status = status;
    this.detail = detail;
  }
}

const validationError = (where, field, msg, type = "value_error") =>
  new HttpError(422, [{ type, loc: [where, field], msg }]);

const ok = (data) => ({ status: 200, data });
const created = (data) => ({ status: 201, data });
const noContent = () => ({ status: 204, data: null });

const TOKEN_TTL_MS = 60 * 60 * 1000;
const ORDER_STATUSES = ["pending", "paid", "shipped", "delivered", "cancelled"];
const BOOK_SORTS = { title: "title", price: "price", rating: "avg_rating", published_year: "published_year" };
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const routes = [];

function route(method, pattern, auth, handler) {
  const keys = [];
  const source = pattern.replace(/:(\w+)/g, (_, key) => {
    keys.push(key);
    return "([^/]+)";
  });
  routes.push({ method, regex: new RegExp(`^${source}/?$`), keys, auth, handler });
}

function createToken(userId) {
  return `mock.${btoa(JSON.stringify({ sub: String(userId), exp: Date.now() + TOKEN_TTL_MS }))}`;
}

function userFromToken(db, token) {
  if (!token?.startsWith("mock.")) return null;
  try {
    const payload = JSON.parse(atob(token.slice(5)));
    if (payload.exp < Date.now()) return null;
    return db.users.find((u) => u.id === Number(payload.sub)) ?? null;
  } catch {
    return null;
  }
}

const publicUser = (u) => ({ id: u.id, email: u.email, full_name: u.full_name, role: u.role, created_at: u.created_at });

function intParam(value, name) {
  const n = Number(value);
  if (!Number.isInteger(n)) throw validationError("path", name, "Input should be a valid integer", "int_parsing");
  return n;
}

function str(body, field, { min = 1, max = 200, optional = false } = {}) {
  const value = body[field];
  if (value === undefined || value === null || value === "") {
    if (optional) return undefined;
    throw validationError("body", field, "Field required", "missing");
  }
  if (typeof value !== "string") throw validationError("body", field, "Input should be a valid string", "string_type");
  const trimmed = value.trim();
  if (trimmed.length < min) throw validationError("body", field, `String should have at least ${min} character${min === 1 ? "" : "s"}`, "string_too_short");
  if (trimmed.length > max) throw validationError("body", field, `String should have at most ${max} characters`, "string_too_long");
  return trimmed;
}

function num(body, field, { gt, min, max, int = false } = {}) {
  const value = body[field];
  if (value === undefined || value === null || value === "") throw validationError("body", field, "Field required", "missing");
  const n = typeof value === "number" ? value : Number(value);
  if (Number.isNaN(n)) throw validationError("body", field, "Input should be a valid number", "float_parsing");
  if (int && !Number.isInteger(n)) throw validationError("body", field, "Input should be a valid integer", "int_parsing");
  if (gt !== undefined && !(n > gt)) throw validationError("body", field, `Input should be greater than ${gt}`, "greater_than");
  if (min !== undefined && n < min) throw validationError("body", field, `Input should be greater than or equal to ${min}`, "greater_than_equal");
  if (max !== undefined && n > max) throw validationError("body", field, `Input should be less than or equal to ${max}`, "less_than_equal");
  return n;
}

function email(body, field = "email") {
  const value = str(body, field, { max: 254 }).toLowerCase();
  if (!EMAIL_RE.test(value)) throw validationError("body", field, "value is not a valid email address");
  return value;
}

function parseBook(body, partial) {
  const fields = {
    title: () => str(body, "title", { max: 200 }),
    author: () => str(body, "author", { max: 120 }),
    genre: () => str(body, "genre", { max: 50 }),
    description: () => str(body, "description", { min: 0, max: 2000, optional: true }) ?? "",
    price: () => Math.round(num(body, "price", { gt: 0 }) * 100) / 100,
    stock: () => num(body, "stock", { min: 0, int: true }),
    published_year: () => num(body, "published_year", { min: 1000, max: new Date().getFullYear(), int: true }),
  };
  const out = {};
  for (const [key, parse] of Object.entries(fields)) {
    if (partial && !(key in body)) continue;
    out[key] = parse();
  }
  return out;
}

function withRating(db, book) {
  const reviews = db.reviews.filter((r) => r.book_id === book.id);
  const avg = reviews.length ? reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length : 0;
  return { ...book, avg_rating: Math.round(avg * 10) / 10, review_count: reviews.length };
}

function findBook(db, id) {
  const book = db.books.find((b) => b.id === id);
  if (!book) throw new HttpError(404, "Book not found");
  return book;
}

function orderOut(db, order) {
  const owner = db.users.find((u) => u.id === order.user_id);
  return { ...order, user_name: owner?.full_name ?? "Deleted user" };
}

function findOrderFor(db, id, user) {
  const order = db.orders.find((o) => o.id === id);
  if (!order || (user.role !== "admin" && order.user_id !== user.id)) throw new HttpError(404, "Order not found");
  return order;
}

function restock(db, order) {
  for (const item of order.items) {
    const book = db.books.find((b) => b.id === item.book_id);
    if (book) book.stock += item.quantity;
  }
}

const round2 = (n) => Math.round(n * 100) / 100;

route("POST", "/auth/register", null, ({ db, body }) => {
  const data = {
    full_name: str(body, "full_name", { max: 100 }),
    email: email(body),
    password: str(body, "password", { min: 8, max: 128 }),
  };
  if (db.users.some((u) => u.email === data.email)) throw new HttpError(409, "Email already registered");
  const user = { id: nextId(db, "users"), ...data, role: "user", created_at: new Date().toISOString() };
  db.users.push(user);
  return created(publicUser(user));
});

route("POST", "/auth/login", null, ({ db, body }) => {
  const user = db.users.find((u) => u.email === String(body.username ?? "").trim().toLowerCase());
  if (!user || user.password !== body.password) throw new HttpError(401, "Incorrect email or password");
  return ok({ access_token: createToken(user.id), token_type: "bearer" });
});

route("GET", "/auth/me", "user", ({ user }) => ok(publicUser(user)));

route("PATCH", "/users/me", "user", ({ user, body }) => {
  if ("full_name" in body) user.full_name = str(body, "full_name", { max: 100 });
  return ok(publicUser(user));
});

route("POST", "/users/me/password", "user", ({ user, body }) => {
  const current = str(body, "current_password", { max: 128 });
  const next = str(body, "new_password", { min: 8, max: 128 });
  if (current !== user.password) throw new HttpError(400, "Current password is incorrect");
  user.password = next;
  return noContent();
});

route("GET", "/books/genres", null, ({ db }) => ok([...new Set(db.books.map((b) => b.genre))].sort()));

route("GET", "/books", null, ({ db, query }) => {
  const page = query.page ? Number(query.page) : 1;
  const size = query.size ? Number(query.size) : 8;
  if (!Number.isInteger(page) || page < 1) throw validationError("query", "page", "Input should be greater than or equal to 1");
  if (!Number.isInteger(size) || size < 1 || size > 50) throw validationError("query", "size", "Input should be between 1 and 50");

  const sort = query.sort || "title";
  const sortKey = BOOK_SORTS[sort.replace(/^-/, "")];
  if (!sortKey) throw validationError("query", "sort", `Input should be one of: ${Object.keys(BOOK_SORTS).map((k) => `${k}, -${k}`).join(", ")}`);
  const direction = sort.startsWith("-") ? -1 : 1;

  const search = (query.search ?? "").trim().toLowerCase();
  let items = db.books.map((b) => withRating(db, b));
  if (search) items = items.filter((b) => b.title.toLowerCase().includes(search) || b.author.toLowerCase().includes(search));
  if (query.genre) items = items.filter((b) => b.genre === query.genre);
  if (query.in_stock === "true") items = items.filter((b) => b.stock > 0);
  items.sort((a, b) => {
    const x = a[sortKey];
    const y = b[sortKey];
    return (typeof x === "string" ? x.localeCompare(y) : x - y) * direction;
  });

  const total = items.length;
  return ok({ items: items.slice((page - 1) * size, page * size), total, page, size, pages: Math.max(1, Math.ceil(total / size)) });
});

route("GET", "/books/:id", null, ({ db, params }) => ok(withRating(db, findBook(db, intParam(params.id, "book_id")))));

route("POST", "/books", "admin", ({ db, body }) => {
  const book = { id: nextId(db, "books"), ...parseBook(body, false) };
  db.books.push(book);
  return created(withRating(db, book));
});

route("PATCH", "/books/:id", "admin", ({ db, params, body }) => {
  const book = findBook(db, intParam(params.id, "book_id"));
  Object.assign(book, parseBook(body, true));
  return ok(withRating(db, book));
});

route("DELETE", "/books/:id", "admin", ({ db, params }) => {
  const book = findBook(db, intParam(params.id, "book_id"));
  db.books = db.books.filter((b) => b.id !== book.id);
  db.reviews = db.reviews.filter((r) => r.book_id !== book.id);
  return noContent();
});

route("GET", "/books/:id/reviews", null, ({ db, params }) => {
  const book = findBook(db, intParam(params.id, "book_id"));
  const reviews = db.reviews
    .filter((r) => r.book_id === book.id)
    .sort((a, b) => b.created_at.localeCompare(a.created_at))
    .map((r) => ({ ...r, user_name: db.users.find((u) => u.id === r.user_id)?.full_name ?? "Deleted user" }));
  return ok(reviews);
});

route("POST", "/books/:id/reviews", "user", ({ db, params, body, user }) => {
  const book = findBook(db, intParam(params.id, "book_id"));
  const rating = num(body, "rating", { min: 1, max: 5, int: true });
  const comment = str(body, "comment", { min: 0, max: 500, optional: true }) ?? "";
  if (db.reviews.some((r) => r.book_id === book.id && r.user_id === user.id)) throw new HttpError(409, "You have already reviewed this book");
  const review = { id: nextId(db, "reviews"), book_id: book.id, user_id: user.id, rating, comment, created_at: new Date().toISOString() };
  db.reviews.push(review);
  return created({ ...review, user_name: user.full_name });
});

route("GET", "/orders", "user", ({ db, query, user }) => {
  if (query.status && !ORDER_STATUSES.includes(query.status)) throw validationError("query", "status", `Input should be one of: ${ORDER_STATUSES.join(", ")}`, "enum");
  let orders = user.role === "admin" ? db.orders : db.orders.filter((o) => o.user_id === user.id);
  if (query.status) orders = orders.filter((o) => o.status === query.status);
  orders = [...orders].sort((a, b) => b.created_at.localeCompare(a.created_at));
  if (query.limit) orders = orders.slice(0, Number(query.limit));
  return ok(orders.map((o) => orderOut(db, o)));
});

route("POST", "/orders", "user", ({ db, body, user }) => {
  if (!Array.isArray(body.items) || body.items.length === 0) throw validationError("body", "items", "List should have at least 1 item after validation", "too_short");
  const items = body.items.map((raw, index) => {
    const quantity = num(raw, "quantity", { min: 1, int: true });
    const book = db.books.find((b) => b.id === Number(raw.book_id));
    if (!book) throw new HttpError(404, `Book ${raw.book_id} not found (item ${index + 1})`);
    if (book.stock < quantity) throw new HttpError(400, book.stock === 0 ? `"${book.title}" is out of stock` : `Only ${book.stock} left of "${book.title}"`);
    return { book, quantity };
  });
  for (const { book, quantity } of items) book.stock -= quantity;
  const lines = items.map(({ book, quantity }) => ({ book_id: book.id, title: book.title, price: book.price, quantity }));
  const order = {
    id: nextId(db, "orders"),
    user_id: user.id,
    items: lines,
    total: round2(lines.reduce((sum, l) => sum + l.price * l.quantity, 0)),
    status: "pending",
    created_at: new Date().toISOString(),
  };
  db.orders.push(order);
  return created(orderOut(db, order));
});

route("GET", "/orders/:id", "user", ({ db, params, user }) => ok(orderOut(db, findOrderFor(db, intParam(params.id, "order_id"), user))));

route("POST", "/orders/:id/cancel", "user", ({ db, params, user }) => {
  const order = findOrderFor(db, intParam(params.id, "order_id"), user);
  if (order.user_id !== user.id) throw new HttpError(403, "You can only cancel your own orders");
  if (order.status !== "pending") throw new HttpError(400, "Only pending orders can be cancelled");
  order.status = "cancelled";
  restock(db, order);
  return ok(orderOut(db, order));
});

route("PATCH", "/orders/:id/status", "admin", ({ db, params, body, user }) => {
  const order = findOrderFor(db, intParam(params.id, "order_id"), user);
  if (!ORDER_STATUSES.includes(body.status)) throw validationError("body", "status", `Input should be one of: ${ORDER_STATUSES.join(", ")}`, "enum");
  if (order.status === "cancelled") throw new HttpError(400, "Cancelled orders cannot be changed");
  if (body.status === "cancelled") restock(db, order);
  order.status = body.status;
  return ok(orderOut(db, order));
});

route("GET", "/dashboard/stats", "user", ({ db, user }) => {
  if (user.role === "admin") {
    const active = db.orders.filter((o) => o.status !== "cancelled");
    return ok({
      role: "admin",
      books_count: db.books.length,
      users_count: db.users.filter((u) => u.role === "user").length,
      orders_count: db.orders.length,
      pending_orders: db.orders.filter((o) => o.status === "pending").length,
      revenue: round2(active.reduce((sum, o) => sum + o.total, 0)),
      low_stock: db.books.filter((b) => b.stock <= 3).sort((a, b) => a.stock - b.stock).map((b) => ({ id: b.id, title: b.title, stock: b.stock })),
    });
  }
  const mine = db.orders.filter((o) => o.user_id === user.id);
  return ok({
    role: "user",
    orders_count: mine.length,
    pending_orders: mine.filter((o) => o.status === "pending").length,
    total_spent: round2(mine.filter((o) => o.status !== "cancelled").reduce((sum, o) => sum + o.total, 0)),
    reviews_count: db.reviews.filter((r) => r.user_id === user.id).length,
  });
});

export function handle(method, path, { query = {}, body, token } = {}) {
  const db = loadDb();
  const matching = routes.filter((r) => r.regex.test(path));
  if (matching.length === 0) return { status: 404, data: { detail: "Not Found" } };
  const match = matching.find((r) => r.method === method);
  if (!match) return { status: 405, data: { detail: "Method Not Allowed" } };

  const values = path.match(match.regex).slice(1);
  const params = Object.fromEntries(match.keys.map((key, i) => [key, decodeURIComponent(values[i])]));

  try {
    let user = null;
    if (match.auth) {
      user = userFromToken(db, token);
      if (!user) throw new HttpError(401, token ? "Could not validate credentials" : "Not authenticated");
      if (match.auth === "admin" && user.role !== "admin") throw new HttpError(403, "Not enough permissions");
    }
    const { status, data } = match.handler({ db, params, query, body: body ?? {}, user });
    saveDb(db);
    return { status, data: data === null ? null : JSON.parse(JSON.stringify(data)) };
  } catch (error) {
    if (error instanceof HttpError) return { status: error.status, data: { detail: error.detail } };
    console.error(error);
    return { status: 500, data: { detail: "Internal Server Error" } };
  }
}
