import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import UpdatePostModal from "../components/UpdatePostModal";

function ProfilePage() {
  const navigate = useNavigate();
  const [posts, setPosts] = useState([]);
  const [user, setUser] = useState({ name: "", username: "", bio: "", id: 1 });
  const [error, setError] = useState(false);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedPost, setSelectedPost] = useState(null);

  // Determine backend URL based on environment
  const isLocalhost =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1";
  const backendUrl = isLocalhost
    ? "http://localhost:8000"
    : "https://team-yapper-backend-api-1.onrender.com";

  // Random profile picture URL from picsum.photos
  const randomProfilePic = `https://picsum.photos/80?random=${Math.floor(Math.random() * 1000)}`;

  useEffect(() => {
  const fetchUserAndPosts = async () => {
    try {
      const userRes = await fetch(`${backendUrl}/user`, { credentials: "include" });
      if (!userRes.ok) throw new Error("Not logged in");

      const userInfo = await userRes.json();
      setUser({
        id: userInfo.id,
        username: userInfo.email,
        name: userInfo.email.split("@")[0],
        bio: userInfo.bio || "",
      });

      const postsRes = await fetch(`${backendUrl}/user/${userInfo.id}/posts`);
      const postData = await postsRes.json();
      setPosts(postData.posts || []);
    } catch (err) {
      console.error("Fetch error:", err);
      setError(true);
    }
  };

  fetchUserAndPosts();
}, [backendUrl]);

  const handlePostUpdated = (updatedPost) => {
  setPosts((prevPosts) =>
    prevPosts.map((post) =>
      post.id === updatedPost.id ? updatedPost : post
    )
  );
};

const handlePostDeleted = (deletedPostId) => {
  setPosts((prevPosts) =>
    prevPosts.filter((post) => post.id !== deletedPostId)
  );
};

const closeModal = () => {
  setIsModalOpen(false);
  setSelectedPost(null);
};

  return (
    <div className="min-h-screen bg-gray-900 px-6 py-12 flex justify-center relative">
      {/* Back Button */}
      <button
        onClick={() => navigate("/")}
        className="absolute top-6 left-6 flex items-center space-x-2 px-3 py-2 bg-gray-700 text-white rounded hover:bg-gray-600 transition"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-5 w-5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M9.707 14.707a1 1 0 01-1.414 0L3.586 10l4.707-4.707a1 1 0 011.414 1.414L6.414 10l3.293 3.293a1 1 0 010 1.414z"
            clipRule="evenodd"
          />
        </svg>
        <span>Home</span>
      </button>
      {/* Logout Button*/}
      <button
        onClick={() => {
          window.location.href = `${backendUrl}/logout`;
        }}
        className="absolute top-6 right-6 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
      >
        Logout
      </button>

      <div className="w-full max-w-4xl flex flex-col items-center space-y-8">
        {/* Profile Box */}
        <div className="w-full bg-gray-800 p-8 rounded-xl border border-gray-700 shadow-2xl text-center">
          <div className="flex flex-col items-center space-y-4">
            {/* Random profile picture */}
            <img
              src={randomProfilePic}
              alt="Profile"
              className="w-24 h-24 rounded-full object-cover mx-auto"
            />
            <div>
              <div className="text-xl font-semibold text-white">
                {user.name}
              </div>
              <div className="text-sm text-gray-300">{user.username}</div>
            </div>
          </div>
          <p className="mt-4 text-gray-300 text-sm">{user.bio}</p>
        </div>

        {/* Posts Section */}
        <div className="w-full flex-1 flex flex-col space-y-4">
          <h2 className="text-2xl font-semibold mb-4 text-white w-full">
            Your posts
          </h2>

          {error && (
            <div className="text-sm text-red-500 text-center py-20 w-full">
              Failed to load posts.
            </div>
          )}

          {!error && posts.length === 0 && (
            <div className="flex-1 text-sm text-gray-300 text-center py-20 w-full">
              No posts to display.
            </div>
          )}

          {!error && posts.length > 0 && (
            <ul className="space-y-4 w-full">
              {posts.map((post) => (
                <li
                  key={post.id}
                  className="bg-gray-800 p-4 rounded border border-gray-700 flex justify-between items-start w-full"
                >
                  <p className="text-gray-300">{post.content}</p>
                  <button
                    onClick={() => {
                      setSelectedPost(post);
                      setIsModalOpen(true);
                    }}
                    className="ml-4 px-3 py-1 bg-indigo-700 text-white text-sm rounded hover:bg-indigo-500 transition"
                  >
                    Update
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
      <UpdatePostModal
        isOpen={isModalOpen}
        post={selectedPost}
        backendUrl={backendUrl}
        onClose={closeModal}
        onPostUpdated={handlePostUpdated}
        onPostDeleted={handlePostDeleted}
      />
    </div>
  );
}

export default ProfilePage;
