$(document).ready(function () {
  $("#user").click(function (event) {
    event.preventDefault();
    $("#myDropdown").slideToggle();
  });


  $(document).click(function (event) { 
    if (!$(event.target).closest('#user').length) {
      $('#myDropdown').slideUp();
    }    
  });
});
