import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { signUpUser } from "../../../lib/requestUtils";
import { useUserUpdate } from "../../../stores/user";
import { useMutation } from "@tanstack/react-query";
import "./index.scss";

const SignUpSchema = z.object({
  first_name: z.string().min(2, "First name must be at least 2 characters"),
  last_name: z.string().min(2, "Last name must be at least 2 characters"),
  other_names: z.string().optional(),
  address: z.string().min(1, "Address is required"),
  whatsapp_number: z.string().min(10, "Phone number must be at least 10 digits"),
  email: z.string().email({ message: "Invalid email address" }),
  password: z.string().min(6, "Password must be at least 6 characters")
});

export type SignUpFormType = z.infer<typeof SignUpSchema>;

export function SignUp() {
  const { login } = useUserUpdate();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
    reset
  } = useForm<SignUpFormType>({
    resolver: zodResolver(SignUpSchema),
    defaultValues: {
      first_name: "",
      last_name: "",
      other_names: "",
      address: "",
      whatsapp_number: "",
      email: "",
      password: ""
    }
  });

  const mutation = useMutation({
    mutationFn: async (data: SignUpFormType) => {
      return await signUpUser({
        first_name: data.first_name.trim(),
        last_name: data.last_name.trim(),
        other_names: data.other_names?.trim() || "",
        address: data.address.trim(),
        whatsapp_number: data.whatsapp_number.trim(),
        email: data.email.trim(),
        password: data.password.trim()
      });
    },
    onSuccess: (user) => {
      if (user && user.id) {
        login(user);
        reset();
        // Optionally redirect or show success
      } else {
        setError("email", { type: "manual", message: "Signup failed" });
      }
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onError: (err: any) => {
      setError("email", { type: "manual", message: err?.message || "Signup failed" });
    }
  });

  const onSubmit = (data: SignUpFormType) => {
    mutation.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} id="signup-form" className="signup">
      <h1 className="signup-title">Sign Up Form</h1>
      <p>Required fields are followed by *</p>
      <p>Already a user? <a href="/signin">Click here to log in!</a></p>
      <section className="signup-section">
        <h2 className="signup-subtitle">Contact Information</h2>
        <div className="cinput-field">
          <label htmlFor="first-name">Name(s):</label>
          <input {...register("first_name")}
            type="text"
            name="first-name"
            placeholder="First Name *"
            required
            minLength={2}
            disabled={isSubmitting}
          />
          {errors.first_name && <span className="form-error">{errors.first_name.message}</span>}
          <input {...register("last_name")}
            type="text"
            name="last-name"
            placeholder="Last Name *"
            required
            minLength={2}
            disabled={isSubmitting}
          />
          {errors.last_name && <span className="form-error">{errors.last_name.message}</span>}
          <input {...register("other_names")}
            type="text"
            name="other-names"
            placeholder="Other Names"
            disabled={isSubmitting}
          />
        </div>
        <div className="cinput-field">
          <label htmlFor="address">Address *</label>
          <input {...register("address")}
            type="text"
            name="address"
            placeholder="18 Ifelodun Street, Abusoro, Akure."
            required
            disabled={isSubmitting}
          />
          {errors.address && <span className="form-error">{errors.address.message}</span>}
        </div>
        <div className="cinput-field">
          <label htmlFor="phone-number">Phone Number *</label>
          <input {...register("whatsapp_number")}
            type="text"
            name="phone-number"
            placeholder="08001797400"
            inputMode="numeric"
            maxLength={11}
            required
            disabled={isSubmitting}
          />
          {errors.whatsapp_number && <span className="form-error">{errors.whatsapp_number.message}</span>}
          <small>Enter your whatsapp phone number</small>
        </div>
      </section>
      <section className="signup-section">
        <h2 className="signup-subtitle">Accout Information</h2>
        <div className="cinput-field">
          <label htmlFor="email">Email *</label>
          <input {...register("email")}
            type="email"
            name="email"
            placeholder="kincaid@gmail.com"
            required
            disabled={isSubmitting}
          />
          {errors.email && <span className="form-error">{errors.email.message}</span>}
        </div>
        <div className="cinput-field">
          <label htmlFor="password">Password *</label>
          <input {...register("password")}
            type="password"
            name="password"
            placeholder="Password"
            required
            minLength={6}
            disabled={isSubmitting}
          />
          {errors.password && <span className="form-error">{errors.password.message}</span>}
          <small>Password must be minimum of 6 letters</small>
        </div>
      </section>
  <input className="cinput-submit" id="signup-submit" type="submit" value={mutation.isPending ? "Signing Up..." : "Sign Up"} data-btn disabled={mutation.isPending} />
    </form>
  );
}
