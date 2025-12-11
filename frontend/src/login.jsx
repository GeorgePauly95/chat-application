import './login.css'
import App from './App.jsx'
import { useState } from 'react'


function Start() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  return (
    <div>
      {isLoggedIn ? <App /> : <Login isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />}
    </div>

  )
}

function Login({ setIsLoggedIn }) {

  function login(e) {
    var username = e.get("username")
    fetch("/api/login", {
      method: "POST",
      body: JSON.stringify({ username: username })
    })
      .then(response => response.json())
      .then(data => {
        if (data) {
          setIsLoggedIn(true)
        }
      })
  }

  return (
    <div className="box_form">
      <form action={login} className='login_form'>
        <div>
          <label for="username">username</label>
          <input name="username" type='text' />
        </div>
        <div>
          <label for="password" type='text'>password</label>
          <input name="password" />
        </div>
        <button type="submit"> Sign in</button>
      </form>
    </div>
  )
}

export default Start 
