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
      document.getElementById("canvasText").innerHTML=canvas;
    }
  }

}

addLoadEvent(loadXMLDoc)
addLoadEvent(getBitmap)
