import { request } from "./http";

export const authApi = {
  register: (data) => request("POST", "/auth/register", { body: data }),
  login: (email, password) => request("POST", "/auth/login", { form: { username: email, password } }),
  me: () => request("GET", "/auth/me"),
};

export const usersApi = {
  updateMe: (data) => request("PATCH", "/users/me", { body: data }),
  changePassword: (current_password, new_password) =>
    request("POST", "/users/me/password", { body: { current_password, new_password } }),
};

export const booksApi = {
  list: (params) => request("GET", "/books", { query: params }),
  genres: () => request("GET", "/books/genres"),
  get: (id) => request("GET", `/books/${id}`),
  create: (data) => request("POST", "/books", { body: data }),
  update: (id, data) => request("PATCH", `/books/${id}`, { body: data }),
  remove: (id) => request("DELETE", `/books/${id}`),
  reviews: (id) => request("GET", `/books/${id}/reviews`),
  addReview: (id, data) => request("POST", `/books/${id}/reviews`, { body: data }),
};

export const ordersApi = {
  list: (params) => request("GET", "/orders", { query: params }),
  get: (id) => request("GET", `/orders/${id}`),
  create: (items) => request("POST", "/orders", { body: { items } }),
  cancel: (id) => request("POST", `/orders/${id}/cancel`),
  updateStatus: (id, status) => request("PATCH", `/orders/${id}/status`, { body: { status } }),
};

export const dashboardApi = {
  stats: () => request("GET", "/dashboard/stats"),
};
