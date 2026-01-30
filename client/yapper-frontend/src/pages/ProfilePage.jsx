import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

function ProfilePage() {
  const navigate = useNavigate()
  const [posts, setPosts] = useState([])
  const [user, setUser] = useState({ name: '', username: '', bio: '', id: 1 })
  const [error, setError] = useState(false)

  const randomProfilePic = `https://picsum.photos/80?random=${Math.floor(Math.random() * 1000)}`

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/user/${user.id}/posts`)
      .then(async (res) => {
        if (!res.ok) throw new Error(`Fetch failed with status ${res.status}`)
        return res.json()
      })
      .then((data) => {
        setPosts(data.posts || [])

        if (data.email) {
          setUser((prev) => ({
            ...prev,
            username: data.email,
            name: data.email.split('@')[0],
          }))
        }
      })
      .catch((err) => {
        console.error("Fetch error:", err)
        setError(true)
      })
  }, [user.id])

  return (
    <div className="min-h-screen bg-gray-900 flex justify-center">
      <div className="w-full max-w-4xl flex flex-col h-screen px-6 py-12">
        {/* Profile Box */}
        <div className="w-full bg-gray-800 p-8 rounded-xl border border-gray-700 shadow-2xl text-center mb-8">
          <div className="flex flex-col items-center space-y-4">
            <img
              src={randomProfilePic}
              alt="Profile"
              className="w-24 h-24 rounded-full object-cover mx-auto"
            />
            <div>
              <div className="text-xl font-semibold text-white">{user.name}</div>
              <div className="text-sm text-gray-300">{user.username}</div>
            </div>
          </div>
          <p className="mt-4 text-gray-300 text-sm">{user.bio}</p>
        </div>

        {/* Posts Section */}
        <div className="flex-1 flex flex-col w-full">
          <h2 className="text-2xl font-semibold mb-4 text-white">Your posts</h2>

          <div className="flex-1 flex flex-col justify-center">
            {error && (
              <div className="text-sm text-red-500 text-center">
                Failed to load posts.
              </div>
            )}

            {!error && posts.length === 0 && (
              <div className="text-sm text-white text-center">
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
                      onClick={() => navigate(`/update/${post.id}`)}
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
      </div>
    </div>
  )
}

export default ProfilePage
