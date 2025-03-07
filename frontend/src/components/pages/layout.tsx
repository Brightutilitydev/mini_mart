import { useStore } from '@nanostores/react'
import { $router } from '../../stores/router'
import Home from './Home'
import Product from './Product'
import { SignUp } from './SignUp'
import User from './User'
import { SignIn } from './SignIn'

export const Layout = () => {
    const page = useStore($router)


    if (!page) {
        return <></>
    } else if (page.route === "home") {
        return <Home />
    } else if (page.route === "product") {
        return <Product />
    } else if (page.route === "signin") {
        return <SignIn />
    } else if (page.route === "signup") {
        return <SignUp />
    } else if (page.route === "user") {
        return <User />
    } else if (page.route === "search") {
        return <></>
    }

}