import functools, json
from flask import render_template, flash, redirect, url_for, request, make_response, jsonify
from Tom_4328112.db_models import User, Chat, Message
from Tom_4328112.forms import RegistrationForm, LoginForm, CreateChat
from Tom_4328112 import app, db, bcrypt, socketio
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import send, emit, disconnect, join_room, leave_room

# Route für die Index-Seite
@app.route('/')
def index():
    return render_template("index.html", title="Main")

# Route für den Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Wenn der User schon eingeloggt ist, dann nichts machen
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # form definieren für den LogIN
    form = LoginForm()
    # Wenn die Flask-Wtf Form bestätigt wird:
    if form.validate_on_submit():
        # Schauen ob der User in der Datenbank zu finden ist
        user = User.query.filter_by(username=form.username.data).first()
        # checkt ob User existiert und ob das Passwort stimmt.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # ruft Log_In Funktion auf erstellt einen cookie für eine Session
            login_user(user, remember=False)
            # bget method because if normal dictionary acces ther would e an error if it woluld be null
            next_page = request.args.get("next")
            flash(f'Welcome {user.username}!', 'succes')
            # Special ternary conditional
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            #Flash Message gibt fedback
            flash(f'Wrong Password or Username!', 'fail')
    return render_template("login.html", title="Log In", form=form)

# Route zum erstellen eines Accounts
@app.route('/createAccount', methods=['GET', 'POST'])
def register():
    # Wenn der User schon eingeloggt ist, dann nichts machen
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Form definiern die bei der Registrierung verwendet wird
    form = RegistrationForm()
    # Wenn Form bestätigt wurde auf Register Page:
    if form.validate_on_submit():
        # Passwort hashen
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        # Datenbank Daten adden und commiten
        db.session.add(user)
        db.session.commit()
        # The Css for the flash message depending on weater it is an alert or a confirm...
        flash(f'Account created for {form.username.data}!', 'succes')
        return redirect(url_for("login"))
    return render_template("register.html", title="Create an Account", form=form)


#####################################################################
# Route für den Logout (Hat kein Template)
@app.route('/logout')
def logout():
    logout_user()
    flash(f'Successful logout!', 'succes')
    return redirect(url_for("index"))

#Route für die Kontakt (Matrikelnummer)
@app.route('/kontakt')
@login_required
def kontakt():
    return render_template("kontakt.html", title="Kontakt")

#Route für das flowchart
@app.route('/flowChart')
@login_required
def flow_chart():
    return render_template("Flow_Chart.html", title="FlowChart")

#Route für den Chat
@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    form = CreateChat()
    # Hier werden Paramter übergebn, die mit Jinja in HTML verwendet werden können
    return render_template("chat.html", title="Chat", rooms=current_user.chats, current_user=current_user, form=form)


# Diese Route bestätigt die Existenz von usern beim Hinzufügen bei der Create Chat Funktion
@app.route('/chat/_validate_user', methods=['POST'])
@login_required
def valiadate_participants():
    # nachricht auspacken
    data = request.get_json()
      # nachricht im terminal loggen
    print(current_user.username + " send following fetch message \n" + str(data))
      # Prüfen ob der geschickte User in der Dtaenbank ist
    if User.query.filter_by(username=str(data["user_to_verify"])).first():
        data["valid"] = True
    # Antworten 
    res = make_response(jsonify(data), 200)
    #log
    print("Servers answer" + str(res.get_json()))
    return res



