import { useState, useEffect } from 'react'
import Conversations from './conversations.jsx'
import isEmptyMessage from './utils.js'
import './App.css'

function App() {
  return (
    <div className="box_outer">
      <Conversations />
      <TextInput />
    </div>
  )
}

const userId = 2

function TextInput() {
  const [msgHst, setMsghst] = useState([{ "content": "" }])

  useEffect(() => {
    fetch("/api/messages").then(response => response.json())
      .then(data => {
        setMsghst(data)
      })
  }, [])

  function sendMessage(e) {
    var current_message = e.get("currmsg")
    if (isEmptyMessage(current_message)) {
      return
    }
    fetch("/api/messages", {
      method: "POST",
      body: JSON.stringify({
        "sender_id": 2,
        "group_id": 1,
        "content": current_message,
      })
    })
      .then(response => {
        if (response.ok) {
          setMsghst([...msgHst, {
            "sender_id": 2,
            "group_id": 1,
            "content": current_message,
          }])
          return response.json()
        }
        return "Message Failed"
      })
      .then(data => console.log(data))
  }


  return (
    <div className='box_inner'>
      {<MessageHistory msgHst={msgHst} />}
      <form action={sendMessage} className='form'>
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
    <div className={userId != message.sender_id ? 'msgl' : 'msgr'}>{message}</div>
  )
}

export default App
