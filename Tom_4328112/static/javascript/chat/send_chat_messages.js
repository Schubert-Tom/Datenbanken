$(document).ready(function() {
    var audio = new Audio("static/sounds/notification_sound.mp3");
    audio.volume = 0.2;
    //################### Nachrichten senden ###################
    // Nachrichten können gesendet werden. Diese werden an den Server geschickt
    // und von dort aus an alle versendet die online sind und in die Datenbank geschrieben


    // Nachrichten werden aus der Textbox ausgelesen und versendet
    $("#send").click(function(event) {
        // Auslesen der Textbox
        var message = $("#msg_write").val();
        var room = $(".all_messages").attr('id');
        // Wenn Nachricht leer ist oder wenn kein Room ausgewählt ist
        // Zum Beispiel Start screen kann auch keine Nahricht gesendet werden
        // Weil die id=-1 ist
        if (message == "" || room < 0) {
            event.preventDefault();
            return;
        }
        // Nachricht versenden an namespace chat_message
        socket.emit('chat_message', {
            'msg': message,
            'room': room
        });
        // Textfeld leeren
        $("#msg_write").val("");
        //Textfeld wieder fokusieren damit man schnell schreiben kann
        $("#msg_write").focus();
        // Verhindern dass Form abgeschickt wird
        event.preventDefault();
    });

    // Wenn der Server antwortet
    // Empfangene Nachricht rendern mit render Funktion
    socket.on("chat_message", msg => {
        // ID des chats der geschickt wird
        var chat_room_id = JSON.parse(msg)["chat"];
        // Id des Chats laden, der gerade angezeigt wird
        var id = $(".all_messages").attr('id');
        render_Chat_message(JSON.parse(msg), false);
        if (JSON.parse(msg)["user_name"] != current_user && id != chat_room_id) {
            audio.play();
        }


    });

});