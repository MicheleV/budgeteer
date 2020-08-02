// TODO: lint me!
function setInput(element, value){
  const formNum = element.id.replace("copy-button-","");
  const targetId = `id_form-${formNum}-amount`
  print(targetId, value)
  document.getElementById(targetId).value = value
}