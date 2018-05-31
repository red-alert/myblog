function autoFlip(func) {
  setInterval(function() {
    setInterval("randomFlip()", randomTime())
  }, randomTime())
}

function randomFlip() {
  flippers = document.getElementsByClassName("flip-container");
  fnum = Math.floor(Math.random()*flippers.length);
  flipper = flippers[fnum];
  flipper.classList.toggle("flip");
}

function randomTime() {
  t = Math.floor((Math.random()*500)+3500)
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

addLoadEvent(randomFlip)
addLoadEvent(autoFlip)
