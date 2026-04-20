import { useEffect } from 'react'
import axios from 'axios'

function App() {
  useEffect(() => {
    // 장고 서버로 테스트 요청 보내기
    axios.get('http://localhost:8000/api/users/test/')
      .then(response => {
        console.log("드디어 성공!:", response.data.message)
      })
      .catch(error => {
        console.error("에러 발생!:", error)
      })
  }, [])

  return (
    <div>
      <h1>Tide Project</h1>
      <p>콘솔창(F12)을 확인해보세요!</p>
    </div>
  )
}

export default App
