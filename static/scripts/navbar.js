$(function () {
  $('#logout').click(function () {
    $.ajax({
      type: 'POST',
      url: '/api/user/logout',
      contentType: 'application/json',
      dataType: 'json',
      success: function (resp) {
        window.location = '/';
      },
      failure: function (errMsg) {
        window.location = '/';
      },
    });
  });
});
