$(document).ready(function () {
  $(document).on("click", ".delete_chat", function () {
    // Der Mauszeiger ist jetzt nicht mehr over_delete weil das Objekt weg ist
    over_delete = false;
    // Verhindern dass die Form normal abgeschickt wird
    var chat_id = $(this).attr("id").split("/")[1];
    console.log(chat_id);
    // Prüfen ob der Chat-Name die konform ist
    // Abschicken der Daten an den Namespace create_new_chat
    socket.emit("delete_chat", {
      chat_id: chat_id,
    });
  });
  socket.on("delete_chat", (rsp_data) => {
    $("#startscreen").css("display", "flex");
    $("#chat").css("display", "none");
    // Wenn ein Chat ertsellt wurde
    if (JSON.parse(rsp_data)["chat_left"] == true) {
      // Checken in welcher Anzeige man sich befindet
      if ($("#all_chats").css("display") == "none") {
        // Wenn man gerade selber einen Chat erstellt
        // Soll beim Wechseln auf die Overview diese neu vom Server geladen werden
        fetch_when_comeback = true;
      } else {
        // Chat Overview neu laden vom Server mittels jquery load
        $("#all_chats_wrapper").load("/chat #all_chats");
      }
    }
  });
});
