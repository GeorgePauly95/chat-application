import { useState, useEffect } from 'react'
import SidePanel from './sidepanel.jsx'
import isEmpty from './utils.js'
import './App.css'

function App({ user_id }) {
  const [group_id, setGroup_id] = useState(5)
  return (
    <div className="box_outer">
      <SidePanel user_id={user_id} group_id={group_id} setGroup_id={setGroup_id} />
      <TextInput user_id={user_id} group_id={group_id} setGroup_id={setGroup_id} />
    </div>
  )
}

function TextInput({ user_id, group_id }) {
  const [msgHst, setMsghst] = useState([{ "content": "" }])

  useEffect(() => {
    fetch(`/api/messages/?groupid=${group_id}`).then(response => response.json())
      .then(data => {
        setMsghst(data)
      })
  }, [group_id])

  function sendMessage(e) {
    var current_message = e.get("currmsg")
    if (isEmpty(current_message)) {
      return
    }
    fetch("/api/messages", {
      method: "POST",
      body: JSON.stringify({
        "sender_id": user_id,
        "group_id": group_id,
        "content": current_message,
      })
    })
      .then(response => {
        if (response.ok) {
          setMsghst([...msgHst, {
            "sender_id": user_id,
            "group_id": group_id,
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
      {<MessageHistory msgHst={msgHst} user_id={user_id} />}
      <form action={sendMessage} className='form'>
        <textarea name="currmsg" type="text" className="currmsg" placeholder="enter message here" />
        <button type="submit" className="sendbtn">Send</button>
      </form>
    </div>
  )
}

function MessageHistory({ msgHst, user_id }) {
  return (<div className='msgHst'>
    {msgHst.map(message => <MessageBlob key={message["id"]} message={message} user_id={user_id} />)}
  </div>)
}

function MessageBlob({ message, user_id }) {
  return (
    <div className={"msg " + (message["sender_id"] == user_id ? "msgr" : "msgl")}>
      {message["content"]}
    </div>
  )
}

export default App
