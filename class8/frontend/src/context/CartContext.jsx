import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

const CART_KEY = "booknest-cart";
const CartContext = createContext(null);

function readCart() {
  try {
    return JSON.parse(localStorage.getItem(CART_KEY)) ?? [];
  } catch {
    return [];
  }
}

export function CartProvider({ children }) {
  const [items, setItems] = useState(readCart);

  useEffect(() => {
    try {
      localStorage.setItem(CART_KEY, JSON.stringify(items));
    } catch {
      return;
    }
  }, [items]);

  const add = useCallback((book, quantity = 1) => {
    setItems((current) => {
      const existing = current.find((i) => i.book_id === book.id);
      if (existing) {
        return current.map((i) =>
          i.book_id === book.id ? { ...i, stock: book.stock, quantity: Math.min(book.stock, i.quantity + quantity) } : i,
        );
      }
      return [
        ...current,
        { book_id: book.id, title: book.title, author: book.author, price: book.price, stock: book.stock, quantity: Math.min(book.stock, quantity) },
      ];
    });
  }, []);

  const setQuantity = useCallback((bookId, quantity) => {
    setItems((current) =>
      current.map((i) => (i.book_id === bookId ? { ...i, quantity: Math.max(1, Math.min(i.stock, quantity)) } : i)),
    );
  }, []);

  const remove = useCallback((bookId) => setItems((current) => current.filter((i) => i.book_id !== bookId)), []);
  const clear = useCallback(() => setItems([]), []);

  const value = useMemo(() => {
    const count = items.reduce((sum, i) => sum + i.quantity, 0);
    const total = Math.round(items.reduce((sum, i) => sum + i.price * i.quantity, 0) * 100) / 100;
    const quantityOf = (bookId) => items.find((i) => i.book_id === bookId)?.quantity ?? 0;
    return { items, count, total, add, setQuantity, remove, clear, quantityOf };
  }, [items, add, setQuantity, remove, clear]);

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export const useCart = () => useContext(CartContext);
