$(document).ready(function () {
  $("#start_buy_request").click(function (e) {
    e.preventDefault();

    var token_id = $(this).data("token_id");
    var property_title = $(this).data("property_title");
    var property_price = $(this).data("property_price");

    var currentPort = window.location.port;
    var createSignatureURL = `http://127.0.0.1:${currentPort}/create_signature_to_buy_request/`;
    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    var data = {
      token_id: token_id,
    };
    var jsonData = JSON.stringify(data);

    prepayment_amount().then(function (result) {
      if (result.status) {
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
              buying_request(
                response,
                token_id,
                property_title,
                property_price,
                result.prepayment
              );
              // console.log(response.signature);
            } else {
              console.log(response.message);
            }
          },
          error: function () {
            console.log("مشکل در ارتباط با سرور");
          },
        });
      }
    });
  });

  function prepayment_amount() {
    return new Promise(function (resolve) {
      $("#prepayment").val("");
      var prepayment_modal_element = document.getElementById(
        "buy_request_prepayment_modal"
      );
      var body_element = document.body;
      prepayment_modal_element.style.display = "block";
      body_element.style.overflow = "hidden";

      $(
        "#buy_request_prepayment_modal #dont_prepayment,.internal_buy_request_prepayment_modal button"
      )
        .off("click")
        .on("click", function (e) {
          e.preventDefault();
          console.log("dont_payment");
          prepayment_modal_element.style.display = "none";
          body_element.style.overflow = "auto";
          var result = {
            status: false,
          };

          resolve(result);
        });

      $("#buy_request_prepayment_modal #do_prepayment")
        .off("click")
        .one("click", function (e) {
          e.preventDefault();
          console.log("do_payment");

          prepayment_element_input = $("#prepayment").val();
          if (prepayment_element_input !== "") {
            prepayment = prepayment_element_input;
            prepayment_modal_element.style.display = "none";
            body_element.style.overflow = "auto";
            var result = {
              status: true,
              prepayment: prepayment,
            };

            resolve(result);
          }
        });
    });
  }

  function buying_request(
    response,
    token_id,
    property_title,
    property_price,
    prepayment
  ) {
    // var jsonData = JSON.stringify(response);

    var buying_request_modal_element = document.getElementById(
      "buy_request_token_modal"
    );
    var body_element = document.body;

    buying_request_modal_element.style.display = "block";
    body_element.style.overflow = "hidden";

    buying_request_modal_element.querySelector("#token_number").innerHTML =
      token_id;
    buying_request_modal_element.querySelector(
      "#buy_request_property_title"
    ).innerHTML = property_title;
    buying_request_modal_element.querySelector(
      "#buy_request_property_price"
    ).innerHTML = property_price;
    buying_request_modal_element.querySelector(
      "#buy_request_transaction_fee"
    ).innerHTML = parseFloat(property_price) * 0.000005;

    buying_request_modal_element.querySelector(
      "#buy_request_transaction_prepayment"
    ).innerHTML = parseFloat(prepayment);

    $("#buy_request_token_modal #do_buy_request")
      .off("click")
      .one("click", function (e) {
        e.preventDefault();
        console.log("java script");

        $(this).addClass("loading");


        var buying_request_modal_element = document.getElementById(
          "buy_request_token_modal"
        );
        var body_element = document.body;

        var currentPort = window.location.port;
        var buying_request_URL = `http://127.0.0.1:${currentPort}/buying_request/`;
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        var jsonData = JSON.stringify({
          signature: response.signature,
          buy_request_information: response.buy_request_information,
          transaction_fee: parseFloat(property_price) * 0.000005,
          prepayment: prepayment,
        });

        $.ajax({
          type: "post",
          url: buying_request_URL,
          data: jsonData,
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          dataType: "json",
          success: function (response) {
            if (response.status) {
              console.log(response.status);
              buying_request_modal_element.style.display = "none";
              body_element.style.overflow = "auto";
              var buying_request_result_modal_element = document.getElementById(
                "buying_request_result_modal"
              );
              buying_request_result_modal_element.style.display = "block";
              body_element.style.overflow = "hidden";
              buying_request_result_modal_element.querySelector("p").innerHTML =
                response.message;

              $(
                "#buying_request_result_modal #ok_buy_requestـresult,.internal_buy_request_result_modal button"
              ).click(function (e) {
                e.preventDefault();
                buying_request_result_modal_element.style.display = "none";
                body_element.style.overflow = "auto";
                window.location.reload();
              });
            } else {
              console.log(response.message);
            }
            $("#do_buy_request").removeClass("loading");

          },
          error: function () {
            console.log("مشکل در ارتباط با سرور");
            $("#do_buy_request").removeClass("loading");

          },
        });
      });

    $(
      "#buy_request_token_modal #dont_buy_request,.internal_buy_request_modal button"
    )
      .off("click")
      .on("click", function (e) {
        e.preventDefault();
        console.log("dont");

        var buying_request_modal_element = document.getElementById(
          "buy_request_token_modal"
        );
        var body_element = document.body;

        buying_request_modal_element.style.display = "none";
        body_element.style.overflow = "auto";
      });
  }
});
