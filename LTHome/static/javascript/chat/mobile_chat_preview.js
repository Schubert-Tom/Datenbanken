$(document).ready(function() {
    $("#expand_chats").click(function() {
        console.log("sadasdasdasd");
        $(".content_wrapper").toggleClass("show_all_chats");
        if ($(".show_all_chats").length > 0) {
            $(".all_chats_toggle span").text("Zurück zum Chat");
            // $("#chat").css("display", "none");
        } else {
            $(".all_chats_toggle span").text("Zu allen Chats");
            // $("#chat").css("display", "grid");
        }
    });


});