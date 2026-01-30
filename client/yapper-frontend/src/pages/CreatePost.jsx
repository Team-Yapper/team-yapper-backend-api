import { useState } from 'react'

function CreatePost({ onClose }) {
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!content.trim()) {
      setError('Post content cannot be empty')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/posts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: content.trim() }),
        credentials: 'include'
      })

      if (!response.ok) {
        if (response.status === 401) {
          setError('You must be logged in to create a post')
        } else if (response.status === 404) {
          setError('User not found')
        } else {
          setError('Failed to create post')
        }
        return
      }

      const newPost = await response.json()
      console.log('Post created:', newPost)
      setContent('')
      if (onClose) {
        onClose()
      }
    } catch (err) {
      setError(err.message || 'An error occurred while creating the post')
      console.error('Error creating post:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className='text-lg font-bold mb-4 text-black'>What do you want to yap about?</h2>
      <form onSubmit={handleSubmit} className='space-y-3'>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Share your thoughts..."
          rows="4"
          disabled={loading}
          className='w-full p-2 border border-gray-300 rounded resize-none text-black h-[150px] sm:h-[200px] md:h-[450px]'
        />
        {error && <p className='text-red-500 text-sm'>{error}</p>}
        <div className='flex gap-2 justify-end'>
          <button 
            type="submit" 
            disabled={loading}
            className='px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400'
          >
            {loading ? 'Creating...' : 'Post'}
          </button>
          {onClose && (
            <button 
              type="button" 
              onClick={onClose}
              className='px-4 py-2 bg-gray-400 text-white rounded hover:bg-gray-500'
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  )
}

export default CreatePost
