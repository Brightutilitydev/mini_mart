import "./index.scss";
import { useStore } from "@nanostores/react";
import { $cart } from "../../../stores/cart";
import { $modalIsActive, openModalComponent } from "../../../stores/modal";
import { $loggedIn } from "../../../stores/user";

export default function Header() {
    const loggedIn = useStore($loggedIn)
    const modalIsActive = useStore($modalIsActive)
    const cart = useStore($cart)

    return <header className="header" aria-hidden={modalIsActive} inert={modalIsActive}>
        <div className="header-logo">
            <a href="/">
                <img src="/dummies/logo.png" alt="Logo" className="header-logo-img" />
            </a>
        </div>
        <nav className="header-nav">
            <ul className="header-nav-list">
                <li className="header-nav-li">
                    <button data-btn className="header-nav-search-btn"
                        onClick={openModalComponent.bind(null, "search")}
                    >
                        <span className="sr-only">Search</span>

                        <svg viewBox="0 0 24 24">
                            <use href="#icon-search"></use>
                        </svg>
                    </button>
                </li>
                <li className="header-nav-li">
                    <button data-btn className="header-nav-liked-products"
                        onClick={openModalComponent.bind(null, "liked_products")}
                    >
                        <span className="sr-only">Liked Products</span>
                        <svg viewBox="0 0 24 24">
                            <use href="#icon-like-outline"></use>
                        </svg>
                    </button>
                </li>
                
                {!loggedIn && <li className="header-nav-li">
                    <a href="/auth/signin" data-btn className="header-nav-sign-in">Log In</a>
                </li>}
            </ul>

            <button data-btn className="header-nav-cart"
                onClick={openModalComponent.bind(null, "cart")}
            >
                <svg viewBox="0 0 24 24">
                    <use href="#icon-cart"></use>
                </svg>
                <span>Cart ({cart.length})</span>

            </button>

        </nav>
    </header>


}