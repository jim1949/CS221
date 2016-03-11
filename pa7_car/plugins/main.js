// Include this script to include everything you need.

(function() {
  var head = document.getElementsByTagName('head')[0];

  function includeScript(src, text) {
    var script = document.createElement('script');
    script.src = src;
    if (text) script.text = text;
    head.appendChild(script);
    return script;
  }

  function includeStylesheet(href) {
    var css = document.createElement('link');
    css.setAttribute('rel', 'stylesheet');
    css.setAttribute('href', href);
    head.appendChild(css);
    return css;
  }

  function initMathJax(scriptLocation, fallbackScriptLocation) {
    if (typeof(sfig) != 'undefined') return;  // Already loaded through sfig
    var script = includeScript(scriptLocation);
    var buf = '';
    buf += 'MathJax.Hub.Config({';
    buf += '  extensions: ["tex2jax.js", "TeX/AMSmath.js", "TeX/AMSsymbols.js"],';
    buf += '  tex2jax: {inlineMath: [["$", "$"]]},';
    buf += '});';
    script.innerHTML = buf;

    // If fail, try the fallback location
    script.onerror = function() {
      if (fallbackScriptLocation)
        initMathJax(fallbackScriptLocation, null);
    }
  }

  initMathJax(
    'plugins/MathJax/MathJax.js?config=default',
    //'https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js?config=default',
    ((window.location.protocol != "file:") ?
    '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=default' :
    'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default')
  );

  includeScript('plugins/jquery.min.js');
  includeStylesheet('plugins/main.css');
})();

function fixScrollPosition() {
  var store = {};
  if (typeof(localStorage) != 'undefined' && localStorage != null) store = localStorage;

  var scrollTopKey = window.location.pathname+'.scrollTop';
  // Because we insert MathJax, we lose the scrolling position, so we have to
  // put it back manually.
  window.onscroll = function() {
    store[scrollTopKey] = document.body.scrollTop;
  }
  if (store.scrollTop)
    window.scrollTo(0, store[scrollTopKey]);
}

function onLoad(ownerName, attributionHtml) {
  var header = $('#assignmentHeader');
  var p = $('<p>')
    .append($('<div>', {'class': 'assignmentTitle'}).append(document.title))
    .append($('<div>').append('Stanford CS221 Fall 2014-2015'.bold()));
  var creds = $('<div>', {'class': 'assignmentCreds'})
  if (attributionHtml)
    creds.append($('<div>').append(attributionHtml))
  if (ownerName)
    creds.append($('<div>').append('Owner TA: ' + ownerName))
  creds.append($('<div id="disclaimer">').append('Note: grader.py only provides basic tests.  Passing grader.py does not by any means guarantee full points.'))
  header.append(p.append(creds));

  // Link to code
  $('code').each(function(i, elem) {
    if ($(elem).attr('class') == 'link')  {
      var value = elem.innerHTML;
      if (value.match(/.py$/))
        elem.innerHTML = '<a href="' + value + '">' + value + '</a>';
    }
  });

  fixScrollPosition();
}
