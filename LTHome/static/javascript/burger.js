$(document).ready(function() {
    $(".burger").click(function() {
        $(".dropdown").toggleClass("visible");
        $("body").toggleClass("expanded");
    })

});