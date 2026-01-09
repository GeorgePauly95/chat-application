import './login.css'
import App from './App.jsx'
import { useEffect, useState } from 'react'


function Start() {
  const [user_id, setUser_id] = useState(null)


  useEffect(() => {
    fetch("/api/me")
      .then(response => {
        if (response.ok) {
          return response.json()
        }
        return null
      })
      .then(user_data => {
        if (user_data) {
          setUser_id(user_data["user_id"])
        }
      })
  })
  return (
    <div>
      {user_id != null ? <App user_id={user_id} /> : <Login setUser_id={setUser_id} />}
    </div>

  )
}

function Login({ setUser_id }) {

  function login(e) {
    var username = e.get("username")
    var password = e.get("password")
    fetch("/api/login", {
      method: "POST",
      body: JSON.stringify({
        username: username,
        password: password,
      })
    })
      .then(response => response.json())
      .then(data => { setUser_id(data["user_id"]) })
  }

  function register(e) {
    var username = e.get("username")
    var password = e.get("password")
    fetch("/api/register", {
      method: "POST",
      body: JSON.stringify({
        username: username,
        password: password
      })
    })
      .then(response => response.json())
      .then(data => { setUser_id(data["user_id"]) })
  }

  return (
    <div className="box_form">
      <form action={login} className='login_form'>
        <div className="box_input">
          <label for="username" className="user_detail">Username</label>
          <input name="username" type='text' />
        </div>
        <div className="box_input">
          <label for="password" className="user_detail">Password</label>
          <input name="password" type='password' />
        </div>
        <button type="submit" className="submit_btn">Sign&nbsp;in</button>
        <div className='sign_up'>
          Still not a User?
        </div>
        <button type="submit" formAction={register} className="submit_btn">Sign&nbsp;up</button>
      </form>
    </div>
  )
}

export default Start 
