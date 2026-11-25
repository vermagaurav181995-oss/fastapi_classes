const STORAGE_KEY = "booknest-mock-db-v1";

const daysAgo = (days) => new Date(Date.now() - days * 86_400_000).toISOString();

function seed() {
  const users = [
    { id: 1, email: "admin@booknest.dev", full_name: "Ada Admin", password: "admin123", role: "admin", created_at: daysAgo(180) },
    { id: 2, email: "reader@booknest.dev", full_name: "Riya Reader", password: "reader123", role: "user", created_at: daysAgo(60) },
    { id: 3, email: "sam@booknest.dev", full_name: "Sam Patel", password: "sam12345", role: "user", created_at: daysAgo(21) },
  ];

  const books = [
    { id: 1, title: "Dune", author: "Frank Herbert", genre: "Science Fiction", price: 9.99, stock: 14, published_year: 1965, description: "A desert planet, a priceless spice and a young heir caught in a war between great houses. An epic about power, ecology and prophecy." },
    { id: 2, title: "Project Hail Mary", author: "Andy Weir", genre: "Science Fiction", price: 14.5, stock: 6, published_year: 2021, description: "A lone astronaut wakes up with no memory and a mission to save Earth. Clever science, humour and an unlikely friendship." },
    { id: 3, title: "Neuromancer", author: "William Gibson", genre: "Science Fiction", price: 8.25, stock: 2, published_year: 1984, description: "The novel that defined cyberpunk: a washed-up hacker is hired for one last job inside the matrix." },
    { id: 4, title: "The Hobbit", author: "J.R.R. Tolkien", genre: "Fantasy", price: 10.99, stock: 20, published_year: 1937, description: "Bilbo Baggins leaves his comfortable hole for an adventure with thirteen dwarves, a wizard and a dragon." },
    { id: 5, title: "The Name of the Wind", author: "Patrick Rothfuss", genre: "Fantasy", price: 12.0, stock: 0, published_year: 2007, description: "Kvothe tells the true story of how a gifted orphan became the most notorious wizard of his age." },
    { id: 6, title: "1984", author: "George Orwell", genre: "Classics", price: 7.5, stock: 11, published_year: 1949, description: "Big Brother is watching. A chilling picture of surveillance, propaganda and the fight to think freely." },
    { id: 7, title: "Pride and Prejudice", author: "Jane Austen", genre: "Classics", price: 6.99, stock: 9, published_year: 1813, description: "Elizabeth Bennet and Mr. Darcy trade sharp words in a witty story about manners, money and first impressions." },
    { id: 8, title: "Sapiens", author: "Yuval Noah Harari", genre: "Non-Fiction", price: 16.99, stock: 7, published_year: 2011, description: "A brief history of humankind, from foraging bands to global empires and the age of algorithms." },
    { id: 9, title: "Educated", author: "Tara Westover", genre: "Non-Fiction", price: 13.25, stock: 3, published_year: 2018, description: "A memoir of growing up off the grid in Idaho and finding a way out through education." },
    { id: 10, title: "Atomic Habits", author: "James Clear", genre: "Self-Help", price: 15.0, stock: 25, published_year: 2018, description: "Small changes, remarkable results: a practical framework for building good habits and breaking bad ones." },
    { id: 11, title: "The Pragmatic Programmer", author: "David Thomas & Andrew Hunt", genre: "Technology", price: 39.99, stock: 5, published_year: 1999, description: "Timeless advice on writing flexible, maintainable code and growing as a software developer." },
    { id: 12, title: "Clean Code", author: "Robert C. Martin", genre: "Technology", price: 34.5, stock: 8, published_year: 2008, description: "Principles and patterns for writing code that other people can read, change and trust." },
  ];

  const reviews = [
    { id: 1, book_id: 1, user_id: 2, rating: 5, comment: "Slow start, then I couldn't put it down. The world-building is unreal.", created_at: daysAgo(40) },
    { id: 2, book_id: 1, user_id: 3, rating: 4, comment: "Dense but rewarding. Keep the glossary open!", created_at: daysAgo(12) },
    { id: 3, book_id: 2, user_id: 2, rating: 5, comment: "Rocky is the best character of the decade.", created_at: daysAgo(30) },
    { id: 4, book_id: 4, user_id: 3, rating: 5, comment: "Cosy and adventurous at the same time.", created_at: daysAgo(15) },
    { id: 5, book_id: 6, user_id: 2, rating: 4, comment: "Scarily relevant today.", created_at: daysAgo(25) },
    { id: 6, book_id: 10, user_id: 3, rating: 4, comment: "Practical. The 1% better idea really stuck with me.", created_at: daysAgo(9) },
    { id: 7, book_id: 11, user_id: 2, rating: 5, comment: "Every developer should read this once a year.", created_at: daysAgo(18) },
    { id: 8, book_id: 8, user_id: 3, rating: 3, comment: "Big ideas, a bit sweeping in places.", created_at: daysAgo(5) },
  ];

  const orders = [
    { id: 1, user_id: 2, items: [{ book_id: 1, title: "Dune", price: 9.99, quantity: 1 }, { book_id: 4, title: "The Hobbit", price: 10.99, quantity: 1 }], total: 20.98, status: "delivered", created_at: daysAgo(35) },
    { id: 2, user_id: 2, items: [{ book_id: 11, title: "The Pragmatic Programmer", price: 39.99, quantity: 1 }], total: 39.99, status: "shipped", created_at: daysAgo(6) },
    { id: 3, user_id: 2, items: [{ book_id: 10, title: "Atomic Habits", price: 15.0, quantity: 2 }], total: 30.0, status: "pending", created_at: daysAgo(1) },
    { id: 4, user_id: 3, items: [{ book_id: 8, title: "Sapiens", price: 16.99, quantity: 1 }, { book_id: 6, title: "1984", price: 7.5, quantity: 1 }], total: 24.49, status: "paid", created_at: daysAgo(3) },
  ];

  return {
    users,
    books,
    reviews,
    orders,
    nextId: { users: 4, books: 13, reviews: 9, orders: 5 },
  };
}

export function loadDb() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
  }
  const db = seed();
  saveDb(db);
  return db;
}

export function saveDb(db) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(db));
  } catch {
  }
}

export function resetDb() {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
  }
}

export function nextId(db, table) {
  const id = db.nextId[table];
  db.nextId[table] += 1;
  return id;
}
