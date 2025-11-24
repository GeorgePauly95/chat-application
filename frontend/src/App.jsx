import { useState } from 'react'
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
  const [msghst, setMsghst] = useState([])
  function sentMessage(e) {
    setMessage(e.get("currmsg"))
    msghst.push(message)
    setMsghst(msghst)
  }
  return (
    <div>
      <form action={sentMessage}>
        <label>
          <input name="currmsg" type="text" className="currmsg" placeholder="enter message here" />
        </label>
        <button type="submit" className="sendbtn">Send</button>
      </form>
      {<MessageHistory msghst={msghst} />}
      {message && <MessageBlob message={message} />}
    </div>
  )
}

function MessageHistory({ msghst }) {
  return (<div>
    {msghst.map(message => <div>{message}</div>)}
  </div>)
}

function MessageBlob({ message }) {
  return (<div className='blob'>{message}</div>)
}


export default App
