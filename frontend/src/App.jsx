import { useState, useEffect } from 'react'
import './App.css'
import Conversations from './conversations.jsx'

function App() {
  return (
    <div className="box_outer">
      <Conversations />
      <TextInput />
    </div>
  )
}


function TextInput() {
  const [msgHst, setMsghst] = useState([{ "messageContent": "" }])

  useEffect(() => {
    fetch("/api/messages").then(response => response.json())
      .then(data => {
        setMsghst(data)
      })
  }, [])

  function sendMessage(e) {
    var uuid = crypto.randomUUID()
    setMsghst([...msgHst, {
      "id": uuid,
      "sender_id": 1,
      "group_id": 1,
      "content": e.get("currmsg"),
      "sent_at": "12-12-2025",
      "deleted_at": null,
      "replied_to": null,
    }])
    fetch("/api/messages", {
      method: "POST",
      body: JSON.stringify({
        "id": uuid,
        "sender_id": 1,
        "group_id": 1,
        "content": e.get("currmsg"),
        "sent_at": "12-12-2024",
        "deleted_at": null,
        "replied_to": null,
      })
    })
      .then(response => response.json())
      .then(data => console.log(data))

  }

  return (
    <div className='box_inner'>
      <div className='box_messages'>
        {<MessageHistory msgHst={msgHst} />}
      </div>
      <form action={sendMessage} className='form'>
        {/* onKeyUp={}  */}
        <textarea name="currmsg" type="text" className="currmsg" placeholder="enter message here" />
        <button type="submit" className="sendbtn">Send</button>
      </form>
    </div>
  )
}

function MessageHistory({ msgHst }) {
  return (<div className='msgHst'>
    {msgHst.map(message => <MessageBlob message={message["content"]} />)}
  </div>)
}

function MessageBlob({ message }) {
  return (
    <div className='msg'>{message}</div>
  )
}

export default App
