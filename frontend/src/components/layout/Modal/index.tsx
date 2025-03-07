import "./index.scss"
import Cart from "../Cart"
import LikedProducts from "../LikedProducts"
import SearchBar from "../SearchBar"
import { useStore } from "@nanostores/react"
import { $modalComponent } from "../../../stores/modal"
import ChangePassword from "../ChangePassword"

export default function Modal() {

    const modalComponent = useStore($modalComponent)

    // Make the modal close when the target of the click event is the modal itself!
    return <>
        <section className="c-modal" id="modal" aria-hidden="false">
            {/* { modalComponent === "cart" && <Cart /> } */}
            {/* { modalComponent === "cart" && <Cart /> } */}
            {
                modalComponent === "cart" ?
                    <Cart /> :
                    (modalComponent === "liked_products" ?
                        <LikedProducts /> :
                        (modalComponent === "search" ?
                            <SearchBar /> :
                            <ChangePassword />
                        )
                    )
            }
            {/* <LikedProducts /> */}
            {/* <SearchBar /> */}
        </section>


    </>
}