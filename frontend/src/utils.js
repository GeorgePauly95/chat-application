
function isEmptyMessage(message) {
  console.log(message)
  message = message.replaceAll(" ", "");
  console.log(message)
  message = message.replaceAll("\n", "");
  console.log(message)
  if (message == "") {
    return true
  }
  return false
}

export default isEmptyMessage
