$(document).ready(function () {
  $("#buy_operation").click(function (e) {
    e.preventDefault();
    var token_id = $(this).data("token_id");
    var property_price = $(this).data("property_price");
    var buy_request_prepayment = $(this).data("buy_request_prepayment");
    var accepted_buy_request = $(this).data("accepted_buy_request");

    var currentPort = window.location.port;
    var createSignatureURL = `http://127.0.0.1:${currentPort}/create_signature_to_buy_operation/`;
    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    var data = {
      token_id: token_id,
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
          buy_operation(
            response,
            token_id,
            buy_request_prepayment,
            property_price,
            accepted_buy_request
          );
          console.log(response);
        } else {
          console.log(response.message);
        }
      },
      error: function () {
        console.log("مشکل در ارتباط با سرور");
      },
    });
  });

  function buy_operation(
    response,
    token_id,
    buy_request_prepayment,
    property_price,
    accepted_buy_request,
  ) {
    var buy_operation_modal_element = document.getElementById(
      "buy_operation_modal"
    );
    var body_element = document.body;

    buy_operation_modal_element.style.display = "block";
    body_element.style.overflow = "hidden";

    buy_operation_modal_element.querySelector(
      "#buy_operation_token_id"
    ).innerHTML = token_id;

    buy_operation_modal_element.querySelector(
      "#buy_operation_property_price"
    ).innerHTML =
      parseFloat(property_price) - parseFloat(buy_request_prepayment);

    buy_operation_modal_element.querySelector(
      "#buy_operation_transaction_fee"
    ).innerHTML = parseFloat(property_price) * 0.00005;

    $("#do_buy_operation")
      .off("click")
      .one("click", function (e) {
        e.preventDefault();
        console.log("started buy operation");

        $(this).addClass("loading");


        var buy_operation_modal_element = document.getElementById(
          "buy_operation_modal"
        );
        var body_element = document.body;
        var currentPort = window.location.port;
        var buyingURL = `http://127.0.0.1:${currentPort}/buying_operation/`;
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        var jsonData = JSON.stringify({
          signature: response.signature,
          buy_operation_information: response.buy_operation_information,
          transaction_fee: parseFloat(property_price) * 0.00005,
          remaining_cost:
            parseFloat(property_price) - parseFloat(buy_request_prepayment),
            accepted_buy_request : accepted_buy_request,
        });
        // var jsonData = JSON.stringify(response);

        $.ajax({
          type: "post",
          url: buyingURL,
          data: jsonData,
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          dataType: "json",
          success: function (response) {
            if (response.status) {
              console.log(response.status);
              buy_operation_modal_element.style.display = "none";
              body_element.style.overflow = "auto";
              var buy_result_modal = document.getElementById(
                "buy_operation_result_modal"
              );
              buy_result_modal.style.display = "block";
              body_element.style.overflow = "hidden";
              buy_result_modal.querySelector("p").innerHTML = response.message;

              $(
                "#buy_operation_result_modal #ok_buy_operation_result,.internal_buy_operation_result_modal button"
              ).click(function (e) {
                e.preventDefault();
                buy_result_modal.style.display = "none";
                body_element.style.overflow = "auto";
                window.location.reload();
              });
            } else {
              console.log(response.message);
            }

            $("#do_buy_operation").removeClass("loading");


          },
          error: function () {
            console.log("مشکل در ارتباط با سرور");

            $("#do_buy_operation").removeClass("loading");

          },
        });
      });

    $("#dont_buy_operation,.internal_buy_operation_modal button")
      .off("click")
      .on("click", function (e) {
        e.preventDefault();
        console.log("dont");
        var buy_operation_modal_element = document.getElementById(
          "buy_operation_modal"
        );
        var body_element = document.body;
        buy_operation_modal_element.style.display = "none";
        body_element.style.overflow = "auto";
      });
  }
});
