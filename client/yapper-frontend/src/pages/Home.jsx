import React, { useEffect, useState } from "react";
import CreatePost from "./CreatePost";
import Navbar from "../components/NavBar.jsx";
import ErrorPage from "../pages/ErrorPage";

function Home() {
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState(false);
  const [showCreatePost, setShowCreatePost] = useState(false);

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
    <>
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
                <p className="italic text-gray-700 mt-2 flex justify-end">
                  {post.user_email || "Unknown"}
                </p>
              </div>
            ))
          )}
        </div>
      </div>

      {/* V FOR CREATE POST FUNCTIONALITY V */}
      {/* Fixed position + button */}
      {!showCreatePost && (
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
              <CreatePost onClose={() => setShowCreatePost(false)} />
            </div>
          </div>
        </div>
      )}
      {/* ^ FOR CREATE POST FUNCTIONALITY ^ */}
    </>
  );
}
export default Home;