# Diese Route gibt Messages aus der Datenbank zurück wenn sie zum beispiel beim Infinite Scrolling oder beim laden von chats
@app.route('/chat/_get_messages', methods=['POST'])
@login_required
def get_messages():
    #daten entpacken
    data = request.get_json()
    #Daten loggen
    print(current_user.username + " is sending following fetch message \n" + str(data))
    # Chat ID aus Nachricht auslesen
    chat_id = data["chat_id"]
    #Chat suchen von dem Nachrichten gebraucht werden
    chat_new = Chat.query.filter_by(chat_id=chat_id).first()
    #response machen
    res = make_response(jsonify({}), 400)
    # Wenn chat existiert
    if chat_new:
        res = make_response(jsonify({}), 401)
        # Wenn der User der Anfragt auch Teil des Chats ist
        if current_user in chat_new.chat_participants:
            # Dem Client 40 Nachrichten zurückschicken
            msg_already_loaded = data["msg_already_loaded"]
            print("msg already loaded: "+ str(msg_already_loaded))
            # Berechnet den Index ab dem die neue Nachrichten geladen werden sollen
            # Bei Infinte Scrolling wird ein Wert msg_already_load mitgegeben dieser muss hier in einen
            # index umgerechnet werden
            current_load_index = len(chat_new.messages) - 1 - msg_already_loaded
            print(len(chat_new.messages))
            print(current_load_index)
            if current_load_index >= 0:
                
                # Wenn es noch mehr als 40 noch nicht geladene Nachrichten gibt
                if current_load_index >= 39:
                    msgs_to_send = chat_new.messages[current_load_index - 39:current_load_index + 1]
                else:
                    msgs_to_send = chat_new.messages[:current_load_index + 1]
                # Jedes Message Objekt in Dictionary umwandeln
                for i in range(0, len(msgs_to_send)):
                    msgs_to_send[i] = convert_to_dict(msgs_to_send[i])
                #Response bilden wenn es noch nachrichten zu senden gibt
                response = {
                    "messages": msgs_to_send,
                    "status": True
                }
                # Keine Nachrichten senden und status false wenn es keien NAchrichten mehr gibt
            else:
                response = {
                    "messages": [],
                    "status": False
                }
                # response senden und Dictionary in Json umwandeln
            print("Server is sending following answer:\n "+str(response))
            res = make_response(jsonify(response), 200)

    return res

# Wandlet ein Datenbank Objekt in ein Dictionary um
def convert_to_dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d

# Definiert dass bei Socket.IO auch die USer_identifikation durchgefühert werden kann
def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


# Beim testen im long-polling Mode bestht ein sehr großer delay bis erkannt
# wird, dass der User disconnected
# Wenn eventlet über einen WebSocket agiert haben wir eine Realtime übertragung
@socketio.on('disconnect',namespace="/chat")
def user_disconnect():
    if current_user.is_authenticated:
        print('Following Client disconnected:' + current_user.username)

# Beim connecnten mit dem Server joint der SUer allen angehörigen Chats damit er im Anschluss live NAchrichten empfangen kann
@socketio.on('connect', namespace="/chat")
@authenticated_only
def user_connect():
    user = User.query.filter_by(id=current_user.id).first()
    user.sid = request.sid
    db.session.commit()
    # join all chats with join_room
    for room in current_user.chats:
        join_room(room.chat_id)
    print("Client connected: " + current_user.username)

# Empfangen von NAchrichten im 'chat_message' Bucket
@socketio.on('chat_message', namespace="/chat")
@authenticated_only
def handle_message(msg):
    # Wenn Sender überhaupt im Chat
    if current_user in Chat.query.filter_by(chat_id=msg["room"]).first().chat_participants:
        #Message Datenbank Objekt bilden
        message = Message(text=msg["msg"], user=current_user.id, chat=msg["room"], user_name=current_user.username)
        # Datenbak adden und commiten
        db.session.add(message)
        db.session.commit()
        print(current_user.username +" is sending following message:\n"+str(message))
        # Antworten
        dictionary=convert_to_dict(message)
        json_response=json.dumps(dictionary)
        print(json_response)
        emit("chat_message",json_response ,room=message.chat)

      #wird gesendet
    


