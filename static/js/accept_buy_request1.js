$(document).ready(function () {
  $("#accept_buy_request").click(function (e) {
    e.preventDefault();
    console.log("hello");
    var token_id = $(this).data("token_id");
    var buyer_address = $(this).data("buyer_address");
    var prepayment = $(this).data("prepayment");
    var property_price = $(this).data("property_price");

    var currentPort = window.location.port;
    var createSignatureURL = `http://127.0.0.1:${currentPort}/create_signature_to_accept_buy_request/`;
    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    var data = {
      token_id: token_id,
      buyer_address: buyer_address,
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
          accept_buy_request(
            response,
            buyer_address,
            token_id,
            property_price,
            prepayment
          );
          console.log(response.signature);
        } else {
          console.log(response.message);
        }
      },
      error: function () {
        console.log("مشکل در ارتباط با سرور");
      },
    });
  });

  function accept_buy_request(
    response,
    buyer_address,
    token_id,
    property_price,
    prepayment
  ) {
    var currentPort = window.location.port;
    var accept_buy_requestURL = `http://127.0.0.1:${currentPort}/accepting_buy_request/`;
    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    var jsonData = JSON.stringify({
      signature: response.signature,
      accept_buy_request_information: response.accept_buy_request_information,
      transaction_fee: parseFloat(property_price) * 0.0005,
    });
    // var jsonData = JSON.stringify(response);

    var accept_buy_request_modal_element = document.getElementById(
      "accepting_buy_request_modal"
    );
    var body_element = document.body;
    accept_buy_request_modal_element.style.display = "block";
    body_element.style.overflow = "hidden";
    accept_buy_request_modal_element.querySelector(
      "#buy_request_buyer"
    ).innerHTML = buyer_address;
    accept_buy_request_modal_element.querySelector(
      "#buy_request_buyer_transaction_fee"
    ).innerHTML = parseFloat(property_price) * 0.0005;
    accept_buy_request_modal_element.querySelector(
      "#buy_request_buyer_prepayment"
    ).innerHTML = prepayment;

    $(
      "#accepting_buy_request_modal #do_reject_buy_request,.internal_accept_buy_request_modal button"
    ).click(function (e) {
      e.preventDefault();
      accept_buy_request_modal_element.style.display = "none";
      body_element.style.overflow = "auto";
    });

    $("#accepting_buy_request_modal #do_accept_buy_request").click(function (
      e
    ) {
      e.preventDefault();
      $.ajax({
        type: "post",
        url: accept_buy_requestURL,
        data: jsonData,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        dataType: "json",
        success: function (response) {
          if (response.status) {
            console.log(response.status);
            accept_buy_request_modal_element.style.display = "none";
            body_element.style.overflow = "auto";
            var accept_buy_request_result_modal_element =
              document.getElementById("accepting_buy_reqiest_result_modal");
            accept_buy_request_result_modal_element.style.display = "block";
            body_element.style.overflow = "hidden";
            accept_buy_request_result_modal_element.querySelector(
              "p"
            ).innerHTML = response.message;

            $(
              "#accepting_buy_reqiest_result_modal #ok_accept_buy_request_result,.internal_accept_buy_request_result_modal button"
            ).click(function (e) {
              e.preventDefault();
              accept_buy_request_result_modal_element.style.display = "none";
              body_element.style.overflow = "auto";
              window.location.reload();
            });
          } else {
            console.log(response.message);
          }
        },
        error: function () {
          console.log("مشکل در ارتباط با سرور");
        },
      });
    });
  }
});
