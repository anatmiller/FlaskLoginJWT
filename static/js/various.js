$(document).ready(function () {

  var isAuthenticated = false;

  $.ajax({
    url: "isAuthenticated", success: function (result) {
      if (result.isAuthenticated) {
        $("#active-users").removeClass('d-none');
        load_users();
        isAuthenticated = result.isAuthenticated
      }
      else {
        window.location.href = "/";
      }
    }, error: function(error) {
      if (error.status === 403){
         window.location.href = "/";
      }

    }
  });


  function load_users() {
    var email = $("#email").val();
    var pass = $("#password").val();
    $.ajax
    ({
      type: 'get',
      url: '/getActiveUsers',
      success: function (response) {
        console.log('got response', response);
        if (response.status === "Success") {
          var tbody = $('#active-users-tbl').find('tbody');
          $.each(response.users, function (i, user) {
            var tr = $('<tr>');
            $('<td>').html(user).appendTo(tr);
            tbody.append(tr);
          });
        }
        else {

        }
      },
      error: function (error) {
        console.log(error);
      }
    });
  }


});
