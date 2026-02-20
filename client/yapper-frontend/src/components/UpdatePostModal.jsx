import { useEffect, useState } from "react";

function UpdatePostModal({
  isOpen,
  post,
  backendUrl,
  onClose,
  onPostUpdated,
  onPostDeleted,
}) {
  const [editedContent, setEditedContent] = useState("");

  // When modal opens, preload content
  useEffect(() => {
    if (post) {
      setEditedContent(post.content);
    }
  }, [post]);

  // ESC key closes modal
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === "Escape") onClose();
    };

    window.addEventListener("keydown", handleEsc);
    return () => window.removeEventListener("keydown", handleEsc);
  }, [onClose]);

  if (!isOpen || !post) return null;

  const handleUpdate = async () => {
    try {
      const res = await fetch(`${backendUrl}/posts/${post.id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ content: editedContent }),
      });

      if (!res.ok) throw new Error("Update failed");

      const updatedPost = await res.json();
      onPostUpdated(updatedPost);
      onClose();
    } catch (err) {
      console.error("Update error:", err);
    }
  };

  const handleDelete = async () => {
    try {
      const res = await fetch(`${backendUrl}/posts/${post.id}`, {
        method: "DELETE",
        credentials: "include",
      });

      if (!res.ok) throw new Error("Delete failed");

      onPostDeleted(post.id);
      onClose();
    } catch (err) {
      console.error("Delete error:", err);
    }
  };

  return (
    <div
      className="fixed inset-0 backdrop-blur-sm bg-black/20 flex justify-center items-center z-50"
      onClick={onClose}
      data-testid="backdrop"
    >
      <div
        className="bg-gray-800 p-6 rounded-lg w-96 border border-gray-700"
        onClick={(e) => e.stopPropagation()}
      >
        <h3 className="text-white text-lg mb-4">Edit Post</h3>

        <textarea
          value={editedContent}
          onChange={(e) => setEditedContent(e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white border border-gray-600 mb-4"
          rows="4"
        />

        <div className="flex justify-between">
          <button
            onClick={handleUpdate}
            className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-500"
          >
            Save
          </button>

          <button
            onClick={handleDelete}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-500"
          >
            Delete
          </button>

          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-500"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export default UpdatePostModal;
