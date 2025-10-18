const socket = io();

document.getElementById('go_button').addEventListener('click', () => {
    socket.emit('Go_button_pushed');
  });