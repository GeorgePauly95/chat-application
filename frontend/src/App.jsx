import { StrictMode, useState } from 'react'
import './App.css'
function App() {

  return (
    <div>
      <MyConversation />
      <MyConversation />
      <MyConversation />
      <MyConversation />
      <MyConversation />
      <MyConversation />
      <MyConversation />
      <MyConversation />
    </div>
  )
}

function MyConversation() {
  return (
    <div className="convobox">
      <span> <img src="" alt="image" /></span>
      <span className="name">George Pauly</span>
      <span className="lastmsgtime">09:00 AM</span>
      <div className='lower'>
        <span className='readstatus'> Read </span>
        <span className='lastmsg'>
          Good Morning!
        </span>
      </div>
    </div >
  )

}

function ReadStatus() {

}
export default App
