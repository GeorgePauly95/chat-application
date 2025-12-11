import './login.css'

function Login() {

  return (
    <div className="box_form">
      <form>
        <div>
          <label for="username">username</label>
          <input name="username" />
        </div>
        <div>
          <label for="password">password</label>
          <input name="password" />
        </div>
        <button type="submit"> Sign in</button>
      </form>
    </div>
  )
}

export default Login
