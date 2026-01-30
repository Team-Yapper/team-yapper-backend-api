import { useState } from 'react'
import CreatePost from './CreatePost'

function Home() {
  const [showCreatePost, setShowCreatePost] = useState(false)

  return (  
    <div>   
        <h2 className='text-gray-700'>Home Page</h2>
        <p>Welcome to the Yapper home page!</p>
        
        {/* V FOR CREATE POST FUNCTIONALITY V */}
        {/* Fixed position + button */}
        {!showCreatePost && (
          <button 
            type="button" 
            onClick={() => setShowCreatePost(true)}
            className='fixed bottom-8 right-8 w-14 h-14 bg-blue-500 text-white text-2xl rounded-full shadow-lg hover:bg-blue-600 flex items-center justify-center'
          >
            +
          </button>
        )}

        {/* Modal overlay */}
        {showCreatePost && (
          <div className='fixed inset-0 pointer-events-none'>
            {/* Modal window - bottom right */}
            <div className='fixed bottom-4 right-4 sm:bottom-6 sm:right-6 md:bottom-24 md:right-8 bg-white rounded-lg shadow-xl w-[calc(100%-2rem)] sm:w-[90%] md:w-[500px] h-[90vh] sm:h-[90vh] md:h-[600px] pointer-events-auto'>
              {/* Close button */}
              <button
                onClick={() => setShowCreatePost(false)}
                className='absolute top-2 right-2 text-gray-500 hover:text-gray-700 text-2xl'
              >
                ✕
              </button>
              {/* CreatePost form inside modal */}
              <div className='p-6'>
                <CreatePost onClose={() => setShowCreatePost(false)} />
              </div>
            </div>
          </div>
        )}
        {/* ^ FOR CREATE POST FUNCTIONALITY ^ */}
    </div>
  )
}
export default Home