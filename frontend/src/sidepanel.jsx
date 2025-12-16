import { useState } from "react"
import Conversations from "./conversations"
import "./conversations.css"
function SidePanel({ user_id }) {
  const [contacts, setContacts] = useState(false)
  function handleAddGroups() {
    fetch("/api/users")
      .then(response => response.json())
      .then(result => console.log(result))
    setContacts(false);
    alert("Contacts!")
  }

  return (
    <div className="side_panel">
      <div className="header">
        <div className="app_name">
          WhatsGapp
        </div>
        <div className="add_group">
          <button type="button" className="add_group_btn" onClick={handleAddGroups}>+</button>
        </div>
      </div>
      {!contacts ? <Conversations user_id={user_id} /> : <Contacts users={users} />}
    </div>
  )
}

function Contacts({ users }) {
  return (
    <div>

    </div>
  )
}
export default SidePanel
