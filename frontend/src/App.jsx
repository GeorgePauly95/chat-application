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
        const n = data.length;
        let messages = [];
        for (let i = 0; i < n; i++) {
          messages.push(data[i]["messageContent"])
        };
        setMsghst(messages)
      })
  }, [])

  useEffect(() => {
    fetch("/api/messages", {
      method: "POST",
      body: JSON.stringify({
        "senderName": "George",
        "messageContent": message,
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
    setMessage(e.get("currmsg"))
    setMsghst([...msgHst, message])
  }

  return (
    <div>
      <form action={sentMessage}>
        <input name="currmsg" type="text" className="currmsg" placeholder="enter message here" />
        <button type="submit" className="sendbtn">Send</button>
      </form>
      {<MessageHistory msgHst={msgHst} />}
      {message && <MessageBlob message={message} />}
    </div>
  )
}

function MessageHistory({ msgHst }) {
  return (<div>
    {msgHst.map(message => <MessageBlob message={message} />)}
  </div>)
}

function MessageBlob({ message }) {


  return (
    <div className='blob'>{message}</div>
  )
}

export default App
