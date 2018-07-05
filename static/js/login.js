$(document).ready(function () {
  $(function () {
    $("input[type='password'][data-eye]").each(function (i) {
      var $this = $(this);

      $this.wrap($("<div/>", {
        style: 'position:relative'
      }));
      $this.css({
        paddingRight: 60
      });
      $this.after($("<div/>", {
        html: 'Show',
        class: 'btn btn-primary btn-sm',
        id: 'passeye-toggle-' + i,
        style: 'position:absolute;right:10px;top:50%;transform:translate(0,-50%);-webkit-transform:translate(0,-50%);-o-transform:translate(0,-50%);padding: 2px 7px;font-size:12px;cursor:pointer;'
      }));
      $this.after($("<input/>", {
        type: 'hidden',
        id: 'passeye-' + i
      }));
      $this.on("keyup paste", function () {
        $("#passeye-" + i).val($(this).val());
      });
      $("#passeye-toggle-" + i).on("click", function () {
        if ($this.hasClass("show")) {
          $this.attr('type', 'password');
          $this.removeClass("show");
          $(this).removeClass("btn-warning");
          $(this).text('Show');
          // $(this).removeClass("btn-outline-primary");
        } else {
          $this.attr('type', 'text');
          $this.val($("#passeye-" + i).val());
          $this.addClass("show");
          $(this).text('Hide');
          $(this).addClass("btn-warning");
          // $(this).addClass("btn-outline-primary");
        }
      });
    });
  });
  $("form").submit(function(e){
        e.preventDefault();
        do_login()
    });

  function do_login() {

    var email = $("#email").val();
    var pass = $("#password").val();
      $.ajax
      ({
        type: 'post',
        url: '/',
        data: {
          email: email,
          password: pass
        },
        success: function (response) {
          console.log('got response', response);
          if (response.status === "Success") {
            window.location.href = "/";
          }
          else {
            $("#login-btn").removeClass('disabled');
            alert("Wrong Details");
          }
        },
        error: function(error) {
          console.log(error);
          // $("#error").removeClass('d-none');
          $("#error").text(error.responseJSON.message).removeClass('d-none')
        }
      });
    }
});

