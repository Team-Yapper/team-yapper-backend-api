import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar.jsx'
import ErrorPage from "../pages/ErrorPage";

function Home() {
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState(false);
  const navigate = useNavigate()

  useEffect(() => {
    fetch("http://127.0.0.1:8000/posts")
      .then((res) => {
        if (!res.ok) throw new Error("Fetch failed");
        return res.json();
      })
      .then((data) => setPosts(data))
      .catch(() => setError(true));
  }, []);

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <ErrorPage />
      </div>
    );
  }

  return (  
    <div className="min-h-screen bg-gray-900">
      <Navbar />
      <div className="max-w-3xl mx-auto mt-12 px-4 space-y-10">
        {posts.length === 0 ? (
          <p className="text-gray-500 text-center">No posts available.</p>
        ) : (
          posts.map((post) => (
            <div
              key={post.id}
              className="group p-6 bg-gray-800 rounded-xl border border-gray-700 shadow-sm transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-xl hover:border-blue-500/50 hover:bg-gray-750 cursor-pointer"
            >
              <h2 className="font-semibold text-lg text-gray-100 group-hover:text-blue-400 transition-colors">{post.content}</h2>
              <p className="italic text-sm text-gray-500 mt-3 flex justify-end group-hover:text-gray-400 transition-colors">{post.user_email || "Unknown"}</p>
            </div>
          ))
        )}
      </div>

        <div className="max-w-3xl mx-auto mt-6 px-4 flex justify-end">
        <button
          onClick={() => navigate("/create")}
          className="bg-blue-500 text-white px-4 py-2 rounded shadow hover:bg-blue-600 transition"
        >
          Create Post
        </button>
      </div>
    </div>
  )
}
export default Home