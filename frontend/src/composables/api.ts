const BASE_NAME = "http://127.0.0.1:5000"


const createApiLink = (string: string) => `${BASE_NAME}/${string}`

export const fetchData = async (endpoint: string) => {
  const res = await fetch(`${BASE_NAME}/${endpoint}`)
  return res
}


// Users

interface RegisteringUser {
  address: string
  email: string
  first_name: string
  last_name: string
  password: string
  whatsapp_number: string
}

export const signUpUser = async (new_user: RegisteringUser) => {
  const request = new Request(createApiLink("register"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(new_user)
  })

  const response = await fetch(request)
  const data = await response.json()
  console.log(data)
}

interface LogInCredentials {
  email: string
  password: string
}
export const logInUser = async (user: LogInCredentials) => {

  const request = new Request(createApiLink("login"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(user)
  })

  const response = await fetch(request)
  const data = await response.json()
  console.log(data)
}






// cookies
const setRefreshToken = (token: string) => {

  

  
}




// types

export interface Product {
  category_id: string
  created_at: string
  description: string
  id: string
  name: string
  price: number
  stock: number
  updated_at: string
}

export interface User {
  address: string
  created_at: string
  email: string
  first_name: string
  id: string
  is_admin: boolean
  last_name: string
  password: string
  phone_number: string
  updated_at: string
  whatsapp_number: string
}
