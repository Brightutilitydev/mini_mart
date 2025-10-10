// import { logInUser } from "../../../composables/api";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { loginUser } from "../../../lib/requestUtils";
import { useUserUpdate } from "../../../stores/user";
import "./index.scss";
import { useNavigate } from "react-router";
import useToken from "../../../hooks/useToken";

const SignInSchema = z.object({
  email: z.string().email({ message: "Invalid email address" }),
  password: z.string().min(6, "Password must be at least 6 characters")
});

export type SignInFormType = z.infer<typeof SignInSchema>;

export function SignIn() {
  const { setToken } = useToken()
  const navigate = useNavigate()
  const { login } = useUserUpdate();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
    reset
  } = useForm<SignInFormType>({
    resolver: zodResolver(SignInSchema),
    defaultValues: { email: "", password: "" }
  });

  const onSubmit = async (data: SignInFormType) => {
    try {
      const { access_token, user } = (await loginUser(data.email.trim(), data.password.trim()))!;
      setToken(access_token); // Store in context/nanostore
      login(user);            // Store user object
      reset();
      navigate('/')
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (err: any) {
      setError("email", { type: "manual", message: err?.message || "Login failed" });
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} id="signin-form" className="signin">
      <h1 className="signin-title">Log In</h1>
      <p>New here? <a href="/auth/signup">Click Here to Sign Up</a></p>
      <section className="signin-section">
        <div className="cinput-field">
          <label htmlFor="email">Email</label>
          <input {...register("email")}
            type="email"
            name="email"
            placeholder="kincaid@gmail.com"
            required
            autoComplete="email"
            disabled={isSubmitting}
          />
          {errors.email && <span className="form-error">{errors.email.message}</span>}
        </div>
        <div className="cinput-field">
          <label htmlFor="password">Password</label>
          <input {...register("password")}
            type="password"
            name="password"
            placeholder="Password"
            required
            minLength={6}
            autoComplete="current-password"
            disabled={isSubmitting}
          />
          {errors.password && <span className="form-error">{errors.password.message}</span>}
        </div>
      </section>
      <input className="cinput-submit" id="signin-submit" type="submit" value={isSubmitting ? "Signing In..." : "Sign In"} data-btn disabled={isSubmitting} />
    </form>
  );
}
