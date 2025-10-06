import { useContext } from "react";
import { UserContext } from "../hoc/UserProvider";

export function useUser() {
  const ctx = useContext(UserContext);
  if (!ctx) throw new Error("useUser must be used within UserProvider");
  return { user: ctx.user };
}

export function useUserUpdate() {
  const ctx = useContext(UserContext);
  if (!ctx) throw new Error("useUserUpdate must be used within UserProvider");
  return { setUser: ctx.setUser };
}
