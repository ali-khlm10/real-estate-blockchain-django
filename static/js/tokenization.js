$(document).ready(function () {
  $(".start_tokenization").click(function (e) {
    e.preventDefault();
    var property_id = $(this).data("property_id");
    var currentPort = window.location.port;
    const currentURL = `http://127.0.0.1:${currentPort}/create_signature_to_tokenization/`;
    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    var data = {
      property_id: property_id,
    };
    var jsonData = JSON.stringify(data);

    $.ajax({
      type: "post",
      url: currentURL,
      data: jsonData,
      // headers: {
      //   "Content-Type": "application/json",
      //   "X-CSRFToken": csrftoken,
      // },
      dataType: "json",
      success: function (response) {
        if (response.status) {

        } else {
          console.log(response.message);
          
        }
      },
      error: function () {
        console.log("مشکل در ارتباط با سرور");
      },
    });
  });
});
