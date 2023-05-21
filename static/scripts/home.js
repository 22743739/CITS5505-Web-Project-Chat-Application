window.userInfo = {};
window.userList = [];
window.currentConnected = '';

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

function getChatUsers() {
  $.ajax({
    type: 'GET',
    url: '/api/users/chat',
    contentType: 'application/json',
    dataType: 'json',
    success: function (resp) {
      if (resp.success) {
        var users = resp.data;
        window.userList = users;

        var html =
          '<li class="userList-item userList-public" data-key="0" data-name="public-room">Public Room</li>';

        users.forEach((user) => {
          html += `
            <li class="userList-item" data-key="${user.id}" data-name="${user.name}">
                ${user.name}(${user.email})
            </li>`;
        });
        // render
        $('#userList').html(html);
        $('.userList-item').click(function (e) {
          $('.userList-item').removeClass('userList-item-active');
          $(this).addClass('userList-item-active');
          var { key } = e.target.dataset;
          $('#textarea').val('');
          cahtTo(key);
        });
      } else {
        $('.invalid-server').text(resp.message);
      }
    },
    failure: function (errMsg) {
      $('.invalid-server').text(errMsg);
    },
  });
}

function cahtTo(userId) {
  // PUBLIC KEY
  if (userId === '0') {
    $('.receiver-name').html('Public Room');
    $('.chat-header-receiver').html('Public Room');
    $('.receiver-detail').html('');
  } else {
    const user = userList.find((user) => user.id == userId);
    $('.receiver-name').html(user.name);
    $('.chat-header-receiver').html(user.name);
    $('.receiver-detail').html(`
        <div class="receiver-item">
        Email: <br />
        <span>${user.email}</span>
        </div>
        <div class="receiver-item">
            Mobile Number: <br />
            <span>${user.mobileNumber}</span>
        </div>
        <div class="receiver-item">
            Joined in: <br />
            <span>${user.createAt}</span>
        </div>
    `);
  }

  if (window.currentConnected) {
    window.socket.emit('leave', {
      sender: window.userInfo.id,
      receiver: window.currentConnected,
    });
  }

  window.currentConnected = userId;
  window.socket.emit('join', {
    sender: window.userInfo.id,
    receiver: userId,
  });
}

function renderMessages(data) {
  let html = '';
  data.forEach((item) => {
    const isMe = item.sender.id === userInfo.id;
    html += `
    <p class="row ${isMe ? 'row-me' : 'row-other'}">
      <div class="author">
      <p>【${item.senderInfo.name}】<span>${item.createAt}</span><p>
      <p>
      ${item.content}
      </p>
      </div>
    </p>
    `;
  });
  $('.chat-body').html(html);

  // scroll to bottom
  $('.chat-body').animate(
    {
      scrollTop:
        $('.chat-body')[0].scrollHeight - $('.chat-body')[0].clientHeight,
    },
    100,
  );
}

function initWebSocket() {
  var socket = io();
  socket.on('connect', function () {});
  socket.on('message', function (payload) {
    console.log(payload);
    if (payload.type === 'chat_messages') {
      renderMessages(payload.data);
    }
  });
  window.socket = socket;
}

function addSendClickEvent() {
  $('#send').click(function () {
    var content = $('#textarea').val();
    if (window.currentConnected) {
      if (content) {
        // send message
        window.socket.emit('send', {
          sender: window.userInfo.id,
          receiver: window.currentConnected,
          content,
        });
        $('#textarea').val('');
      } else {
        $('.invalid-server').text('Please provide the message content');
      }
    } else {
      $('.invalid-server').text('Please select a room');
    }
  });
}

$(function () {
  initWebSocket();

  getUserInfo();
  getChatUsers();

  addSendClickEvent();
});
