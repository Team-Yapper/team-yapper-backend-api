// components/Navbar.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Yapper_logo from "../images/Yapper_logo.png";
import profile_pic from "../images/profile_pic.png";

const Navbar = () => {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Determine backend URL based on environment
  const isLocalhost =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1";
  const backendUrl = isLocalhost
    ? "http://localhost:8000"
    : "https://team-yapper-backend-api-1.onrender.com";

  useEffect(() => {
    // Check if user is logged in
    fetch(`${backendUrl}/user`, {
      credentials: "include",
    })
      .then((res) => {
        if (res.ok) {
          setIsLoggedIn(true);
        } else {
          setIsLoggedIn(false);
        }
      })
      .catch(() => setIsLoggedIn(false));
  }, [backendUrl]);

  return (
    <nav className="flex justify-between items-center px-6 py-4 bg-gray-100 shadow">
      <div>
        <img
          src={Yapper_logo}
          alt="Logo"
          className="h-10 w-10 ml-2 cursor-pointer"
          onClick={() => navigate("/")}
        />
      </div>

      <div>
        {isLoggedIn ? (
          <img
            src={profile_pic}
            alt="Profile"
            className="h-10 w-10 rounded-full object-cover border-2 border-gray-300 mr-2 cursor-pointer"
            onClick={() => navigate("/profile")}
          />
        ) : (
          <button
            onClick={() => (window.location.href = `${backendUrl}/login`)}
            className="px-4 py-2 rounded-lg border border-transparent font-medium bg-gray-900 text-white cursor-pointer transition-colors duration-250 hover:border-blue-500"
          >
            Login
          </button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
