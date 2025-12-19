import { useState, useEffect } from "react"


function Contacts({ user_id, contactsView, setContactsView }) {
  const [contacts, setContacts] = useState([])

  useEffect(() => {
    fetch(`/api/users/${user_id}`)
      .then(response => response.json()).then(data => { setContacts(data) })
  }, [user_id])

  function createNewGroup(formData) {
    fetch("/api/groups", {
      "method": "POST",
      "body": JSON.stringify({
        "name": formData.get("groupname"),
        "admin": user_id,
        "members": formData.getAll("contact"),
      })
    })
    setContactsView(false)
  }

  return (
    <div className="box_contacts">
      <button type="submit" className="close_contacts" onClick={() => setContactsView(false)}>X</button>
      <form action={createNewGroup} className="box_group">
        <button type="submit" className="create_group">create&nbsp;group</button>
        <div className="box_groupname">
          <label for="groupname">Group name: </label>
          <input type="text" name="groupname" />
        </div>
        <div className="list_contact">
          {contacts.map(contact => <Contact key={contact["id"]} contact={contact} user_id={user_id} />)}
        </div>
      </form>
    </div>
  )
}

function Contact({ contact, user_id }) {
  return (<div className="contact">
    <label for="contact">{contact["name"]}</label>
    <input type="checkbox" name="contact" value={contact["id"]} />
  </div>)
}

export default Contacts
