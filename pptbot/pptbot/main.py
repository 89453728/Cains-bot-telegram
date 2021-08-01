from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
import random
import time
import urllib
import json
import sqlite3
from users import User

DB = "ppt.db"
DBUSERS = "../../usuarios.db"

def join (arr):
    text = ""
    for iter in range(0,len(arr)):
        text += arr[iter] + " "
    return text

def getFrase(pos: int, tabla:str):
    db = sqlite3.connect(DB)
    frase = (db.execute("select * from " + tabla + "  where id = " + str(pos) + ";")).fetchall()
    return frase[0][1]
def getMaxID2(table: str):
    db = sqlite3.connect("ppt.db")
    num = (db.execute("select max(id) from " + table + ";")).fetchall()
    db.close()
    return num[0][0]
# https://api.telegram.org/bot1866547726:AAH6oaROz1TbuaLOv0i-yBZFHwaOllikCRE/getUpdates

def getUser(username: str) -> User:
    db = sqlite3.connect(DBUSERS)
    query = (db.execute("SELECT * FROM usuarios WHERE username = \"" + username + "\";")).fetchall()
    db.close()
    if (len(query) > 0):
        query = query[0]
        return User(int(query[0]),query[1],int(query[2]),int(query[3]),int(query[4]),int(query[5]),int(query[6]))
    else: 
        return -1
def saveUser(usuario: User):
    db = sqlite3.connect(DBUSERS)
    cur = db.cursor()
    query = "UPDATE usuarios SET blanchus="+str(usuario.blanchus)+", pocket="+str(usuario.pocket)+", banco="+str(usuario.banco)+", tipobanco="+str(usuario.tipobanco)+", robado=" + str(usuario.robado) + " WHERE username = \""+usuario.username+"\";"
    cur.execute(query)
    db.commit()
    db.close()

def getMaxID():
    db = sqlite3.connect(DBUSERS)
    m = (db.execute("SELECT MAX(ID) FROM USUARIOS;")).fetchall()
    if (m[0][0] == None):
        m = 0
    else: 
        m = m[0][0]
    db.close()
    return int(m)

def newUser(usuario: User) -> int:
    db = sqlite3.connect(DBUSERS)
    cur = db.cursor()
    query = "INSERT INTO usuarios(id,username,blanchus,pocket,banco,tipobanco,robado) VALUES ("+str(usuario.id)+",\""+str(usuario.username)+"\","+str(usuario.blanchus)+","+str(usuario.pocket)+","+str(usuario.banco)+","+str(usuario.tipobanco)+","+str(usuario.robado)+");"
    cur.execute(query)
    db.commit()
    db.close()



token = "1866547726:AAH6oaROz1TbuaLOv0i-yBZFHwaOllikCRE"

def error(bot, update, error):
    print("error")

def fracaso(update: Update, context: CallbackContext):
    text = str(update.message.text)
    text = text.split(' ')
    if (len(text) >= 2):
        text = text[1:len(text)]
        text = join(text)

        db = sqlite3.connect(DB)
        cur = db.cursor()
        cur.execute("INSERT INTO fracasos (id, texto) VALUES ((SELECT MAX(ID) FROM fracasos) + 1,\"" +  text + "\");")
        db.commit()
        db.close()
    else:
        update.message.reply_text("debes incluir una frase")

def triunfo(update: Update, context: CallbackContext):
    text = str(update.message.text)
    text = text.split(' ')
    if (len(text) >= 2):
        text = text[1:len(text)]
        text = join(text)

        db = sqlite3.connect(DB)
        cur = db.cursor()
        cur.execute("INSERT INTO triunfos (id, texto) VALUES ((SELECT MAX(ID) FROM triunfos) + 1,\"" +  text + "\");")
        db.commit()
        db.close()
    else: 
        update.message.reply_text("debes incluir una frase")

