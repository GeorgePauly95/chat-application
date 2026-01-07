import { useState } from "react"
import Conversations from "./conversations"
import Contacts from "./contacts"
import "./sidepanel.css"
import "./contacts.css"

function SidePanel({ user_id, convs, setCurrentGroup_id }) {
  const [contactsView, setContactsView] = useState(false)
  function handleAddGroups() {
    setContactsView(true);
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
      {!contactsView ? <Conversations user_id={user_id} convs={convs} setCurrentGroup_id={setCurrentGroup_id} /> :
        <Contacts user_id={user_id} contactsView={contactsView} setContactsView={setContactsView} />}
    </div>
  )
}


export default SidePanel
