import { useState, useEffect } from 'react'
import SidePanel from './sidepanel.jsx'
import { isEmpty } from './utils.js'
import './App.css'

function App({ user_id }) {

  const [convs, setConvs] = useState([{ id: null, messages: [] }])
  const [currentGroup_id, setCurrentGroup_id] = useState()
  const [ws, setWs] = useState(null)


  useEffect(() => {

    const websocket = new WebSocket(`ws://localhost:5173/api/ws/${user_id}`)
    setWs(websocket)

    return () => { websocket.close() }
  }, [user_id])

  useEffect(() => {
    if (!ws) return

    function handleMessage(e) {
      var message = JSON.parse(e.data)
      var group_id = message.group_id

      setConvs((convs) => {
        return convs.map((conv) => {
          if (conv.id == group_id) {
            return { ...conv, messages: [...conv.messages, message] }
          }
          return conv
        })
      })
    }
    ws.addEventListener("message", handleMessage)
    return () => { ws.removeEventListener("message", handleMessage) }
  }, [ws]
  )


  useEffect(() => {
    fetch(`/api/groups/?user_id=${user_id}`)
      .then(response => response.json())
      .then(conversations => {
        setConvs(conversations);
      })
  }, [ws, user_id])


  const currentGroup = convs.filter((conv) => conv["id"] === currentGroup_id)[0];

  if (!currentGroup) {
    return <div className='loading'>WhatsGapp</div>
  }

  var messages = currentGroup.messages



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
    <div className="box_outer">
      <SidePanel user_id={user_id} convs={convs} setCurrentGroup_id={setCurrentGroup_id} />
      <MainPanel user_id={user_id} messages={messages} send_message={send_message} />
    </div>
  )
}

function MainPanel({ user_id, messages, send_message }) {



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
