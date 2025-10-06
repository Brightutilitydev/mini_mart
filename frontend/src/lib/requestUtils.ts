/* eslint-disable @typescript-eslint/no-explicit-any */
import { AxiosError } from "axios";
import { axiosConfig } from "./axiosConfig";
import CustomAppError from "./customAppError";

// Types
export interface RegisteringUser {
  address: string;
  email: string;
  first_name: string;
  other_names: string;
  last_name: string;
  password: string;
  whatsapp_number: string;
}

export interface LogInCredentials {
  email: string;
  password: string;
}

export interface Product {
  category_id: string;
  created_at: string;
  description: string;
  id: string;
  name: string;
  price: number;
  stock: number;
  updated_at: string;
}

export interface User {
  address: string;
  created_at: string;
  email: string;
  first_name: string;
  id: string;
  is_admin: boolean;
  last_name: string;
  password: string;
  phone_number: string;
  updated_at: string;
  whatsapp_number: string;
}

const throwError = (error: AxiosError) => {
  throw new CustomAppError(error);
};

const checkError = (err: AxiosError) => {
  if (err.code !== "ERR_NETWORK") {
    throwError(err);
  } else {
    throw err;
  }
};

export async function getAccessToken(): Promise<{ access_token: string } | undefined> {
  try {
    const response = await axiosConfig.post("/refresh", {}, {
      withCredentials: true
    });
    return response.data;
  } catch (error: any) {
    checkError(error);
  }
}

export async function loginUser(email: string, password: string): Promise<{access_token: string, user: User} | undefined> {
  try {
    const response = await axiosConfig.post("/login", { email, password }, {
      withCredentials: true
    });
    return response.data;
  } catch (error: any) {
    checkError(error);
  }
}

export async function signUpUser(new_user: RegisteringUser): Promise<User | undefined> {
  try {
    const response = await axiosConfig.post("/register", new_user, {
      withCredentials: true
    });
    return response.data;
  } catch (error: any) {
    checkError(error);
  }
}

export async function getProfile(): Promise<User | undefined> {
  try {
    const response = await axiosConfig.get("/profile", {
      withCredentials: true
    });
    return response.data;
  } catch (error: any) {
    checkError(error);
  }
}

export async function getProducts(): Promise<Product[] | undefined> {
  try {
    const response = await axiosConfig.get("/products", {
      withCredentials: true
    });
    return response.data;
  } catch (error: any) {
    checkError(error);
  }
}
