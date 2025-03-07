import { inactivateModal } from "../../../stores/modal"
import "./index.scss"



export default function ChangePassword() {

    return <>

        <section className="change-password sgrid">
            <button title="Close" className="change-password-close" data-btn onClick={inactivateModal}>Close</button>
            <h2 className="change-password-title">Change Password</h2>
            <div className="change-password-main">
                <form className="change-password-form">
                    <div className="ch-input-field">
                        <input className="change-password-input"
                            type="password"
                            name="change-password-original-password"
                            placeholder="Original Password" />
                    </div>

                    <div className="ch-input-field">
                        <input className="change-password-input"
                            type="password"
                            name="change-password-new-password"
                            placeholder="New Password" />

                        <input className="change-password-input"
                            type="password"
                            name="change-password-confirm-new-password"
                            placeholder="Confirm New Password" />

                    </div>
                    <input data-btn className="change-password-button" value="Change Password" type="submit" />

                </form>

            </div>
        </section>
    </>

}