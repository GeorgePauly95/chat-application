import { useState, useEffect } from 'react'
import './App.css'

function App() {
  return (
    <div className="box_outer">
      <Conversations />
      <TextInput />
    </div>
  )
}

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

function TextInput() {
  const [msgHst, setMsghst] = useState([{ "messageContent": "" }])

  useEffect(() => {
    fetch("/api/messages").then(response => response.json())
      .then(data => {
        setMsghst(data)
      })
  }, [])

  function sendMessage(e) {
    setMsghst([...msgHst, {
      "senderName": "George",
      "messageContent": e.get("currmsg"),
      "sentAt": "12-12-2025",
      "readStatus": true,
      "repliedTo": null,
    }])
    fetch("/api/messages", {
      method: "POST",
      body: JSON.stringify({
        "senderName": "George",
        "messageContent": e.get("currmsg"),
        "sentAt": "12-12-2024",
        "readStatus": true,
        "repliedTo": null,
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
        <textarea name="currmsg" type="text" className="currmsg" placeholder="enter message here" />
        <button type="submit" className="sendbtn">Send</button>
      </form>
    </div>
  )
}

function MessageHistory({ msgHst }) {
  return (<div className='msgHst'>
    {msgHst.map(message => <MessageBlob message={message["messageContent"]} />)}
  </div>)
}

function MessageBlob({ message }) {
  return (
    <div className='msg'>{message}</div>
  )
}

export default App
