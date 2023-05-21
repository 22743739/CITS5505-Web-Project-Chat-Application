window.userInfo = {};

function getUserInfo() {
  $.ajax({
    type: 'GET',
    url: '/api/user/info',
    contentType: 'application/json',
    dataType: 'json',
    success: function (resp) {
      if (resp.success) {
        var userInfo = resp.data;
        window.userInfo = userInfo;
        // render
        $('#sender').text(userInfo.name);
      } else {
        $('.invalid-server').text(resp.message);
      }
    },
    failure: function (errMsg) {
      $('.invalid-server').text(errMsg);
    },
  });
}

$(function () {
  getUserInfo();
});

$(function () {
  $('#search').click(function () {
    var inputVal = $('#input').val();
    if (!inputVal) {
      $('.invalid-server').text('Please provide the keyword');
      return;
    }

    $.ajax({
      type: 'GET',
      url: `/api/search?keyword=${inputVal}`,
      contentType: 'application/json',
      dataType: 'json',
      success: function (resp) {
        if (resp.success) {
          // render
          if (resp.data.length === 0) {
            $('.search-body').html(`<div class="search-nodata">No Data</div>`);
          } else {
            let html = '';
            resp.data.forEach((item) => {
              let receiver;
              if (item.receiver === 0) {
                receiver = 'Public Room';
              } else if (item.receiverInfo.id == window.userInfo.id) {
                receiver = 'You';
              } else {
                receiver = item.receiverInfo.name;
              }

              let sender;
              if (item.sender == window.userInfo.id) {
                sender = 'You';
              } else {
                sender = item.senderInfo.name;
              }

              html += `
                <p class="row">
                <div class="author">
                <p>【${sender}】to 【${receiver}】<span>${item.createAt}</span><p>
                <p>
                ${item.content}
                </p>
                </div>
              </p>
                `;
            });
            $('.search-body').html(html);
          }
        } else {
          $('.invalid-server').text(resp.message);
        }
      },
      failure: function (errMsg) {
        $('.invalid-server').text(errMsg);
      },
    });
  });
});
