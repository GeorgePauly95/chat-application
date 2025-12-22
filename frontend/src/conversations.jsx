import { useState, useEffect } from 'react'
import './conversations.css'

function Conversations({ user_id, setGroup_id }) {
  const [convs, setConvs] = useState([])
  useEffect(() => {

    // need to change it to fetch groups for particular user id
    fetch(`/api/groups/?user_id=${user_id}`)
      .then(response => response.json())
      .then(data => {
        setConvs(data)
      })
  }, [user_id])

  return (
    <div className='box_conv'>
      {convs.map(conv => <Conversation key={conv.id} conv={conv} setGroup_id={setGroup_id} />)}
    </div >
  )
}

function Conversation({ conv, setGroup_id }) {
  var id = conv["id"]
  return (
    <div className='conv' onClick={() => { setGroup_id(id) }}>
      {conv["name"]}
    </div>
  )
}

export default Conversations
