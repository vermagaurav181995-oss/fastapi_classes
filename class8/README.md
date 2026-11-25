# Class 8: BookNest (React UI first, API next)

## Start the UI

```bash
cd class8/frontend
npm install
npm run dev
```

Open http://localhost:5173 and sign in with one of the demo accounts:

| Email | Password | Role |
|---|---|---|
| reader@booknest.dev | reader123 | user |
| admin@booknest.dev | admin123 | admin |

Everything is mocked: no backend is needed yet.
- The data lives in your browser's localStorage.
- The **API** button in the bottom-right corner shows every request the UI makes.
- The reset button in that panel restores the seed data.

## Pages

| Route | Page | Who |
|---|---|---|
| `/login`, `/register` | Sign in and sign up | public |
| `/` | Dashboard: stats, recent orders, top rated books (admins also see low stock) | logged in |
| `/books` | Catalog: search, genre filter, sort, pagination (admins can also add, edit and delete) | logged in |
| `/books/:id` | Book details, add to cart, reviews | logged in |
| `/cart` | Cart and checkout | logged in |
| `/orders` | Orders with status tabs (users can cancel; admins can change status) | logged in |
| `/profile` | Edit your name, change your password | logged in |

## Next step: the FastAPI backend

[API_CONTRACT.md](API_CONTRACT.md) lists every endpoint, schema and error the UI expects.
To point the UI at a real backend instead of the mock, run:

```bash
cp .env.example .env
```

Then edit `.env`:

```bash
VITE_USE_MOCK=false
VITE_API_URL=http://localhost:8000
```

Restart `npm run dev` after changing `.env`.

## Where things are

```
frontend/src/
├── api/
│   ├── endpoints.js     every API call the UI makes (method + path)
│   ├── http.js          request(): mock or real fetch, token, errors
│   └── mock/
│       ├── server.js    fake FastAPI: routes, auth, validation, status codes
│       └── db.js        seed data, saved to localStorage
├── context/             AuthContext, CartContext, ToastContext
├── components/          Layout, route guards, UI kit, modals, API log
└── pages/               Login, Register, Dashboard, Books, BookDetail, Cart, Orders, Profile
```
