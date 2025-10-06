import React from "react";
import "./LoadingScreen.scss";

const LoadingScreen = () => (
  <div className="loading-screen">
    <div className="loading-bg" />
    <div className="loading-content">
      <img src={"/dummies/logo.png"} alt="Mini Mart Logo" className="loading-logo" />
      <p className="loading-tip">
        You can search for products and manage your cart easily!
      </p>
    </div>
  </div>
);

export default React.memo(LoadingScreen);
