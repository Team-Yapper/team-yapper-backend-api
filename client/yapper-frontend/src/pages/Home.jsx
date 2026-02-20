import React, { useEffect, useState } from "react";
import CreatePost from "./CreatePost";
import Navbar from "../components/Navbar.jsx";
import ErrorPage from "../pages/ErrorPage";

function Home() {
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState(false);
  const [showCreatePost, setShowCreatePost] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const fetchPosts = () => {
  // fetch("http://localhost:8000/posts")
  fetch("https://team-yapper-backend-api-1.onrender.com/posts")
    .then((res) => {
      if (!res.ok) throw new Error("Fetch failed");
      return res.json();
    })
    .then((data) => setPosts(data))
    .catch(() => setError(true));
  };

  useEffect(() => {
    // Check if user is logged in
    // fetch("http://localhost:8000/user", {
    fetch("https://team-yapper-backend-api-1.onrender.com/user", {
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

    // Fetch posts
    fetchPosts()
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
    <>
      <div className="min-h-screen bg-gray-900 pb-20">
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
                <h2 className="font-semibold text-lg text-gray-100 group-hover:text-blue-400 transition-colors">
                  {post.content}
                </h2>
                <p className="italic text-sm text-gray-500 mt-3 flex justify-end group-hover:text-gray-400 transition-colors">
                  {post.user_email || "Unknown"}
                </p>
                <p className="italic text-xs text-gray-500 mt-3 flex justify-end group-hover:text-gray-400 transition-colors">
                  {post.created_at || "Unknown"}
                </p>
              </div>
            ))
          )}
        </div>

        {/* V FOR CREATE POST FUNCTIONALITY V */}
        {/* Fixed position + button - only show if logged in */}
        {!showCreatePost && isLoggedIn && (
          <button
            type="button"
            onClick={() => setShowCreatePost(true)}
            className="fixed bottom-8 right-8 w-14 h-14 rounded-lg border border-transparent font-medium bg-gray-900 text-white cursor-pointer transition-colors duration-250 hover:border-blue-500 flex items-center justify-center text-2xl shadow-lg leading-none pb-1"
          >
            +
          </button>
        )}

        {/* Modal overlay */}
        {showCreatePost && (
          <div className="fixed inset-0 pointer-events-none">
            {/* Modal window - bottom right */}
            <div className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 md:bottom-24 md:right-8 bg-white rounded-lg shadow-xl w-[calc(100%-2rem)] sm:w-[90%] md:w-[500px] h-[90vh] sm:h-[90vh] md:h-[600px] pointer-events-auto">
              {/* Close button */}
              <button
                onClick={() => setShowCreatePost(false)}
                className="absolute top-2 right-2 px-3 py-2 rounded-lg border border-transparent font-medium bg-gray-900 text-white cursor-pointer transition-colors duration-250 hover:border-blue-500"
              >
                ✕
              </button>
              {/* CreatePost form inside modal */}
              <div className="p-6">
                <CreatePost 
                  onClose={() => setShowCreatePost(false)} 
                  onCreate={() => {
                    fetchPosts()
                    setShowCreatePost(false);
                  }}
                />
              </div>
            </div>
          </div>
        )}
        {/* ^ FOR CREATE POST FUNCTIONALITY ^ */}
      </div>
    </>
  );
}
export default Home;
