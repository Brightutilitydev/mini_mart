import { useState } from "react"
import "./index.scss"
import { signUpUser } from "../../../composables/api"


export function SignUp() {

  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [otherNames, setOtherNames] = useState("")

  const [address, setAddress] = useState("")

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [phone, setPhone] = useState("")



  // TODO: change the types when you figure out something acceptable
  const changeFirstName = (e) => setFirstName(e.target!.value);
  const changeLastName = (e) => setLastName(e.target!.value);
  const changeOtherNames = (e) => setOtherNames(e.target!.value);
  const changeAddress = (e) => setAddress(e.target!.value);
  const changeEmail = (e) => setEmail(e.target!.value);
  const changePassword = (e) => setPassword(e.target!.value);
  const changePhone = (e) => setPhone(e.target!.value);


  const submitForm = async (e) => {
    e.preventDefault();
    signUpUser({
      first_name: firstName.trim(),
      last_name: lastName.trim(),
      whatsapp_number: phone.trim(),
      email: email.trim(),
      password: password.trim(),
      address: address.trim()
    })
    console.log(e);


  }




  return <>


    <form onSubmit={submitForm} id="signup-form" className="signup">
      <h1 className="signup-title">Sign Up Form</h1>

      <p>Required fields are followed by *</p>

      <p>Already a user? <a href="/signin">Click here to log in!</a></p>

      <section className="signup-section">

        <h2 className="signup-subtitle">Contact Information</h2>


        <div className="cinput-field">
          <label htmlFor="">Name(s):</label>
          <input onChange={changeFirstName} value={firstName} type="text" name="first-name" placeholder="First Name *" required minLength={2} />
          <input onChange={changeLastName} value={lastName} type="text" name="last-name" placeholder="Last Name *" required minLength={2} />
          <input onChange={changeOtherNames} value={otherNames} type="text" name="other-names" placeholder="Other Names" />
        </div>




        <div className="cinput-field">
          <label htmlFor="">Address *</label>
          <input onChange={changeAddress} value={address} type="text" name="adress" placeholder="18 Ifelodun Street, Abusoro, Akure." required />
        </div>



        <div className="cinput-field">
          <label htmlFor="">Phone Number *</label>
          <input onChange={changePhone} value={phone} type="text" name="phone-number" placeholder="08001797400" inputMode="numeric" maxLength={11} required />
          <small>Enter your whatsapp phone number</small>
        </div>
      </section>




      <section className="signup-section">

        <h2 className="signup-subtitle">Accout Information</h2>

        <div className="cinput-field">
          <label htmlFor="">Email *</label>
          <input onChange={changeEmail} value={email} type="email" name="email" placeholder="kincaid@gmail.com" required />
        </div>

        <div className="cinput-field">
          <label htmlFor="">Password *</label>
          <input onChange={changePassword} value={password} type="password" name="adress" placeholder="Password" required minLength={6} />
          <small>Password must be minimum of 6 letters</small>

        </div>
      </section>


      <input className="cinput-submit" id="signup-submit" type="submit" value="Sign Up" data-btn />
    </form>


  </>



}
