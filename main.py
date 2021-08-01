from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler
import time 
import sqlite3
import random
from telegram.ext.filters import UpdateFilter
from telegram.utils.helpers import create_deep_linked_url
from lib.users import User

DB = "usuarios.db"
TOKEN = "your token"

def error(bot, update, error):
    print("error")

def getUser(username: str) -> User:
    db = sqlite3.connect(DB)
    query = (db.execute("SELECT * FROM usuarios WHERE username = \"" + username + "\";")).fetchall()
    db.close()
    if (len(query) > 0):
        query = query[0]
        return User(int(query[0]),query[1],int(query[2]),int(query[3]),int(query[4]),int(query[5]),int(query[6]))
    else: 
        return -1
def saveUser(usuario: User):
    db = sqlite3.connect(DB)
    cur = db.cursor()
    query = "UPDATE usuarios SET blanchus="+str(usuario.blanchus)+", pocket="+str(usuario.pocket)+", banco="+str(usuario.banco)+", tipobanco="+str(usuario.tipobanco)+", robado=" + str(usuario.robado) + " WHERE username = \""+usuario.username+"\";"
    cur.execute(query)
    db.commit()
    db.close()

def getMaxID():
    db = sqlite3.connect(DB)
    m = (db.execute("SELECT MAX(ID) FROM USUARIOS;")).fetchall()
    if (m[0][0] == None):
        m = 0
    else: 
        m = m[0][0]
    db.close()
    return int(m)

def newUser(usuario: User) -> int:
    db = sqlite3.connect(DB)
    cur = db.cursor()
    query = "INSERT INTO usuarios(id,username,blanchus,pocket,banco,tipobanco,robado) VALUES ("+str(usuario.id)+",\""+str(usuario.username)+"\","+str(usuario.blanchus)+","+str(usuario.pocket)+","+str(usuario.banco)+","+str(usuario.tipobanco)+","+str(usuario.robado)+");"
    cur.execute(query)
    db.commit()
    db.close()

