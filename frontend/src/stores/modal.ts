import { atom } from "nanostores";

const MODAL_COMPONENT_NAMES = ["search", "liked_products", "cart", "change_password"] as const
type ModalComponent = typeof MODAL_COMPONENT_NAMES[number]

export const $modalIsActive = atom(false);
export const $modalComponent = atom("cart" as ModalComponent)
const modalIsActiveClass = "modal-is-active"

export const changeModalComponent = (component: ModalComponent) => $modalComponent.set(component)
export const openModalComponent = (component: ModalComponent) => {
    changeModalComponent(component);
    activateModal();
}

$modalIsActive.subscribe(modalIsActive => {
    const isInBrowser = "document" in globalThis;
    if (!isInBrowser) return

    const bodyElement = globalThis.document.body
    
    if (modalIsActive) {
        bodyElement.classList.add(modalIsActiveClass)
    } else {
        bodyElement.classList.remove(modalIsActiveClass)
    }

})


export const activateModal = () => { $modalIsActive.set(true) }
export const inactivateModal = () => { $modalIsActive.set(false) }
