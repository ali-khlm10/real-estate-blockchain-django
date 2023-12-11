$(document).ready(function () {
  $(".start_tokenization").click(function (e) {
    e.preventDefault();
    var property_id = $(this).data("property_id");
    var currentPort = window.location.port;
    const currentURL = `http://127.0.0.1:${currentPort}/create_property_sign/`;
    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    var data = {
      property_id: property_id,
    };
    var jsonData = JSON.stringify(data);

    $.ajax({
      type: "post",
      url: currentURL,
      data: jsonData,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      dataType: "json",
      success: function (response) {
        console.log(response);
      },
      error: function () {
        console.log("مشکل در ارتباط با سرور");
      },
    });
  });
});
