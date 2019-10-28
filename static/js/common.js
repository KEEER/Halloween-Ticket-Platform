;(function() {
  var $ = function(sel) {return document.querySelector(sel)}
  var $$ = function(sel) {return document.querySelectorAll(sel)}

  var ripples = [].concat(Array.from($$('[data-ripple]')), Array.from($$('.mdc-button')))
  for(var i = 0; i < ripples.length; i++) {
    mdc.ripple.MDCRipple.attachTo(ripples[i])
  }
})()
