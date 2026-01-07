import { useState, useEffect } from 'react'
import './conversations.css'

function Conversations({ user_id, convs, setCurrentGroup_id }) {


  return (
    <div className='box_conv'>
      {convs.map(conv => <Conversation key={conv.id} conv={conv} setCurrentGroup_id={setCurrentGroup_id} />)}
    </div >
  )
}

function Conversation({ conv, setCurrentGroup_id }) {
  var id = conv["id"]
  return (
    <div className='conv' onClick={() => { setCurrentGroup_id(id) }}>
      {conv["name"]}
    </div>
  )
}

export default Conversations
