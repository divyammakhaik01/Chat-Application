document.addEventListener("DOMContentLoaded", () => {
  var socket = io();

  // Recieve messages
  socket.on("message", (data) => {
    // if message  recieved is of curr user's
    var index = 0;
    if (data["time_stamp"]) {
      if (data["username"] === username) {
        var p = document.createElement("p");
        var span_name = document.createElement("span");
        var span_time = document.createElement("span");
        var span_message = document.createElement("span");
        var br = document.createElement("br");
        var div = document.createElement("div");

        div.className = " d-block text-end py-1";

        p.className = "my-chat1 d-inline-block rounded-start px-2";
        span_time.className = "fw-light text-white";
        span_name.className = "fw-bold";
        span_message.className = "message  fw-normal text-white";

        span_name.innerHTML = data.username;
        span_time.innerHTML = data.time_stamp;
        span_message.innerHTML = data.message;

        span_time.style = "font-size:10px;";
        p.style = "background-color:rgb(74, 166, 228);";

        p.setAttribute("tabIndex", index);
        p.innerHTML =
          br.outerHTML +
          span_message.outerHTML +
          br.outerHTML +
          span_time.outerHTML +
          br.outerHTML;
        div.appendChild(p);
        document.querySelector("#display-section").appendChild(div);
        p.focus();
        ++index;
      } else {
        var p = document.createElement("p");
        var span_name = document.createElement("span");
        var div = document.createElement("div");
        var span_time = document.createElement("span");
        var span_message = document.createElement("span");
        var br = document.createElement("br");

        span_time.className = "fw-light text-white";
        p.className = "other-chat1 d-inline-block rounded-bottom px-2";
        span_message.className = "message  fw-normal text-white";
        span_name.className = "fw-bold";
        div.className = "d-block text-start py-1";

        span_name.innerHTML = data.username;
        span_time.innerHTML = data.time_stamp;
        span_message.innerHTML = data.message;

        span_time.style = "font-size: 10px;";
        p.style = "background-color: rgba(157, 161, 163, 0.945);";
        span_time.style = "font-size:10px;";

        p.setAttribute("tabIndex", index);

        p.innerHTML =
          span_name.outerHTML +
          br.outerHTML +
          span_message.outerHTML +
          br.outerHTML +
          span_time.outerHTML;
        div.appendChild(p);
        document.querySelector("#display-section").appendChild(div);
        p.focus();
        ++index;
      }
    }
    // if joining/leaving room  message is recieved
    else {
      if (data["username"] !== username) {
        var p = document.createElement("p");
        var br = document.createElement("br");
        var div = document.createElement("div");
        div.className = "d-block text-start py-1";
        p.style = "background-color: rgba(157, 161, 163, 0.945);";

        p.className = " d-inline-block badge bg-info text-white ";

        p.setAttribute("tabIndex", index);
        p.innerHTML = br.outerHTML + data["message"] + br.outerHTML;
        div.appendChild(p);
        document.querySelector("#display-section").appendChild(div);
        p.focus();
        ++index;
      }
    }
  });

  // Sending  Message
  // --------------------------------------------------------------------------------
  document.getElementById("send_message").onclick = () => {
    var mes = document.querySelector("#user_message").value;
    document.querySelector("#user_message").value = "";
    socket.send({ message: mes, username: username, room: roomName });
  };

  document.getElementById("user_message").addEventListener("keyup", (event) => {
    console.log(" : : ", event.keyCode);
    var mes = document.querySelector("#user_message").value;
    if (event.keyCode === 13 && mes != "") {
      document.querySelector("#user_message").value = "";
      socket.send({ message: mes, username: username, room: roomName });
    }
  });
  // --------------------------------------------------------------------------------

  // Joining room

  function JoinRoom() {
    socket.emit("join", { username: username, room: roomName });
  }

  JoinRoom();

  // --------------------------------------------------------------------------------

  // Leaving Room

  document.querySelector(".room-click").onclick = () => {
    socket.emit("leave", { username: username, room: roomName });
  };

  document.getElementById("logout-now").onclick = () => {
    socket.emit("leave", { username: username, room: roomName });
  };
  document.getElementById("chat-clicked").onclick = () => {
    socket.emit("leave", { username: username, room: roomName });
  };
  // --------------------------------------------------------------------------------
});

// Search bar
window.onload = function () {
  document.getElementById("input-val").addEventListener("keyup", () => {
    var x = document.getElementById("input-val").value.toUpperCase();

    var rooms_length = document.getElementsByClassName("inside-room4");

    for (var i = 0; i < rooms_length.length; i++) {
      var y = document
        .getElementsByClassName("inside-room4")
        [i].innerHTML.toUpperCase();
      var roomSelect = document
        .getElementsByClassName("tar")
        [i].getElementsByClassName("tar1")[0]
        .getElementsByClassName("inside-room4")[0]
        .innerHTML.toUpperCase();

      if (roomSelect.indexOf(x) > -1) {
        document.getElementsByClassName("tar")[i].style.display = "";
      } else {
        document.getElementsByClassName("tar")[i].style.display = "none";
      }
    }
  });
};
// --------------------------------------------------------------------------------