def dep(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user.username
    text = update.message.text 
    text = text.split(' ')
    if (len(text) != 2):
        update.message.reply_text("para depositar >> /dep cantidad")
        return
    cantidad = int(text[1])
    if(cantidad < 0):
        update.message.reply_text("*NO PUEDES DEPOSITAR CANTIDAD NEGATIVA* \n", parse_mode=ParseMode.MARKDOWN)
        return 
    usuario = getUser(username)

    if (usuario == -1):
        usuario = User(getMaxID()+1,username,0,0,0,0,0)
        newUser(usuario)
    sobrante = usuario.dep(cantidad)

    if(sobrante != -1):
        update.message.reply_text("*DEPOSITO REALIZADO CON EXITO * \n Has ingresado " + str(sobrante) + " 📀 (blanchus) \n 💳 *Banco:* "+str(usuario.banco)+" 📀\n💰 *Cartera:* "+str(usuario.pocket)+" 📀", parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("*DEPOSITO NO REALIZADO* \n\nNo tienes suficientes blanchus en la cartera 😔", parse_mode=ParseMode.MARKDOWN)
    saveUser(usuario)

def ret(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user.username
    text = update.message.text
    text = text.split(' ')
    if (len(text) != 2):
        update.message.reply_text("para depositar >> /dep cantidad")
        return
    cantidad = int(text[1])
    if(cantidad < 0):
        update.message.reply_text("*NO PUEDES RETIRAR CANTIDAD NEGATIVA* \n", parse_mode=ParseMode.MARKDOWN)
        return 
    usuario = getUser(username)
    if (usuario == -1):
        usuario = User(getMaxID()+1,username,0,0,0,0,0)
        newUser(usuario)
    result = usuario.ret(cantidad)
    if(result != -1):
        update.message.reply_text("*EXTRACCION REALIZADA CON EXITO* \n Has retirado " + str(result) + " 📀 (blanchus) \n 💳 *Banco:* "+str(usuario.banco)+" 📀\n💰 *Cartera:* "+str(usuario.pocket)+" 📀", parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("*EXTRACCION NO REALIZADA* \n\nNo tienes suficientes blanchus en la cartera 😔", parse_mode=ParseMode.MARKDOWN)
    saveUser(usuario)

def b(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    text = update.message.text
    text = text.split(' ')
    if (len(text) == 2):
        username = text[1][1:len(text[1])]
    elif(len(text) > 2):
        return
    usuario = getUser(username)
    if (usuario == -1):
        usuario = User(getMaxID()+1,username,0,0,0,0,0)
        newUser(usuario)
    update.message.reply_text("* USUARIO * @"+username+"\n\nBlanchus: "+ str(usuario.blanchus)+" 📀 \nCartera: "+str(usuario.pocket)+" 📀 \nBanco: "+str(usuario.banco) + " 📀", parse_mode=ParseMode.MARKDOWN)

def dar(update: Update, context: CallbackContext): 
    username1 = update.message.from_user.username
    text = update.message.text
    text = text.split(' ')
    if (len(text) != 3):
        update.message.reply_text("para donar a alguien >> /dar @usuario cantidad")
        return
    username2 = text[1][1:len(text[1])]
    cantidad = int(text[2])
    if(cantidad < 0):
        update.message.reply_text("*NO PUEDES DAR CANTIDAD NEGATIVA* \n", parse_mode=ParseMode.MARKDOWN)
        return
    usuario1 = getUser(username1)
    if (usuario1 == -1):
        usuario1 = User(getMaxID()+1,username1,0,0,0,0,0)
        newUser(usuario1)
    usuario2 = getUser(username2)
    if (usuario2 == -1):
        usuario2 = User(getMaxID()+1,username2,0,0,0,0,0)
        newUser(usuario2)
    ammount = usuario1.give(cantidad)
    if (ammount != -1):
        usuario2.get(ammount)
        update.message.reply_text("*TRANSACCION REALIZADA*\n Cartera de @"+username2+": " + str(usuario2.pocket) + "\n Cartera de @" + str(username1) + ": " + str(usuario1.pocket) + " ",parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("*NO TIENES SUFICIENTES BLANCHUS* 😔", parse_mode=ParseMode.MARKDOWN)
        return
    saveUser(usuario1)
    saveUser(usuario2)

def robar(update: Update, context: CallbackContext):
    TRIUNFO = 1
    HUIDA = 2
    FRACASO = 3
    estado = 1

    username1 = update.message.from_user.username
    text = update.message.text
    text = text.split(' ')
    if (len(text) != 2):
        update.message.reply_text("para robar a alguien >> /robar @usuario")
        return
    username2 = text[1][1:len(text[1])]
    robo = random.randint(0,1000)
    if (robo > 0 and robo <= 200):
        estado = FRACASO
    elif (robo > 270 and robo <= 490):
        estado = HUIDA
    else:
        estado = TRIUNFO
    
    usuario1 = getUser(username1)
    usuario2 = getUser(username2)
    if (usuario1 == -1):
        usuario1 = User(getMaxID()+1,username1,0,0,0,0,0)
        newUser(usuario1)
    if (usuario2 == -1):
        usuario2 = User(getMaxID()+1,username2,0,0,0,0,0)
        newUser(usuario2)
    canbe = usuario2.serRobado()
    if (canbe == -1):
        update.message.reply_text("*NO PUEDES ROBAR A ESTE USUARIO* \n Iyo, que le han robao hace menos de 12 horas, dale tregua, no?", parse_mode=ParseMode.MARKDOWN)
        return 
    
    if(estado == TRIUNFO):
        x = int(random.random()*usuario2.pocket)
        cant = usuario2.give(x)
        usuario1.get(cant)
        update.message.reply_text("*ROBO CON EXITO!!* \n@"+username1+"ha robado "+str(cant)+" 📀 Blanchus a @" + username2 + "\n", parse_mode=ParseMode.MARKDOWN)
        usuario2.robado = int(time.time())
        saveUser(usuario1)
        saveUser(usuario2)
    elif(estado == FRACASO):
        x = int(random.random()*usuario1.pocket)
        cant = usuario1.give(x)
        if(cant == -1):
            update.message.reply_text("*TE HA ATRAPADO LA POLI* \n @"+username1+" ha sido atrapado por la policia y debe pagarle una indemnizacion a @"+username2+" pero no tiene dinero en la cartera asi que se le retirara del banco XD", parse_mode=ParseMode.MARKDOWN)
            x = int(random.random()*usuario1.banco)
            usuario1.ret(x)
            cant = usuario1.give(x)
            usuario2.get(cant)
            update.message.reply_text("*INDEMNIZACION EXITOSA!* \n@"+username1+" ha indemnizado a @"+ username2 + " con " + str(cant) + " 📀 Blanchus", parse_mode=ParseMode.MARKDOWN)
            return 
        usuario2.get(cant)
        saveUser(usuario1)
        saveUser(usuario2)
    else:
        update.message.reply_text("*EL LADRON SE ESCAPA* \n@"+username1 + " se ha dado a la fuga antes de que llegue la poli al haber fracasado", parse_mode=ParseMode.MARKDOWN)

def msg(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    usuario = getUser(username)
    if(usuario == -1):
        usuario = User(getMaxID()+1, username, 0,0,0,0,0)
        newUser(usuario)
    text = update.message.text 
    if (len(text) > 0 and len(text) <= 50):
        usuario.get(5)
    elif(len(text) > 50 and len(text) <= 100):
        usuario.get(10)
    elif(len(text) > 100 and len(text) <= 300):
        usuario.get(30)
    else: 
        usuario.get(50)
    saveUser(usuario)

def about(update: Update, context: CallbackContext):
    update.message.reply_text("*INFORMACION ACERCA DE BLANCHU* \n Blanchu es un bot que sirve para la gestion del grupo con un sistema economico ficticio basado en una moneda llamada blanchu.\nBlanchu no recopila ningun tipo de informacion de los usuarios salvo su nombre de usuario para poder asi localizarlos a la hora de hacer cambios en su cartera de blanchus.\n\nSi quieres saber mas acerca del desarrollador de Blanchu: https://github.com/23califatus", parse_mode=ParseMode.MARKDOWN)


updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler('dep',dep))
updater.dispatcher.add_handler(CommandHandler('ret',ret))
updater.dispatcher.add_handler(CommandHandler('b',b))
updater.dispatcher.add_handler(CommandHandler('dar',dar))
updater.dispatcher.add_handler(CommandHandler('robar',robar))
updater.dispatcher.add_handler(CommandHandler('about',about))
updater.dispatcher.add_handler(MessageHandler(~Filters.command,msg))

updater.dispatcher.logger.addFilter((lambda s: not s.msg.endswith('A TelegramError was raised while processing the Update')))
updater.dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()