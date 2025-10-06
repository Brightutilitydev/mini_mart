import { TokenContext } from '../contexts/TokenContext'
import { useContext } from 'react'

const useToken = () => {
  const tokenManager = useContext(TokenContext)

  if (!tokenManager) throw new Error('You cannot call this hook outside a user provider')

  return tokenManager
}

export default useToken
