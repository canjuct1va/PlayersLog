import telebot
from telebot import types
import random

user_role = {}

TOKEN = '7846837778:AAEBi0NzoM4I6G5cn7yUfy19Q6BafNXu8G8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['work'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Worker')
    btn2 = types.KeyboardButton('TC-Helper')
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, 
                     "Привет! Выберите свою роль:", 
                     reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Worker', 'TC-Helper'])
def show_options(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Чистая прибыль')
    btn2 = types.KeyboardButton('Добили')
    markup.add(btn1, btn2)
    
    if message.text == 'Worker':
        text = "Воркер, я помогу тебе рассчитать твою долю от лога.\nНужно всего нажать на кнопку ниже"
    else:
        text = "Хелпер, я помогу тебе рассчитать твою долю от лога.\nНужно всего нажать на кнопку ниже"
    
    user_role[message.chat.id] = message.text
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Чистая прибыль')
def ask_amount(message):
    msg = bot.send_message(message.chat.id, 
                          "Введите сумму лога в долларах (Только число):")
    bot.register_next_step_handler(msg, calculate_shares)

@bot.message_handler(func=lambda message: message.text == 'Добили')
def choose_dobiv_service(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('dobiv by drugsnotnx')
    btn2 = types.KeyboardButton('jufi')
    btn3 = types.KeyboardButton('waster')
    btn4 = types.KeyboardButton('Adark')
    btn5 = types.KeyboardButton('dobiv rampage')
    back = types.KeyboardButton('Назад')
    markup.add(btn1, btn2, btn3, btn4, btn5, back)
    
    bot.send_message(message.chat.id, 
                     "Выбери добивера:",
                     reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Назад')
def go_back(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Чистая прибыль')
    btn2 = types.KeyboardButton('Добили')
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, 
                     "Выберите действие:",
                     reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['dobiv by drugsnotnx', 'jufi', 'waster', 'Adark', 'dobiv rampage'])
def choose_region(message):
    service = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if service in ['dobiv by drugsnotnx', 'dobiv rampage']:
        regions = ['CN', 'EU', 'RU']
    elif service == 'jufi':
        regions = ['CN', 'EU']
    elif service == 'waster':
        regions = ['CN', 'EU']
    else:  # Adark
        regions = ['CN']
        
    for region in regions:
        markup.add(types.KeyboardButton(f'{service} - {region}'))
    markup.add(types.KeyboardButton('Назад'))
    
    bot.send_message(message.chat.id, 
                     "Выберите регион:",
                     reply_markup=markup)

@bot.message_handler(func=lambda message: ' - ' in message.text and message.text.split(' - ')[0] in ['dobiv by drugsnotnx', 'jufi', 'waster', 'Adark', 'dobiv rampage'])
def show_price_and_ask_amount(message):
    service, region = message.text.split(' - ')
    
    price_lists = {
        ('dobiv by drugsnotnx', 'CN'): (
            "💰 Прайс добива от dobiv by drugsnotnx:\n\n"
            "CN\n"
            "• $50 - $300: фикс $30\n"
            "• От $301: 10%\n\n"
        ),
        ('dobiv by drugsnotnx', 'EU'): (
            "💰 Прайс добива от dobiv by drugsnotnx:\n\n"
            "EU\n"
            "• $50 - $300: фикс $30\n"
            "• От $301: 14%\n\n"
        ),
        ('dobiv by drugsnotnx', 'RU'): (
            "💰 Прайс добива от dobiv by drugsnotnx:\n\n"
            "RU\n"
            "• $50 - $300: фикс $30\n"
            "• От $301: 16%\n\n"
        ),
        ('jufi', 'CN'): (
            "💰 Прайс добива от jufi:\n\n"
            "CN\n"
            "• $500 - $10000: 15%\n"
            "• От $10000: 12.5%\n\n"
        ),
        ('jufi', 'EU'): (
            "💰 Прайс добива от jufi:\n\n"
            "EU 🇪🇺\n"
            "• До $500: 30%\n"
            "• $500 - $5000: 10%\n"
            "• От $5000: 8%\n\n"
        ),
        ('waster', 'CN'): (
            "💰 Прайс добива от waster:\n\n"
            "CN\n"
            "• $200 - $399: 17%\n"
            "• $400 - $899: 15%\n"
            "• $900 - $4999: 13%\n"
            "• $5000 и выше: 10%\n\n"
        ),
        ('waster', 'EU'): (
            "💰 Прайс добива от waster:\n\n"
            "EU\n"
            "• $300 - $499: 20%\n"
            "• $500 - $899: 16%\n"
            "• $900 - $4999: 14%\n"
            "• $5000 и выше: 11%\n\n"
        ),
        ('Adark', 'CN'): (
            "💰 Прайс добива от Adark:\n\n"
            "CN\n"
            "• Все суммы от $100: 20%\n\n"
        ),
        ('dobiv rampage', 'CN'): (
            "💰 Прайс добива от dobiv rampage:\n\n"
            "CN\n"
            "• $50 - $300: фикс $30\n"
            "• От $301: 10%\n\n"
        ),
        ('dobiv rampage', 'EU'): (
            "💰 Прайс добива от dobiv rampage:\n\n"
            "EU\n"
            "• $50 - $300: фикс $30\n"
            "• От $301: 14%\n\n"
        ),
        ('dobiv rampage', 'RU'): (
            "💰 Прайс добива от dobiv rampage:\n\n"
            "RU\n"
            "• $50 - $300: фикс $30\n"
            "• От $301: 16%\n\n"
        )
    }
    
    price_list = price_lists.get((service, region), "Прайс не найден")
    price_list += "Введите сумму лога в долларах (Только число):"
    msg = bot.send_message(message.chat.id, price_list)
    bot.register_next_step_handler(msg, lambda m: calculate_with_dobiv(m, service, region))

def show_random_message(chat_id):
    if random.random() < 0.3:  
        choice = random.choice([1, 2])
        
        if choice == 1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
            buttons = [types.KeyboardButton(str(i)) for i in range(1, 11)]
            markup.add(*buttons)
            
            bot.send_message(chat_id, 
                           "Оцени работу бота от 1 до 10:", 
                           reply_markup=markup)
        else:
            bot.send_message(chat_id, 
                           "Всегда рад помочь!\nСЛАВА PLAYERS TEAM")

def calculate_shares(message):
    try:
        amount = float(message.text)
        role = user_role.get(message.chat.id, 'Worker')
        
        if role == 'Worker':
            ts_share = amount * 0.25
        else:
            ts_share = amount * 0.15
            
        scoop_share = amount * 0.20
        remaining = amount - ts_share - scoop_share
        
        response = (f"Расчет для суммы ${amount:,.2f}:\n\n"
                   f"ТС ({25 if role == 'Worker' else 15}%): ${ts_share:,.2f}\n"
                   f"Скуп (20%): ${scoop_share:,.2f}\n"
                   f"залетает на Bybit: ${remaining:,.2f}")
        
        bot.send_message(message.chat.id, response)
        show_random_message(message.chat.id)
        
    except ValueError:
        bot.send_message(message.chat.id, 
                        "Пожалуйста, введите корректное число")

def calculate_dobiv_amount(amount, service, region):
    if service in ['dobiv by drugsnotnx', 'dobiv rampage']:
        if 50 <= amount <= 300:
            return 30, "фикс $30"
        elif amount > 300:
            percentages = {'CN': 0.10, 'EU': 0.14, 'RU': 0.16}
            percent = percentages[region] * 100
            return amount * percentages[region], f"{percent}%"
            
    elif service == 'jufi':
        if region == 'CN':
            if 500 <= amount < 10000:
                return amount * 0.15, "15%"
            elif amount >= 10000:
                return amount * 0.125, "12.5%"
        else:  # EU
            if amount < 500:
                return amount * 0.30, "30%"
            elif amount < 5000:
                return amount * 0.10, "10%"
            else:
                return amount * 0.08, "8%"
                
    elif service == 'waster':
        if region == 'CN':
            if 200 <= amount <= 399:
                return amount * 0.17, "17%"
            elif 400 <= amount <= 899:
                return amount * 0.15, "15%"
            elif 900 <= amount <= 4999:
                return amount * 0.13, "13%"
            elif amount >= 5000:
                return amount * 0.10, "10%"
        else:  # EU
            if 300 <= amount <= 499:
                return amount * 0.20, "20%"
            elif 500 <= amount <= 899:
                return amount * 0.16, "16%"
            elif 900 <= amount <= 4999:
                return amount * 0.14, "14%"
            elif amount >= 5000:
                return amount * 0.11, "11%"
                
    elif service == 'Adark':
        if amount >= 100:
            return amount * 0.20, "20%"
            
    return 0, "0%"

def calculate_with_dobiv(message, service, region):
    try:
        amount = float(message.text)
        role = user_role.get(message.chat.id, 'Worker')
        
        min_amounts = {
            ('dobiv by drugsnotnx', 'CN'): 50,
            ('dobiv by drugsnotnx', 'EU'): 50,
            ('dobiv by drugsnotnx', 'RU'): 50,
            ('jufi', 'CN'): 500,
            ('jufi', 'EU'): 0,
            ('waster', 'CN'): 200,
            ('waster', 'EU'): 300,
            ('Adark', 'CN'): 100,
            ('dobiv rampage', 'CN'): 50,
            ('dobiv rampage', 'EU'): 50,
            ('dobiv rampage', 'RU'): 50
        }
        
        if amount < min_amounts.get((service, region), 0):
            bot.send_message(message.chat.id, 
                           f"Сумма должна быть не менее ${min_amounts.get((service, region))}")
            return
        
        if role == 'Worker':
            ts_share = amount * 0.25
        else:
            ts_share = amount * 0.15
            
        scoop_share = amount * 0.20
        dobiv, dobiv_percent = calculate_dobiv_amount(amount, service, region)
        remaining = amount - ts_share - scoop_share - dobiv
        
        response = (f"Расчет для суммы ${amount:,.2f}:\n\n"
                   f"ТС ({25 if role == 'Worker' else 15}%): ${ts_share:,.2f}\n"
                   f"Скуп (20%): ${scoop_share:,.2f}\n"
                   f"Добив от {service} - {region} ({dobiv_percent}): ${dobiv:,.2f}\n"
                   f"залетает на Bybit: ${remaining:,.2f}")
        
        bot.send_message(message.chat.id, response)
        show_random_message(message.chat.id)
        
    except ValueError:
        bot.send_message(message.chat.id, 
                        "Пожалуйста, введите корректное число")

@bot.message_handler(func=lambda message: message.text in [str(i) for i in range(1, 11)])
def handle_rating(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Чистая прибыль')
    btn2 = types.KeyboardButton('Добили')
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, 
                    f"Спасибо за оценку {message.text}/10! 🙏",
                    reply_markup=markup)

if __name__ == '__main__':
    bot.polling(none_stop=True) 