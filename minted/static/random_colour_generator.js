
var build_random_colours = function(numberOfColours){
    colours = [];
    for (var i = 0; i<numberOfColours; i++){
      r = Math.floor(Math.random() * 255);
      g = Math.floor(Math.random() * 255);
      b = Math.floor(Math.random() * 255);
      colours.push(`rgba(${r}, ${g}, ${b}, 1)`);
    }
    return colours;
}