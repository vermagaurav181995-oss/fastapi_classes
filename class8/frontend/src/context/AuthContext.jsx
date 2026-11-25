import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { authApi } from "../api/endpoints";
import { tokenStore } from "../api/http";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(() => Boolean(tokenStore.get()));

  useEffect(() => {
    if (!tokenStore.get()) return;
    authApi
      .me()
      .then(setUser)
      .catch(() => tokenStore.clear())
      .finally(() => setLoading(false));
  }, []);

  const logout = useCallback(() => {
    tokenStore.clear();
    setUser(null);
  }, []);

  useEffect(() => {
    window.addEventListener("booknest:unauthorized", logout);
    return () => window.removeEventListener("booknest:unauthorized", logout);
  }, [logout]);

  const login = useCallback(async (email, password) => {
    const { access_token } = await authApi.login(email, password);
    tokenStore.set(access_token);
    const me = await authApi.me();
    setUser(me);
    return me;
  }, []);

  const register = useCallback(
    async (data) => {
      await authApi.register(data);
      return login(data.email, data.password);
    },
    [login],
  );

  const value = useMemo(
    () => ({ user, loading, isAdmin: user?.role === "admin", login, register, logout, setUser }),
    [user, loading, login, register, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);
