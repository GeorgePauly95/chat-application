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

    fetch("/api/messages", {
      method: "POST",
      body: JSON.stringify({
        "sender_id": 2,
        "group_id": 1,
        "content": e.get("currmsg"),
      })
    })
      .then(response => {
        if (response.ok) {
          setMsghst([...msgHst, {
            "sender_id": 2,
            "group_id": 1,
            "content": e.get("currmsg"),
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
    <div className={userId != message.sender_id ? 'msgl' : 'msgr'}>{message}</div>
  )
}

export default App
