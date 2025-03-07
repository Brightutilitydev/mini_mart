import { openModalComponent } from "../../../stores/modal"
import "./index.scss"

export default function User() {


    return <>
        <section className="user">
            <h1 className="user-title">👋 Hi! AstridEmma0231</h1>

            <dl className="user-list">
                <div className="user-item">
                    <dt className="user-dt">Name</dt>
                    <dd className="user-dd">Imra Vardeen</dd>
                </div>

                <div className="user-item">
                    <dt className="user-dt">Email</dt>
                    <dd className="user-dd">imradeen@gmail.com</dd>
                </div>

                <div className="user-item">
                    <dt className="user-dt">Phone</dt>
                    <dd className="user-dd">0810 856 7504</dd>
                </div>

                <div className="user-item">
                    <dt className="user-dt">Adress</dt>
                    <dd className="user-dd">7 Binbirest, Unilorin Quaters, Namibia</dd>
                </div>

            </dl>

            <button data-btn className="user-btn"
            onClick={openModalComponent.bind(null, "change_password")}
            >Change Password</button>


        </section>

    </>


} 