import type {  Dispatch, MutableRefObject } from "react";
import { getAccessToken, getProfile } from "../lib/requestUtils";
import { waitForInterceptor } from "../lib/tokenReady";
import { login, type User } from "../stores/user"; // or import $user if you use $user.set

export const rootLoader = (setters: { setToken: Dispatch<string>, currentToken: MutableRefObject<string> }) => async () => {
  const fetchAccessToken = async () => {
    try {
      const token = await getAccessToken()
      setters.setToken(token?.access_token as string)
      // eslint-disable-next-line no-unused-vars, @typescript-eslint/no-unused-vars
    } catch (error) {
      setters.setToken(' ')
    }
  }

  if (!setters.currentToken.current.trim()) {
    await fetchAccessToken()
    await waitForInterceptor()
  } else console.log('skipped token check')

  let userPromise: Promise<unknown> = Promise.resolve(null);
  try {
    userPromise = getProfile();
  } catch (error) {
    userPromise = Promise.reject(error);
  }

  return {
    user_promise: userPromise
  };
};

export const authLoader = (setters: { setToken: Dispatch<string>, currentToken: MutableRefObject<string> }) => async () => {
  const fetchAccessToken = async () => {
      try {
        const token = await getAccessToken()
        setters.setToken(token?.access_token as string)
        // eslint-disable-next-line no-unused-vars, @typescript-eslint/no-unused-vars
      } catch (error) {
        setters.setToken(' ')
      }
    }

    if (!setters.currentToken.current.trim()) {
      await fetchAccessToken()
      await waitForInterceptor()
    } else console.log('skipped token check')


  let userPromise: Promise<unknown> = Promise.resolve(null);
  try {
    userPromise = getProfile();
    userPromise.then((user) => {
      if (user) {
        login(user as User);
      }
    })
  } catch (error) {
    userPromise = Promise.reject(error);
  }

  return { user_promise: userPromise };
}
