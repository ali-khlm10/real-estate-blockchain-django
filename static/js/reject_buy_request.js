$(document).ready(function () {
  $("#reject_buy_request").click(function (e) {
    e.preventDefault();
    var token_id = $(this).data("token_id");
    var buyer_address = $(this).data("buyer_address");
    var prepayment = $(this).data("prepayment");
    var property_price = $(this).data("property_price");

    var currentPort = window.location.port;
    var createSignatureURL = `http://127.0.0.1:${currentPort}/create_signature_to_accept_reject_buy_request/`;
    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

    var data = {
      token_id: token_id,
      buyer_address: buyer_address,
      operation: "rejecting",
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
          reject_buy_request(
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

  function reject_buy_request(
    response,
    buyer_address,
    token_id,
    property_price,
    prepayment
  ) {
    var reject_buy_request_modal_element = document.getElementById(
      "rejecting_buy_request_modal"
    );
    var body_element = document.body;

    reject_buy_request_modal_element.style.display = "block";
    body_element.style.overflow = "hidden";

    reject_buy_request_modal_element.querySelector(
      "#buy_request_buyer"
    ).innerHTML = buyer_address;
    reject_buy_request_modal_element.querySelector(
      "#buy_request_buyer_transaction_fee"
    ).innerHTML = parseFloat(property_price) * 0.000005;
    reject_buy_request_modal_element.querySelector(
      "#buy_request_buyer_prepayment"
    ).innerHTML = prepayment;

    $(
      "#rejecting_buy_request_modal #dont_reject_buy_request, .internal_reject_buy_request_modal button"
    )
      .off("click")
      .on("click", function (e) {
        e.preventDefault();

        console.log("dont");

        var reject_buy_request_modal_element = document.getElementById(
          "rejecting_buy_request_modal"
        );
        var body_element = document.body;

        reject_buy_request_modal_element.style.display = "none";
        body_element.style.overflow = "auto";
      });

    $("#rejecting_buy_request_modal #do_reject_buy_request")
      .off("click")
      .one("click", function (e) {
        e.preventDefault();
        console.log("rejected_buy_request");

        $(this).addClass("loading");

        var currentPort = window.location.port;
        var reject_buy_requestURL = `http://127.0.0.1:${currentPort}/rejecting_buy_request/`;
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        var jsonData = JSON.stringify({
          signature: response.signature,
          accept_reject_buy_request_information:
            response.accept_reject_buy_request_information,
          transaction_fee: parseFloat(property_price) * 0.000005,
          prepayment: prepayment,
        });

        var reject_buy_request_modal_element = document.getElementById(
          "rejecting_buy_request_modal"
        );
        var body_element = document.body;

        $.ajax({
          type: "post",
          url: reject_buy_requestURL,
          data: jsonData,
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          dataType: "json",
          success: function (response) {
            if (response.status) {
              console.log(response.status);
              reject_buy_request_modal_element.style.display = "none";
              body_element.style.overflow = "auto";
              var reject_buy_request_result_modal_element =
                document.getElementById("rejecting_buy_reqiest_result_modal");
              reject_buy_request_result_modal_element.style.display = "block";
              body_element.style.overflow = "hidden";
              reject_buy_request_result_modal_element.querySelector(
                "p"
              ).innerHTML = response.message;

              $(
                "#rejecting_buy_reqiest_result_modal #ok_reject_buy_request_result,.internal_reject_buy_request_result_modal button"
              ).click(function (e) {
                e.preventDefault();
                reject_buy_request_result_modal_element.style.display = "none";
                body_element.style.overflow = "auto";
                window.location.reload();
              });
            } else {
              console.log(response.message);
            }
            $("#do_reject_buy_request").removeClass("loading");
          },
          error: function () {
            console.log("مشکل در ارتباط با سرور");

            $("#do_reject_buy_request").removeClass("loading");
          },
        });
      });
  }
});
