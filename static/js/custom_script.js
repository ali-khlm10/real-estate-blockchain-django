$(document).ready(function () {
  $("#user").click(function (event) {
    event.preventDefault(); // جلوگیری از انجام عملکرد پیش‌فرض لینک
    $("#myDropdown").slideToggle(); // باز کردن یا بستن دراپ‌دان
  });


  $(document).click(function (event) { 
    if (!$(event.target).closest('#user').length) {
      // اگر روی دکمه کلیک نشده بود، دراپ‌دان را ببند
      $('#myDropdown').slideUp();
    }    
  });
});
