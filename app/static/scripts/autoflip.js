function autoFlip(func) {
  setInterval(function() {
    setTimeout("randomFlip()", randomTime())
  }, randomTime())
}

function randomFlip() {
  flippers = document.getElementsByClassName("flip-container");
  fnum = Math.floor(Math.random()*flippers.length);
  flipper = flippers[fnum];
  flipper.classList.toggle("flip");
}

function randomTime() {
  t = Math.floor((Math.random()*500)+500)
  return t
}

addLoadEvent(autoFlip)
