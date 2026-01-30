// components/Navbar.jsx
import React from "react";
import { useNavigate } from "react-router-dom";
import Yapper_logo from "../images/Yapper_logo.png";
import profile_pic from "../images/profile_pic.png"

const Navbar = () => {
    const navigate = useNavigate()
    return (
        <nav className="flex justify-between items-center px-6 py-4 bg-gray-100 shadow">
        <div>
            <img src={Yapper_logo} alt="Logo" className="h-10 w-10 ml-2" onClick={() => navigate("/")} />
        </div>

        <div>
            <img
            src={profile_pic}
            alt="Profile"
            className="h-10 w-10 rounded-full object-cover border-2 border-gray-300 mr-2"
            onClick={() => navigate("/profile")}
            />
        </div>
        </nav>
    );
};

export default Navbar;
