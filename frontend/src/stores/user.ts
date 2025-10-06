import { map, computed } from "nanostores"

export interface User {
    id: string
    first_name: string
    last_name: string
    email: string
    phone_number?: string
    whatsapp_number: string
    address?: string
    is_admin: boolean
}

export const $user = map<Partial<User>>({})
export const $loggedIn = computed($user, user => Object.keys(user).length > 0)

export const login = (user: User) => {
    $user.set(user)
}

export const logout = () => {
    $user.set({})
}

export function useUser() {
    return {
        user: $user.get(),
        loggedIn: $loggedIn.get()
    }
}

export function useUserUpdate() {
    return {
        login,
        logout
    }
}
