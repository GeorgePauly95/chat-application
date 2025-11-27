import { useState, useEffect } from 'react'
import './App.css'

function App() {
  return (
    <div className="box">
      <TextInput />
    </div>
  )
}


function TextInput() {
  const [message, setMessage] = useState("")
  const [msgHst, setMsghst] = useState([])

  useEffect(() => {
    fetch("/api/messages").then(response => response.json())
      .then(data => {
        setMsghst(data)
      })
  }, [])

  useEffect(() => {
    fetch("/api/messages", {
      method: "POST",
      body: JSON.stringify({
        "senderName": "George",
        "messageContent": message["messageContent"],
        "sentAt": "12-12-2024",
        "readStatus": true,
        "repliedTo": null,
      })

    })
      .then(response => response.json())
      .then(data => console.log(data))
  },
    [message])

  function sentMessage(e) {
    setMessage({
      "senderName": "George",
      "messageContent": e.get("currmsg"),
      "sentAt": "12-12-2025",
      "readStatus": true,
      "repliedTo": null,
    })
    setMsghst([...msgHst, message])
  }

  return (
    <div>
      <form action={sentMessage}>
        <input name="currmsg" type="text" className="currmsg" placeholder="enter message here" />
        <button type="submit" className="sendbtn">Send</button>
      </form>
      {<MessageHistory msgHst={msgHst} />}
      {message && <MessageBlob message={message["messageContent"]} />}
    </div>
  )
}

function MessageHistory({ msgHst }) {
  return (<div>
    {msgHst.map(message => <MessageBlob message={message["messageContent"]} />)}
  </div>)
}

function MessageBlob({ message }) {
  return (
    <div className='blob'>{message}</div>
  )
}

export default App
