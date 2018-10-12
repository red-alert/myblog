var d;

!function(d, $, _){
  var modules = {
    d: d,
    jQuery: $,
    underscore: _,
    store: store,
  };

  function require(name){
    return modules[name];
  }

  var d.placeModule = function(name, moduleFunction){
    var exportVal = moduleFunction(require);
    if (name) {
      modules[name] = exportVal;
    }
  };
}(d, $, _);
