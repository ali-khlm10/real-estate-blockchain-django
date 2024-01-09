$(document).ready(function () {
  $("#sell_operation").click(function (e) {
    e.preventDefault();
    var token_id = $(this).data("token_id");
    var property_price = $(this).data("property_price");
    var prepayment = $(this).data("prepayment");
    var buyer_address = $(this).data("buyer_address");
    var buy_id = $(this).data("buy_operation_id");

    var currentPort = window.location.port;
    var createSignatureURL = `http://127.0.0.1:${currentPort}/create_signature_to_sell_operation/`;
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
          sell_operation(
            response,
            token_id,
            prepayment,
            property_price,
            buyer_address,
            buy_id,
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

  function sell_operation(
    response,
    token_id,
    prepayment,
    property_price,
    buyer_address,
    buy_id
  ) {
    var sell_operation_modal_element = document.getElementById(
      "sell_operation_modal"
    );
    var body_element = document.body;

    sell_operation_modal_element.style.display = "block";
    body_element.style.overflow = "hidden";

    sell_operation_modal_element.querySelector(
      "#sell_operation_token_id"
    ).innerHTML = token_id;

    sell_operation_modal_element.querySelector(
      "#sell_operation_buyer_address"
    ).innerHTML = buyer_address;

    sell_operation_modal_element.querySelector(
      "#sell_operation_transaction_fee"
    ).innerHTML = parseFloat(property_price) * 0.0005;

    $("#do_sell_operation")
      .off("click")
      .one("click", function (e) {
        e.preventDefault();
        console.log("java script");

        var sell_operation_modal_element = document.getElementById(
          "sell_operation_modal"
        );
        var body_element = document.body;
        var currentPort = window.location.port;
        var sellingURL = `http://127.0.0.1:${currentPort}/selling_operation/`;
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        var jsonData = JSON.stringify({
          signature: response.signature,
          sell_operation_information: response.sell_operation_information,
          transaction_fee: parseFloat(property_price) * 0.0005,
          buy_id: buy_id,
          remaining_cost: parseFloat(property_price) - parseFloat(prepayment),
        });
        // var jsonData = JSON.stringify(response);

        $.ajax({
          type: "post",
          url: sellingURL,
          data: jsonData,
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          dataType: "json",
          success: function (response) {
            if (response.status) {
              console.log(response.status);
              sell_operation_modal_element.style.display = "none";
              body_element.style.overflow = "auto";
              var sell_result_modal = document.getElementById(
                "sell_operation_result_modal"
              );
              sell_result_modal.style.display = "block";
              body_element.style.overflow = "hidden";
              sell_result_modal.querySelector("p").innerHTML = response.message;

              $(
                "#sell_operation_result_modal #ok_sell_operation_result,.internal_sell_operation_result_modal button"
              ).click(function (e) {
                e.preventDefault();
                sell_result_modal.style.display = "none";
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

    $("#dont_sell_operation,.internal_sell_operation_modal button")
      .off("click")
      .on("click", function (e) {
        e.preventDefault();
        console.log("dont");
        var sell_operation_modal_element = document.getElementById(
          "sell_operation_modal"
        );
        var body_element = document.body;
        sell_operation_modal_element.style.display = "none";
        body_element.style.overflow = "auto";
      });
  }
});