def ppt(update: Update, context: CallbackContext) -> None:
    g = update.message.text
    opt = 0
    piedra = 1
    tijeras = 2
    papel = 3
    resp = ""

    user = update.message.from_user.username

    text = g.split(" ")
    if (len(text) != 2):
        update.message.reply_text("Para jugar: /ppt [piedra, papel, tijeras]")
    else :
        optPC = random.randint(1,300)
        if (text[1] == "piedra"):
            opt = piedra
            if (optPC >= 1 and optPC < 26):
                optPC = piedra 
            elif(optPC >= 26 and optPC < 200 ):
                optPC = papel
            elif (optPC >= 200 and optPC <= 300):
                optPC = tijeras
        elif (text[1] == "tijeras"):
            opt = tijeras
            if (optPC >= 1 and optPC < 26):
                optPC = tijeras 
            elif(optPC >= 26 and optPC < 200 ):
                optPC = papel
            elif (optPC >= 200 and optPC <= 300):
                optPC = piedra
        elif (text[1] == "papel"):
            opt = papel
            if (optPC >= 1 and optPC < 26):
                optPC = papel 
            elif(optPC >= 26 and optPC < 200 ):
                optPC = piedra
            elif (optPC >= 200 and optPC <= 300):
                optPC = tijeras
        elif (text[1] == "lumpi"):
            update.message.reply_text("Has ganado tio, esa es la mejor carta, gana a todo")
            return
        else: 
            update.message.reply_text("Opcion no valida. Para jugar: /ppt [piedra, papel, tijeras]")
            return 
            

        # bot piedra
        if (optPC == piedra):
            if (opt == piedra):
                resp = "Oh vaya, habeis empatado. Intentalo de nuevo a ver si hay suerte"
            elif (opt == tijeras):
                N = int(getMaxID2("fracasos"))
                x = random.randint(0,N)
                resp = getFrase(x,"fracasos")
                resp = resp + "\n BOT: piedra \n " + user + ": tijeras"
                username = update.message.from_user.username
                usuario = getUser(username)
                if (usuario == -1):
                    usuario = User(getMaxID()+1,username,0,0,0,0,0)
                    newUser(usuario)
                cant = usuario.give(11)
                saveUser(usuario)
                if (cant != -1):
                    resp += "\n\n*HAS PERDIDO "+ str(cant)+ " BLANCHUS*"
                else:
                    resp += "\n\n*TAS POBRE Y NO TE HEMOS QUITAO NA!*"
            elif (opt == papel):
                N = int(getMaxID2("triunfos"))
                x = random.randint(0,N)
                resp = getFrase(x,"triunfos")
                resp = resp + "\n BOT: piedra \n " + user + ": papel"
                username = update.message.from_user.username
                usuario = getUser(username)
                if (usuario == -1):
                    usuario = User(getMaxID()+1,username,0,0,0,0,0)
                    newUser(usuario)
                usuario.get(15)
                saveUser(usuario)
                resp += "\n\n*HAS GANADO 15 BLANCHUS*"
        # bot papel
        elif (optPC == papel):
            if (opt == piedra):
                N = int(getMaxID2("fracasos"))
                x = random.randint(0,N)
                resp = getFrase(x,"fracasos")
                resp = resp + "\n BOT: papel \n " + user + ": piedra"
                username = update.message.from_user.username
                usuario = getUser(username)
                if (usuario == -1):
                    usuario = User(getMaxID()+1,username,0,0,0,0,0)
                    newUser(usuario)
                cant = usuario.give(11)
                saveUser(usuario)
                if (cant != -1):
                    resp += "\n\n*HAS PERDIDO "+ str(cant)+ " BLANCHUS*"
                else:
                    resp += "\n\n*TAS POBRE Y NO TE HEMOS QUITAO NA!*"
            elif (opt == tijeras):
                N = int(getMaxID2("triunfos"))
                x = random.randint(0,N)
                resp = getFrase(x,"triunfos")
                resp = resp + "\n BOT: papel \n " + user + ": tijeras"
                username = update.message.from_user.username
                usuario = getUser(username)
                if (usuario == -1):
                    usuario = User(getMaxID()+1,username,0,0,0,0,0)
                    newUser(usuario)
                usuario.get(15)
                saveUser(usuario)
                resp += "\n\n*HAS GANADO 15 BLANCHUS*"
            elif (opt == papel):
                resp = "Oh vaya, habeis empatado. Intentalo de nuevo a ver si hay suerte"
        #bot tijeras
        else:
            if (opt == piedra):
                N = int(getMaxID2("triunfos"))
                x = random.randint(0,N)
                resp = getFrase(x,"triunfos")
                resp = resp + "\n BOT: tijeras \n " + user + ": piedra"
                username = update.message.from_user.username
                usuario = getUser(username)
                if (usuario == -1):
                    usuario = User(getMaxID()+1,username,0,0,0,0,0)
                    newUser(usuario)
                usuario.get(15)
                saveUser(usuario)
                resp += "\n\n*HAS GANADO 15 BLANCHUS*"
            elif (opt == tijeras):
                resp = "Oh vaya, habeis empatado. Intentalo de nuevo a ver si hay suerte"
            elif (opt == papel):
                N = int(getMaxID2("fracasos"))
                x = random.randint(0,N)
                resp = getFrase(x,"fracasos")
                resp = resp + "\n BOT: tijeras \n " + user + ": papel"
                username = update.message.from_user.username
                usuario = getUser(username)
                if (usuario == -1):
                    usuario = User(getMaxID()+1,username,0,0,0,0,0)
                    newUser(usuario)
                cant = usuario.give(11)
                saveUser(usuario)
                if (cant != -1):
                    resp += "\n\n*HAS PERDIDO "+ str(cant)+ " BLANCHUS*"
                else:
                    resp += "\n\n*TAS POBRE Y NO TE HEMOS QUITAO NA!*"
                
        time.sleep(0.3)
        update.message.reply_text(resp,parse_mode=ParseMode.MARKDOWN)

updater = Updater(token)
updater.dispatcher.add_handler(CommandHandler('ppt',ppt))
updater.dispatcher.add_handler(CommandHandler('fracaso',fracaso))
updater.dispatcher.add_handler(CommandHandler('triunfo',triunfo))

updater.dispatcher.logger.addFilter((lambda s: not s.msg.endswith('A TelegramError was raised while processing the Update')))
updater.dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()