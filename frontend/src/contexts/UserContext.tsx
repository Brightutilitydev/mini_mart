import usersStore from '@/stores/usersStore'
import { createContext } from 'react'

export const UserContext = createContext<typeof usersStore | null>(null)
