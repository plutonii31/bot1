import telebot

bot = telebot.TeleBot("8431372366:AAEpwC8aSYe_1_8WgS4WYabhz8UUfySWxAo")
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row("Ежедневная награда", "Магазин")
keyboard1.row("Перевод", "Задания","промокод")
keyboard3 = telebot.types.ReplyKeyboardMarkup(True)
keyboard3.row("10", "50", "100", "300")
keyboard3.row("500", "1000", "1500", "3000")


def get_info(id, chat, m=True):
    with open("fil", "r") as file:
        f = file.readlines()
        print(f,"hgvbjknm")
        while "\n" in f:
            f.remove("\n")
        x = 0
        for i in f:
            if i.split(",")[0].split(":")[0] == str(id):
                return (i, f)
            else:
                print([i.split(",")[0].split(":")[0], id])
            x += 1
    if m:
        with open("fil", "w") as file:
            f.append(str(id) + ":0,0,0,")
            print([str(id)])
            print(f)
            file.write("".join(f) + "\n")
        bot.send_message(chat, "Аккаунт создан.")
    else:
        bot.send_message(chat, "Произошла ошибка.Аккаунта на этот ID не существует.")
        return None
    return get_info(id, chat)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Здравствуйте!", reply_markup=keyboard1)


quests = ["задание", "задание2"]
codes={"CodeFor10Coins":10,"Promo159":159}
idmode = False
summode = False
promomode=False
idu = None


@bot.message_handler(content_types=["text"])
def send_text(message):
    global idmode, idu, summode,promomode
    chat = message.chat.id

    id = message.from_user.id
    print(id)
    text = message.text
    info = get_info(id, chat)[0]
    in2 = get_info(id, chat)[1]
    if idmode:
        if text.isdigit():
            idmode = False
            idu = message.text

            bot.send_message(message.chat.id, "Какую сумму вы собираетесь перевести?", reply_markup=keyboard3)
            summode = True
            return
        else:
            bot.send_message(message.chat.id, "Это не число.", reply_markup=keyboard3)
            return

    if summode:
        if text.isdigit():
            summode = False
            sum = int(message.text)
            print(get_info(id, chat))
            c = (info.split(",")[0].split(":")[1])
            if int(c) < sum:
                bot.send_message(message.chat.id, "Недостаточно средств.", reply_markup=keyboard1)
                return
            c2 = (get_info(idu, chat)[0].split(",")[0].split(":")[1])
            x1 = str(id) + ":" + str(int(c) - sum) + "," + ",".join(get_info(id, chat)[0].split(
                ",")[1:])
            x2 = str(idu) + ":" + str(int(c2) + sum) + "," + ",".join(
                get_info(idu,
                         chat)[0].split(
                    ",")[1:])
            print(x1, x2, sum)
            print(in2)
            try:
                in2[in2.index(get_info(id, chat)[0])] = x1
                in2[in2.index(get_info(idu, chat)[0])] = x2
            except:
                bot.send_message(message.chat.id, "Произошла ошибка: вы попытались сделать перевод самому себе.",
                                 reply_markup=keyboard1)

            with open("fil", "w") as file:
                file.write("".join(in2))
            bot.send_message(message.chat.id, "Успешно переведено.", reply_markup=keyboard1)
            return
    if promomode:
        bot.send_message(message.chat.id, "Эта функция пока ещё в разработке.")
        promo=message.text
        if promo in codes.keys():
            pass
    print(id)
    c = info.split(",")[0].split(":")[1]
    mes = text.lower()
    if mes == "ежедневная награда":
        if info.split(",")[2] == "0":
            with open("fil", "w") as file:
                in2[in2.index(info)] = str(id) + ":" + str(
                    int(info.split(",")[0].split(":")[1]) + 10) + "," + info.split(",")[1] + "," + "1," + \
                                       info.split(",")[3]
                g = "\n".join(in2)
                file.write(g)
            print(g)

            bot.send_message(message.chat.id, "Ваши койны: " + str(int(c) + 10) + "")
            id = message.from_user.id
            text = message.text
            info = get_info(id, chat)[0]
            in2 = get_info(id, chat)[1]
            c = info.split(",")[0].split(":")[1]
            mes = text.lower
        else:
            bot.send_message(message.chat.id, "Вы уже взяли вашу награду сегодня!")
    if mes == "задания":
        bot.send_message(message.chat.id, "Ваши задачи на сегодня:")
        x = 0
        for i in quests:
            x += 1
            bot.send_message(message.chat.id, str(x) + ") " + i)
    if mes == "перевод":
        bot.send_message(message.chat.id, "Кому вы хотите перевести койны? (Введите ID)")
        u = []
        x = 0
        for i in in2[:-1]:
            x += 1
            bot.send_message(message.chat.id, str(x) + ") " + i.split(",")[0].split(":")[0])
            u.append(i.split(",")[0].split(":")[0])

        u.append(in2[-1].split(",")[0].split(":")[0])
        keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
        keyboard2.row(*u)
        bot.send_message(message.chat.id, str(len(in2)) + ") " + in2[-1].split(",")[0].split(":")[0],
                         reply_markup=keyboard2)
        idmode = True
    if mes == "магазин":
        bot.send_message(message.chat.id, "Эта функция пока ещё в разработке.")
    if mes=="промокод":
        promomode=True
    else:
        bot.send_message(message.chat.id, "Неизвестная команда.")


bot.polling(none_stop=True)



