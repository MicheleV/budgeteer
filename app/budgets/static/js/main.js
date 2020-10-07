// TODO: lint me!
function setInput(element, value){
  const formNum = element.id.replace("copy-button-","");
  const targetId = `id_form-${formNum}-amount`
  document.getElementById(targetId).value = value
}


function setToday(element, value){
  const today = new Date().toJSON().slice(0,10)
  const targetId = `id_date`
  document.getElementById(targetId).value = today
}

function firstDayOfThisMonth(element, value){
  const today = new Date().toJSON().slice(0,8).concat('01')
  const targetId = `id_date`
  document.getElementById(targetId).value = today
}