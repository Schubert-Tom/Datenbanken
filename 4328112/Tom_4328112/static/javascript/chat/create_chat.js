// Globales Array zum Sammeln von Teilnehmern für das Erstellen des Chats
var participants = [];
// Globale Variable zum Speichern ob beim Klick auf die Chat-Overview, diese neu geladen werden muss
// weil ein neuer Chat hinzugefügt wurde
var fetch_when_comeback = false;

$(document).ready(function() {
    //################### Sidebar ###################
    //Funktion lässt dynamische Aufteilung der sidebar zu.
    // Unterteilung in all_chats und create_new_chat
    // Auf Knopfdruck wird automatisch zum andern Zustand gewechselt
    $("#btn_new_Chat").click(function() {
        // Wechsel auf die create new chat view
        if ($("#create_new_chat").css("display") == "none") {
            $('#all_chats').css('display', 'none');
            $('#create_new_chat').css('display', 'block');
            $('#btn_new_Chat').html('-');
            return;
        }
        // Wechsel auf die all chats view
        if ($("#all_chats").css("display") == "none") {
            // Beim Abbrechen Error Messages ausblenden
            $(".error_add_user").css("display", "none");
            // Beim Abbrechen alle Textfelder leeren und hinzugefügte Benutzer löschen
            $(".js_made").remove();
            $("#participants").val("");
            $("#chat_name").val("");
            participants = [];
            // Umschalten der View
            $('#all_chats').css('display', 'block');
            $('#create_new_chat').css('display', 'none');
            $('#btn_new_Chat').html('+');
            // Wenn ein neuer Chat von einem anderen User ertsllt wurde muss beim zurückwechseln
            // Die Overview mit allen Chats neu geladen werden
            if (fetch_when_comeback == true) {
                $("#all_chats_wrapper").load("/chat #all_chats");
                fetch_when_comeback = false;
            }
            return;
        }
    });

    //################### Hinzugefügten User checken ###################
    // Dynamische Überprüfung der zum Chat hinzugefügten Benutzer:
    // Durch ein Fetch-Event wird eine asynchroner call an dern Server gemacht
    // und geprüft ob der Username in der Datenbank registriert ist 
    $("#btn_new_User").click(function(event) {
        // Benutzername aus dem Textfeld auslesen
        var user_to_verify = $("#participants").val();
        // Wenn nichts eingegeben wurde --> Funktion verlassen
        if (user_to_verify == "") {
            return;
        }
        // Wenn der User schon hinzugefügt wurde oder man sich selber hinzufügen will --> Funktion verlassen
        if (participants.indexOf(user_to_verify) >= 0 || user_to_verify == current_user) {
            // Für den User Error-Nachrichten einblenden
            $(".error_add_user").css("display", "block");
            $(".error_add_user").html("The User was already added");
            return;
        }
        // Erstellung eines Json Objekts zum Übermitteln welchen User man hinzufügen möchte
        var data = {
                user_to_verify: user_to_verify,
                valid: false,
            }
            //Fetch Befehl (asynchron) mit Fetch API (ajax wäre auch gegangen)
            //Aufbau eines HTTP-Requests
        fetch(`${window.origin}/chat/_validate_user`, {
                method: "POST",
                credentials: "include",
                body: JSON.stringify(data),
                cache: "no-cache",
                headers: new Headers({
                    "content-type": "application/json"
                })

            })
            // Wird ausgeführt nach Erhalt der Response
            .then(function(response) {
                // log falls Response Status nicht ok
                if (response.status != 200) {
                    console.log("Internal Server Error");
                    return;
                }
                response.json().then(function(data) {
                    // Nach Erhalt der Antwort
                    // wird ausgelesen ob der User valid is oder nicht
                    user = data["user_to_verify"];
                    // Wenn User nicht valid, dann Message Error zeigen
                    if (data["valid"] == false) {
                        $(".error_add_user").css("display", "block");
                        $(".error_add_user").html("The User doesn't exist");
                    }
                    // Wenn User  valid, dann neues Textfeld eröffnen und User hinzufügen
                    else {
                        // Error Message ausblenden
                        $(".error_add_user").css("display", "none");
                        // Label erstellen um akzeptierten User anzeigen
                        $("label[for='participants']").before("<label class='js_made'>Added User: " + data["user_to_verify"] + "</label><br class='js_made'>");
                        // Textfeld leeren
                        $("#participants").val("");
                        // Wenn die Person schon im participant Array steht wird sie nicht hinzugefügt
                        // If-Abfrage eigentlich unnötig aber nochmal zur Sicherheit
                        if (participants.indexOf(user) < 0) {
                            participants.push(user);
                        }
                    }
                })
            })
    });

    //################### Prevent Form.submit ###################
    // Damit beim Hinzufügen von Usern beim drücken der Enter Taste nicht der ganze Chat erstellt wird sondern nur der USer geprüft wird
    // wird dies hier verhindert:
    $('#participants').on('keyup keypress', function(e) {
        var keyCode = e.keyCode || e.which;
        // Wenn Enter Taste gedrückt wird
        if (keyCode === 13) {
            e.preventDefault();
            // Bestätigen des Textfelds durch manuelles drücken des Buttons
            $("#btn_new_User").click();
            return false;
        }
    });

    //################### Chat erstellen ###################
    // Der fertig erstellte Chat wird an den Server gesendet
    // Damit dieser den Chat in der Datenbank anlegen kann und die andern User informiern kann

    // Abschicken des Chats und löschen aller Eingaben und labels die im Laufe des Create_Chat-Prozess erstellt wurden
    $("#CreateChat").submit(function(event) {
        // Verhindern dass die Form normal abgeschickt wird
        event.preventDefault();
        var chat_name = $("#chat_name").val();
        console.log(chat_name);
        // Prüfen ob der Chat-Name die konform ist
        if (chat_name.length < 2 || chat_name.length > 15) {
            // Error-Feedback an den User
            $('.error_add_title').css('display', 'block');
            $('.error_add_title').val("Der Chat-Name darf mindestens 2 und maximal 15 zeichen beinhalten");
            return;
        }
        // Abschicken der Daten an den Namespace create_new_chat
        socket.emit("create_new_chat", {
            'chat_name': chat_name,
            'participants': participants
        });
        // löschen aller Eingaben und labels die im Laufe des Create_Chat-Prozess erstellt wurden
        $("#btn_new_Chat").click();
        $(".js_made").remove();
        $("#participants").val("");
        $("#chat_name").val("");
        $('.error_add_title').css('display', 'none');
        participants = [];
    });
    // Wenn Server antwortet--> Checken ob Chat createt wurde
    // Wenn ja Chat erstellen
    // Selbst wenn man nicht die Anfrage zum erstellen eines Chats geschickt hat kommen hier Informationen an
    // wenn ein anderer User einen Chat erstellt hat
    socket.on("create_new_chat", new_chat_data => {
        // Wenn ein Chat ertsellt wurde
        if (JSON.parse(new_chat_data)['new_chat_created'] == true) {
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