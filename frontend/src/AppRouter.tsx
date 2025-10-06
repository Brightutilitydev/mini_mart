import { createBrowserRouter } from "react-router";
import { RouterProvider } from 'react-router/dom'
import { memo, Suspense, useMemo, type Dispatch, type MutableRefObject } from "react";
import { rootLoader } from "./lib/routeLoaders";
import LoadingScreen from "./components/LoadingScreen";
import { UserProvider } from "./hoc/UserProvider";
import Home from "./components/pages/Home";
import { SignIn } from "./components/pages/SignIn";
import { SignUp } from "./components/pages/SignUp";
import Profile from "./components/pages/User";
import useToken from "./hooks/useToken";
import { Layout, AuthLayout } from "./components/pages/layout";

const router = (setters: { setToken: Dispatch<string>, currentToken: MutableRefObject<string> }) => createBrowserRouter([
  { path: '',
    loader: rootLoader(setters),
    id: 'root',
    HydrateFallback: LoadingScreen,
    children: [{
    path: "/auth",
    element: <AuthLayout />, // <-- renders children
    HydrateFallback: LoadingScreen,
    children: [
      { path: "signin", element: <SignIn /> },
      { path: "signup", element: <SignUp /> },
      { path: "", element: <SignIn /> }
    ]
  },
  {
    path: "/",
    element: <Layout />,
    
    children: [
      { path: "profile", element: <Profile /> },
      { path: "", element: <Home /> }
    ]
  }]
  },
  {
    path: "*",
    element: <div>Page not found</div>
  }
]);

const AppRouter = () => {
  const { token, setToken } = useToken()

  const myRouter = useMemo(() => {
    return router({ setToken, currentToken: token! })
  }, [setToken, token])

  return (
  <UserProvider>
    <Suspense fallback={<LoadingScreen />}>
      <RouterProvider router={myRouter} />
    </Suspense>
  </UserProvider>
)};

export default memo(AppRouter);
