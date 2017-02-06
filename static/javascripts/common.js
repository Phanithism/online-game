$(document).ready(function () {

  var message = $('.notification-message').data('message');
  if (message) {
    Materialize.toast(message, 4000);
  }

});
