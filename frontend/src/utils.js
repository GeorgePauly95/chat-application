
function isEmpty(text) {
  const cleaned_text = text.trim();
  if (cleaned_text == "") {
    return true
  }
  return false
}

export default isEmpty
