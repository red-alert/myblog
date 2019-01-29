// var xmlhttp;
// function loadXMLDoc(url) {
//   xmlhttp = null;
//   if (window.XMLHttpRequest)
//   {
//     xmlhttp = new XMLHttpRequest();
//   }
//   else if (window.ActiveXObject)
//   {
//     xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
//   }
// }

function getBitmap() {
  var dfd = $.Deferred();
  var timestamp;
  var canvas = new Uint8Array(500 * 500);
  var offset = 0;

  function handleChunk(responseArray) {
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

  var xmlhttp = new XMLHttpRequest();
  xmlhttp.responseType = "arraybuffer";
  xmlhttp.open("GET","../place/pixel",true);

  // xmlhttp.onload = function(oEvent) {
  //   var arrayBuffer = xmlhttp.Response;
  //   if (!arrayBuffer) { dfd.resolve(); }
  //   var responseArray = new Uint8Array(arrayBuffer);
  //   handleChunk(responseArray);
  //   dfd.resolve(timestamp, canvas);
  // };

  xmlhttp.send(null);
  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState==4 && xmlhttp.status==200) {
      var arrayBuffer = xmlhttp.response;
      var responseArray = new Uint8Array(arrayBuffer);
      handleChunk(responseArray);
      dfd.resolve(timestamp, canvas);
    }
  }
  return dfd.promise();
}

var Canvasse = {
  width: 0,
  height: 0,
  el: null,
  ctx: null,
  isBufferDirty: false,
  isDisplayDirty: false,

  init: function(el, width, height) {
    this.width = width;
    this.height = height;
    this.el = el;
    this.ctx = this.el.getContext('2d');
    this.buffer = new ArrayBuffer(width * height * 4);
    this.readBuffer = new Uint8ClampedArray(this.buffer);
    this.writeBuffer = new Uint32Array(this.buffer);
  },

  drawTileAt: function(x, y, color) {
    this.drawTileToBuffer(x, y, color);
  },

  drawTileToBuffer: function(x, y, color){
    var i = this.getIndexFromCoords(x, y);
    this.setBufferState(i, color);
  },

  getIndexFromCoords: function(x, y) {
    return y * 500 + x;
  },

  setBufferState: function(i, color) {
    this.writeBuffer[i] = color;
    this.isBufferDirty = true;
  },

  drawFileToDisplay: function(x, y, color) {
    this.ctx.fillStyle = color;
    this.ctx.fillRect(x, y, 1, 1);
    this.isDisplayDirty = true;
  },

  drawBufferToDisplay: function() {
    var imageData = new ImageData(this.readBuffer, this.width, this.height);
    this.ctx.putImageData(imageData, 0, 0);
    this.isBufferDirty = false;
  },

  clearRectFromDisplay: function(x, y, width, height) {
    this.ctx.clearRect(x, y, width, height);
    this.isDisplayDirty = true;
  },
<<<<<<< HEAD
}

var Camera = {
  zoomElement: null,
  panElement:null,
  isDirty: false,

  init: function(zoomElement, panElement) {
    this.zoomElement = zoomElement;
    this.panElement = panElement;
  },

  updateScale: function(s){
    this.isDirty = true;
    $(this.zoomElement).css({
      transform: 'scale(' + s + ',' + s + ')',
    });
  },

  updateTranslate: function(x, y) {
    this.isDirty = true;
    $(this.panElement).css({
      transform: 'translate(' + x + 'px',' +y + 'px')',
    });
  },
=======
>>>>>>> d32d90dc2a59d8229a5170cfad94570d34a132c4
}

var Client = {
  MAX_COLOR_INDEX: 15,
  DEFAULT_COLOR : '#FFFFFF',
  DEFAULT_COLOR_ABGR : 0xFFFFFFFF,
  DEFAULT_COLOR_PALETTE: [
    '#FFFFFF', // white
    '#E4E4E4', // light grey
    '#888888', // grey
    '#222222', // black
    '#FFA7D1', // pink
    '#E50000', // red
    '#E59500', // orange
    '#A06A42', // brown
    '#E5D900', // yellow
    '#94E044', // lime
    '#02BE01', // green
    '#00D3DD', // cyan
    '#0083C7', // blue
    '#0000EA', // dark blue
    '#CF6EE4', // magenta
    '#820080', // purple
  ],
  state: null,
  platte: null,

  init: function() {
    this.state = new Uint8Array(new ArrayBuffer(Canvasse.width * Canvasse.height)); // INITIALIZE CANVASSE STATE
    this.setColorPalette(this.DEFAULT_COLOR_PALETTE); // SET this.paletteABGR
    // Palette.generateSwatches(this.DEFAULT_COLOR_PALETTE);
  },

  setColorPalette: function(palette) {
    var isNew = this.palette === null;
    this.palette = palette;
    // Palette.generateSwatches(palette);
    var dataView = new DataView(new ArrayBuffer(4));
    dataView.setUint8(0, 0xFF);
    this.paletteABGR = palette.map(function(colorString) {
      var color = Client.parseHexColor(colorString);
      dataView.setUint8(1, color.blue);
      dataView.setUint8(2, color.green);
      dataView.setUint8(3, color.red);
      return dataView.getUint32(0);
    });
    if (!isNew) {
      this.setInitialState(this.state); // initialize
    }
  },

  parseHexColor: function(hexColor) {
    var colorVal = parseInt(hexColor.slice(1), 16);
    // hexColor = #94E004
    // hexColor.slice(1) = 94E004
    // parseInt() = 0x94E004 -->  45160004
    return {
      red: colorVal >> 16 & 0xFF,
      green: colorVal >> 8 & 0xFF,
      blue: colorVal & 0xFF,
    } // return {red: ,blue: , green: ,}
  },

  setInitialState: function(state) {
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
    Canvasse.drawBufferToDisplay();
  },

  getPaletteColor: function(colorIndex) {
    colorIndex = Math.min(this.MAX_COLOR_INDEX, Math.max(0, colorIndex|0));
    return this.palette[colorIndex % this.palette.length] || DEFAULT_COLOR;
  }, // USED FOR SETTING COLOR

  getPaletteColorABGR: function(colorIndex) {
    colorIndex = Math.min(this.MAX_COLOR_INDEX, Math.max(0, colorIndex|0));
    return this.paletteABGR[colorIndex % this.paletteABGR.length] || DEFAULT_COLOR_ABGR;
  }, // USED FOR DRAWING COLOR TO BUFFER
}

var Palette = {
}

function draw() {
  var can = document.getElementById('place-canvasse');
<<<<<<< HEAD
  var camera = document.getElementById('place-camera');
  var viewer = document.getElementById('place-viewer');
  Camera.init(viewer, camera);
=======
>>>>>>> d32d90dc2a59d8229a5170cfad94570d34a132c4
  Canvasse.init(can,500,500);
  Client.init();
  getBitmap().then(function(timestamp, canvas){
    if (!canvas) { return; }
    Client.setInitialState(canvas);
  })
}

// addLoadEvent(loadXMLDoc)
addLoadEvent(draw)
