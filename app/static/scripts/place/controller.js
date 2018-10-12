var xmlhttp;
function loadXMLDoc(url) {
  xmlhttp = null;
  if (window.XMLHttpRequest)
  {
    xmlhttp = new XMLHttpRequest();
  }
  else if (window.ActiveXObject)
  {
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
}

function getBitmap() {
  var dfd = $.Deferred();
  var timestamp;
  var canvas = new Uint8Array(100 * 100);
  var offset = 0;

  function handleChunk(responseArray) {

    // If we haven't set the timestamp yet, slice it off of this chunk
    if (!timestamp) {
      timestamp = (new Uint32Array(responseArray.buffer, 0, 1))[0],
      responseArray = new Uint8Array(responseArray.buffer, 4);
    }
    // Each byte in the responseArray represents two values in the canvas
    for (var i = 0; i < responseArray.byteLength; i++) {
      canvas[offset + 2 * i] = responseArray[i] >> 4;
      canvas[offset + 2 * i + 1] = responseArray[i] & 15;
    }
    offset += responseArray.byteLength * 2;
  }

  xmlhttp.responseType = "arraybuffer";
  xmlhttp.open("GET","../place/pixel",true);
  xmlhttp.send();

  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState==4 && xmlhttp.status==200) {
      arrayBuffer = xmlhttp.response;
      var responseArray = new Uint8Array(arrayBuffer);
      handleChunk(responseArray);
      dfd.resolve(timestamp, canvas);
    }
  }
  return dfd.promise()
}

var Canvasse = {
  var width = 100;
  var height = 100;
  var canvas = document.getElementById('place-canvasse');
  var ctx = canvas.getContext('2d');
  var buffer = new ArrayBuffer( 100 * 100 * 4);
  var readBuffer = new Unit8ClampedArray(this.buffer);
  var writeBuffer = new Unit8Array(this.buffer);
  var isBufferDirty = false;
  var isDisplayDirty = false;

  function drawTileAt(x, y, color) {
    this.drawTileToBuffer(x, y, color);
  }

  function drawTileToBuffer(x, y, color){
    var i = this.getIndexFromCoords(x, y);
    this.setBufferState(i, color);
  }

  function getIndexFromCoords(x, y) {
    return y * 100 + x;
  }

  function setBufferState(i, color) {
    this.writeBuffer[i] = color;
    this.isBufferDirty = true;
  }

  function drawTileToDisplay(x, y, color) {
    this.ctx.fillStyle = color;
    this.ctx.fillRect(x, y, 1, 1);
    this.isDisplayDirty = true;
  }

  function drawBufferToDisplay() {
    var imageData = new ImageData(this.readBuffer, this.width, this.height);
    this.ctx.putImageData(imageData, 0, 0);
    this.isBufferDirty = false;
  }

  function clearRectFromDisplay(x, y, width, height) {
    this.ctx.clearRect(x, y, width, height);
    this.isDisplayDirty = true;
  }
}

var Client = {
  function setInitialState(state) {
    var canvas = [];
    var colorIndex, color;
    for (var i=0; i<state.length; i++) {
      colorIndex=state[i];
      color = this.getPaletteColorABGR(colorIndex);
      Canvasse.setBufferState(i,color);
      if (colorIndex > 0) {
        this.state[i] = colorIndex;
      }
    }
  }
}

function draw() {
  getBitmap().then(function(timestamp, canvas){
    if (!canvas) { return; }



  })
}

addLoadEvent(loadXMLDoc)
addLoadEvent(getBitmap)
