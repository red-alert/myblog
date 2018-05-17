function shotTime(){
  if (!document.getElementById || !document.getElementById('shot_time')) return false;
  if (!inputSupportsType('date')) return false;
  input = document.getElementById('shot_time')
  formInputType(input, 'date')
}

function formInputType(input, type) {
  input.setAttribute('type', type)
}

function inputSupportsType(type) {
  if (!document.createElement) return false;
  var input = document.createElement('input');
  input.setAttribute('type', type);
  if (input.type == 'text' && type != 'text') {
    return false;
  } else {
    return true;
  }
}

addLoadEvent(shotTime)
