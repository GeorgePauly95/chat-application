import { useState, useEffect } from 'react'
import './conversations.css'

function Conversations() {
  const [convs, setConvs] = useState([])
  useEffect(() => {
    fetch("/api/groups").then(response => response.json()).then(data => { setConvs(data) })
  }, [])
  return (
    <div className='box_conv'>
      {convs.map(conv => <Conversation conv={conv["name"]} />)}
    </div >
  )
}
function Conversation({ conv }) {
  return (
    <div className='conv'>
      {conv}
    </div>
  )
}

export default Conversations
