import { useNavigate } from 'react-router-dom'

function Home() {
  const navigate = useNavigate()

  return (  
    <div>   
        <h2 className='text-gray-700'>Home Page</h2>
        <p>Welcome to the Yapper home page!</p>
        <button type="button" onClick={() => navigate('/CreatePost')}>
          Create a post
        </button>
    </div>
  )
}
export default Home