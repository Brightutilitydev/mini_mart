import { logInUser } from "../../../composables/api";
import "./index.scss"
import { useState } from "react"


export function SignIn() {

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const changeEmail = (e) => setEmail(e.target!.value);
  const changePassword = (e) => setPassword(e.target!.value);

  const submitForm = (e) => {
    e.preventDefault()
    logInUser({
      email: email.trim(),
      password: password.trim(),
    })
  } 

  
  return <>


    <form onSubmit={submitForm} id="signin-form" className="signin">
      <h1 className="signin-title">Log In</h1>

      <p>New here? <a href="/signup">Click Here to Sign Up</a></p>


      <section className="signin-section">


        <div className="cinput-field">
          <label htmlFor="">Email</label>
          <input value={email} onChange={changeEmail} type="email" name="email" placeholder="kincaid@gmail.com" required />
        </div>

        <div className="cinput-field">
          <label htmlFor="">Password</label>
          {/* TODO: what is the password minlength? */}
          <input value={password} onChange={changePassword} type="password" name="adress" placeholder="Password" required minLength={6} />

        </div>
      </section>


      <input className="cinput-submit" id="signin-submit" type="submit" value="Sign In" data-btn />
    </form>


  </>



}
