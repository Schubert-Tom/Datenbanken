// Wie viele Nachrichten wurden schon aus der Datenbank nachgeladen
var msg_already_loaded = 0;
// Intialisieren des Scroll-Wertes k bei dem neue Nachrichten dynamisch aus der Datenban nachgeladen werden sollen
var k = -1000;
//over delete
over_delete = false;
$(document).ready(function() {
    // Check if cursor is over delete button
    ($(".delete_chat").mouseover(function() {
        over_delete = true;
        console.log("over_delete: " + over_delete)
    }));
    ($(".delete_chat").mouseleave(function() {
        over_delete = false;
        console.log("over_delete: " + over_delete)
    }));



    //################### Chat-Auswahl ###################
    //Funktion lädt beim klicken auf einen neuen Chat die ersten 40 Nachrichten vom Server
    // Aufgrund des dynamischen Hinzufügens von ".chat_preview" Elementen
    // wird hier Event-Delegation eingesetzt damit der click auf dynamisch erzeugte DOM-Elemente auch ausgeführt werden kann
    $(document).on("click", '.chat_preview', function() {
        // Es wird geprüft ob der Klick auf einen neuen Chat oder auf den aktuell gefocusten Chat gemacht wird
        // Falls es der bereits angezeigte Chat ist, muss nichts gemacht werden --> return
        var chat_id = this.id;
        // Schauen ob ein neuer Chat angeklickt wurde oder der alte
        var current_chat_id = $(".all_messages").attr('id');
        //wenn hover über Mülltonne dann nichtmehr load_Chat
        if (over_delete) {
            return;
        }
        console.log("geht das");
        // Wenn Media-Query unter 750px dann bei cklick show_all_chats löschen
        if (window.matchMedia("(max-width: 750px)").matches) {
            $(".content_wrapper").removeClass("show_all_chats");
        } else {
            if (chat_id == current_chat_id) {
                return;
            }
        }
        // Von neuen Chat den Titel setzen
        var chat_title = $(this).find("h3");
        $("#chat_title").html(chat_title.html());
        // Von neuen Chat die Teilnehmerliste setzen
        var teilnehmerliste = $(this).find("span");
        $("#chat_info_bar_participants").empty();
        teilnehmerliste.each(function() {
            var teilnehmer = $(this).html();
            $("#chat_info_bar_participants").append(teilnehmer);
        });
        // Den Nachlade-Scroll-Wert auf -1000 setzen, bei dem neuen Chat
        k = -1000;
        // Den schon nachgeladene-Message-Wert auf 0 setzen, bei dem neuen Chat
        msg_already_loaded = 0;
        // Die Chat Id des neuen Chats in HTML schreiben
        $(".all_messages").attr('id', chat_id);
        // Die Chat-Nachrichten aus dem alten Chat nicht mehr anzeigen (HTML Elemnte löschen)
        $(".all_messages").empty();
        // Das Json Objekt erstellen, was an den Server gesendet wird
        // Damit dieser weiß welche Nachrichten ab wo zurückgeschickt werden sollen
        data = {
            'chat_id': chat_id,
            'msg_already_loaded': msg_already_loaded
        };
        // Anfrage an Server nach Nachrichten
        reload_messages_from_database(data);
    });


    //################### Infinite Chat-Scrolling ###################
    //Dynamisches nachladen von Nachrichten. Der Chat lädt dynamisch Nachrichten vom Server nach wenn
    // der Benutzer weit nach oben scrollt --> Infinite Scrolling
    $(".all_messages").scroll(function() {
        //Wenn nach unten gescrollt wird wird die Scrollbar auf 0 gesetzt damit
        // neue Nachrichten die live gesendet werden direkt angezeigt werden und der Chat sich direkt an den Nachrichten flow anhängt
        // Wenn jedoch nach oben gescrollt wird um alte Nachrichten zu lesen werden Nachrichten unten angefügt
        // ohne dass es denjenigen der gerade Nachrichten liest wieder nach unten zieht und somit stört.
        var top = $(this).scrollTop();
        if (top > -8) {
            $(this).scrollTop(0);
        }
        // Wenn man weit nach oben scrollt sollen alte Nachrichten nachgeladen werden
        if (top < k) {
            // Den Scroll-Wert wieder um 1000 veringern damit die nächsten 40 Nachrichten nach diesen 40 
            //Nachrichten wieder nach weiterem Scrollen nach oben nachgeladen werden können geladen werden
            k = k - 1000;
            // Das Json Objekt erstellen, was an den Server gesendet wird
            // Damit dieser weiß welche Nachrichten ab wo zurückgeschickt werden sollen
            var chat_id = $(".all_messages").attr("id");
            var data = {
                'chat_id': chat_id,
                'msg_already_loaded': msg_already_loaded
            };
            // Anfrage an Server nach Nachrichten
            reload_messages_from_database(data);
        }
    });

    //################### Nachladen von Nachrichten ###################
    //Funktion lädt die gewünschten Nachrichten vom Server und ruft danach die render Funktion aus dem "chat.html" file auf
    function reload_messages_from_database(data) {
        //Fetch Befehl (asynchron) mit Fetch API (ajax wäre auch gegangen)
        //Aufbau eines HTTP-Requests
        fetch(`${window.origin}/chat/_get_messages`, {
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
                    console.log("Error")
                    return;
                }
                response.json().then(function(data) {
                    // Startscreen entfernen falls er da ist*/
                    if ($("#startscreen").length) {
                        $("#startscreen").css("display", "none");
                        $("#chat").css("display", "grid");
                    }
                    // Nach Erhalt der Antwort
                    // wird ausgelesen ob überhaupt Nachrichten geladen wurden
                    // Wenn man zum beispiel an den Start des Chats scrollt werden keine Nachrichten nachgeladen
                    if (data["status"] == false) {
                        return;
                    }
                    // Wenn User  Nachrichten geladen wurden:
                    else {
                        // Response entpacken
                        var messages = data["messages"];
                        // msg_already_loaded erhöhen um die geladenen Nachrichten
                        msg_already_loaded += messages.length;
                        // Jede  Nachricht gespiegelt oben anhängen
                        messages.reverse().forEach(
                            function(message) {
                                render_Chat_message(message, true);
                            });
                    }
                });
            });
    }




});