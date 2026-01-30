import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/NavBar.jsx'
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
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-3xl mx-auto mt-12 px-4 space-y-10">
        {posts.length === 0 ? (
          <p className="text-gray-500 text-center">No posts available.</p>
        ) : (
          posts.map((post) => (
            <div
              key={post.id}
              className="p-4 bg-white rounded-lg shadow hover:shadow-md transition"
            >
              <h2 className="font-bold text-lg">{post.content}</h2>
              <p className="italic text-gray-700 mt-2 flex justify-end">Author</p>
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