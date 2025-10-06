/* eslint-disable react-refresh/only-export-components */
import { createContext, useState, useEffect, useRef, useLayoutEffect, type FC, type ReactNode, memo } from "react";
import { getAccessToken } from "../lib/requestUtils";
import { markInterceptorReady } from "../lib/tokenReady.ts";
import { axiosConfig } from "../lib/axiosConfig.ts";
import { TokenContext } from "../contexts/TokenContext.tsx";

export interface User {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone_number?: string;
  whatsapp_number: string;
  address?: string;
  is_admin: boolean;
}

interface UserContextType {
  user: User | null;
  setUser: (user: User | null) => void
}

export const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: FC<{
  children: ReactNode
}> = memo(({ children }) => {
  const [token, setToken] = useState<string>('')
  const [ user, setUser ] = useState<User | null>(null)
  const tokenRef = useRef<typeof token>(token)

  useEffect(() => {
    tokenRef.current = token
  }, [token])

  useEffect(() => {
    let handler: number | undefined
    if (token) {
      handler = axiosConfig.interceptors.request.use(config => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        config.headers.Authorization = !(config as any)._retry
          ? `Bearer ${tokenRef.current}`
          : config.headers.Authorization
        return config
      })

      markInterceptorReady()
    }

    return () => {
      if (handler !== undefined) {
        axiosConfig.interceptors.request.eject(handler)
      }
    }
  }, [token])

  useLayoutEffect(() => {
    const handler = axiosConfig.interceptors.response.use(
      response => response,
      async function (error) {
        const originalRequest = error.config
        if (error.response.status === 403 && error.response.data.message === 'Access Expired') {
          try {
            const tokenResponse = await getAccessToken()
            setToken(tokenResponse?.token || ' ')

            originalRequest.headers.Authorization = `Bearer ${tokenResponse?.token}`
            originalRequest._retry = true
            return axiosConfig(originalRequest)
          } catch (err) {
            setToken('')
            return Promise.reject(err)
          }
        } else {
          return Promise.reject(error)
        }
      }
    )

    return () => axiosConfig.interceptors.response.eject(handler)
  }, [setToken])

  return (
    <UserContext.Provider value={{ user, setUser }}>
      <TokenContext.Provider value={{ token: tokenRef, setToken }}>
        {children}
      </TokenContext.Provider>
    </UserContext.Provider>
  )
})