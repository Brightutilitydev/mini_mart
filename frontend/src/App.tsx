import "./styles/App.scss"

import { UserProvider } from "./hoc/UserProvider"
import AppRouter from "./AppRouter"

function App() {
  return (
    <UserProvider>
      <AppRouter />
    </UserProvider>
  )
}

export default App

