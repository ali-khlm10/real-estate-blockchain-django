$(document).ready(function () {
  $(".start_tokenization").click(function (e) {
    e.preventDefault();
    var property_id = $(this).data("property_id");
    var property_title = $(this).data("property_title");
    var property_price = $(this).data("property_price");

    var currentPort = window.location.port;
    var createSignatureURL = `http://127.0.0.1:${currentPort}/create_signature_to_tokenization/`;
    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    var data = {
      property_id: property_id,
    };
    var jsonData = JSON.stringify(data);

    $.ajax({
      type: "post",
      url: createSignatureURL,
      data: jsonData,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      dataType: "json",
      success: function (response) {
        if (response.status) {
          tokenization(response, property_id, property_title, property_price);
        } else {
          console.log(response.message);
        }
      },
      error: function () {
        console.log("مشکل در ارتباط با سرور");
      },
    });
  });

  function tokenization(response, property_id, property_title, property_price) {
    var currentPort = window.location.port;
    var tokenizationURL = `http://127.0.0.1:${currentPort}/tokenization/`;
    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    var jsonData = JSON.stringify({
      signature: response.signature,
      property_information: response.property_information,
    });
    // var jsonData = JSON.stringify(response);

    var tokenization_modal_element = document.getElementById("tokenization_modal");
    var body_element = document.body;
    tokenization_modal_element.style.display = "block";
    body_element.style.overflow = "hidden";
    tokenization_modal_element.querySelector("#property_number").innerHTML = property_id;
    tokenization_modal_element.querySelector("#property_title").innerHTML = property_title;
    tokenization_modal_element.querySelector("#property_price").innerHTML = property_price;

    $("#tokenization_modal #dont_tokenization,.internal_modal button").click(function (e) {
      e.preventDefault();
      tokenization_modal_element.style.display = "none";
      body_element.style.overflow = "auto";
    });

    $("#tokenization_modal #do_tokenization").click(function (e) {
      e.preventDefault();
      $.ajax({
        type: "post",
        url: tokenizationURL,
        data: jsonData,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        dataType: "json",
        success: function (response) {
          console.log(response);
          tokenization_modal_element.style.display = "none";
          body_element.style.overflow = "auto";
          window.location.reload();
        },
        error: function () {
          console.log("مشکل در ارتباط با سرور");
        },
      });
    });
  }
});
