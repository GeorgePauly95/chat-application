import { useState, useEffect } from 'react'
import SidePanel from './sidepanel.jsx'
import isEmpty from './utils.js'
import './App.css'

function App({ user_id }) {

  const [convs, setConvs] = useState([])
  const [currentGroup_id, setCurrentGroup_id] = useState()
  const [ws, setWs] = useState(() => new WebSocket("ws://localhost:5173/api/messages"))


  useEffect(() => {

    fetch(`/api/groups/?user_id=${user_id}`)
      .then(response => response.json())
      .then(conversations => {
        setConvs(conversations);
      })
  }, [user_id])

  return (
    <div className="box_outer">
      <SidePanel user_id={user_id} convs={convs} currentGroup_id={currentGroup_id} setCurrentGroup_id={setCurrentGroup_id} />
      <MainPanel user_id={user_id} convs={convs} currentGroup_id={currentGroup_id} ws={ws} />
    </div>
  )
}

function MainPanel({ user_id, convs, setConvs, currentGroup_id, ws }) {
  const currentGroup = convs.filter((conv) => conv["id"] === currentGroup_id)[0];

  if (!currentGroup) {
    return <div className='loading'>WhatsGapp</div>
  }

  var messages = currentGroup.messages
  ws.addEventListener("message", (e) => {
    messages = [...messages, e.data]
  })



  function send_message(e) {

    var messageContent = e.get("currmsg")

    if (isEmpty(messageContent)) {
      return
    }

    ws.send(JSON.stringify(
      {
        "sender_id": user_id,
        "group_id": currentGroup_id,
        "content": messageContent,
      }
    ))
  }

  return (
    <div className='box_inner'>
      {<MessageHistory messages={messages} user_id={user_id} />}
      <form action={send_message} className='form'>
        <textarea name="currmsg" type="text" className="currmsg" placeholder="enter message here" />
        <button type="submit" className="sendbtn">Send</button>
      </form>
    </div>
  )
}

function MessageHistory({ messages, user_id }) {
  return (<div className='msgHst'>
    {messages.map(message => <MessageBlob key={message["id"]} message={message} user_id={user_id} />)}
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
