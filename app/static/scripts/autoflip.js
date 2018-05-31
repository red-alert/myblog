function autoFlip(func) {
  setInterval(function() {
    setTimeout("randomFlip()", randomTime(2500,1500))
  }, randomTime(500,500))
}

function randomFlip() {
  flippers = document.getElementsByClassName("flip-container");
  fnum = Math.floor(Math.random()*flippers.length);
  flipper = flippers[fnum];
  flipper.classList.toggle("flip");
}

function randomTime(dif, shortest) { //in miliseconds
  t = Math.floor((Math.random()*dif)+shortest)
  return t
}

function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      oldonload();
      func();
    }
  }
}

addLoadEvent(autoFlip)