##########################################################
# Hier können live neue Chats erstellt werden
@socketio.on('create_new_chat', namespace="/chat")
@authenticated_only
def create_new_chat(chat_data):
    # Teilnehmer am neuen chat auslesn
    participants = chat_data["participants"]
    # neuen Chat erstellen
    newchat = Chat(title=chat_data["chat_name"])
    # Sender der NAchricht zum chat hinzufügen
    newchat.chat_participants.append(current_user)
    current_user_with_sid=User.query.filter_by(id=current_user.id).first()
    # Zum room joinen damit auch jetzt schon live nachrichten in dem Chat empfangen werden könen
    join_room(sid=current_user_with_sid.sid,room=newchat.chat_id)
    # Alle User in der Teilnehmerliste zum Chat hinzufügen
    for participant in participants:
        user = User.query.filter_by(username=participant).first()
        newchat.chat_participants.append(user)
        if user.sid != "":
            join_room(sid=user.sid,room=newchat.chat_id)
            # Datenbak committen
    db.session.add(newchat)
    db.session.commit()
    print(current_user.username + " send following fetch message \n" + str(newchat))
    dictionary={
        "new_chat_created":True
    }
    json_response=json.dumps(dictionary)
    print(json_response)
    # An alle USer die im neuen Chat sind live eine NAchricht schicken
    emit("create_new_chat",json_response ,room=newchat.chat_id)  #wird gesendet

# Zum verlassen von chats von chats
@socketio.on('delete_chat', namespace="/chat")
@authenticated_only
def delete_chat(chat_data):
    chat_data["chat_id"]
    #Chat finden
    chat_to_leave = Chat.query.filter_by(chat_id=int(chat_data["chat_id"])).first()
    # Über chsat iterieren und den user der die Anfrage zum leaven geschickt hat entfernen
    if current_user in chat_to_leave.chat_participants.all():
        chat_to_leave.chat_participants.remove(current_user)
    print(current_user.username + " left the chat-room: " + chat_to_leave.title)
    # Wenn keine Teilnehmer mehr im Chat sind nach dem verlassen Chat löschen
    if len(chat_to_leave.chat_participants.all()) == 0:
        for message_to_delete in chat_to_leave.messages:
            Message.query.filter(Message.message_id == message_to_delete.message_id).delete()   
        Chat.query.filter(Chat.chat_id == chat_data["chat_id"]).delete()     
    # Datenbak bestätigen
    db.session.commit()
    dictionary={
        "chat_left":True
    }
    json_response=json.dumps(dictionary)
    print(json_response)
    print(chat_data["chat_id"])
    # Alle User an die die NAchricht gesendt werden soll die NAchricht live senden
    emit('delete_chat',json_response ,room=int(chat_data["chat_id"]))
    leave_room(sid=request.sid,room=int(chat_data["chat_id"]))






#################### Thats how you would implement the create chat function with JS Fedge #########################

"""
@app.route('/chat/_create_Chat', methods=['POST'])
@login_required
def create_Chat():
    # Json Objekt in Python Dictionary umwandeln
    data = request.get_json()
    # log data
    print(current_user.username + " send following fetch message \n" + str(data))
    # Alle Teilnehmer am Chat aus der Dictionary entnehmen
    participants = data["participants"]
    # neuen Chat mit dem mitgegeben Namen erstellen
    newchat = Chat(title=data["chat_name"])
    # Die Teilnehmerliste besteh aus allen Usern aber ohne den Ersteller
    # Creator wird erst im Chat DatenbankObjekt hinzugefügt
    newchat.chat_participants.append(current_user)
    # Alle anderen User auf der Teilenhmerliste werden im Chat DatenbankObjekt hinzugefügt
    # außer der Creator, dieser wurde bereits hinzuegfügt
    for participant in participants:
        user = User.query.filter_by(username=participant).first()
        newchat.chat_participants.append(user)
    # Die Datenbak Read/Write session commiten
    db.session.add(newchat)
    db.session.commit()


    data.update({"chat_id": newchat.chat_id})
    # Antwort für den Client erstellen-->Dictionary wird wieder in Json Objekt konvertiert
    res = make_response(jsonify(data), 200)
    # log data
    print("Servers answer" + str(res.get_json()))
    return res
"""