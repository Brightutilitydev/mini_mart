import { createRouter } from '@nanostores/router'


export const $router = createRouter({
    
    home: "/",
    user: "/user",
    signin: "/signin",
    signup: "/signup",
    product: "/products/:product",
    search: "/search/:search-term"
    

})