function xhr({ method, url, params, data, done }) {
  var xhr = new XMLHttpRequest();
  method = method.toUpperCase();

  var pair = [];
  for (var k in params) {
    pair.push(k + '=' + params[k]);
  }
  var str = pair.join('&');
  if (method === 'GET') {
    url += '?' + str;
  }
  xhr.open(method, url);

  if (method === 'POST') {
    xhr.setRequestHeader('Content-Type', 'application/json');
  }

  xhr.send(data ? JSON.stringify(data) : null);

  xhr.onreadystatechange = function () {
    if (this.readyState === 4) {
      done(JSON.parse(xhr.responseText));
    }
  };
}

window.xhr = xhr;
