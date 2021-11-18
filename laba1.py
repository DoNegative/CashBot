import telebot;
import sqlite3
import datetime


conn = sqlite3.connect('cash.db', check_same_thread=False)
cursor = conn.cursor()
bot = telebot.TeleBot('2145441676:AAHuN1AbKGvngnokt1n_R_Q0ySluvEZHay4')

#Создаем таблицу покупок
'''
cursor.execute("""CREATE TABLE test
                  (type text, price int,
                   date text)
               """)


'''
#Создаем таблицу доходов
'''
cursor.execute("""CREATE TABLE test1
                  (type text, price int,
                   date text)
               """)

'''


#Добавление в таблицу покупок
def db_table_val(type: str, price: int, date: str):
	cursor.execute('INSERT INTO test (type, price, date) VALUES (?, ?, ?)', (type, price, date))
	conn.commit()
conn.commit()

#Добавление в таблицу доходов
def db_cash(type: str, price: int, date: str):
	cursor.execute('INSERT INTO test1 (type, price, date) VALUES (?, ?, ?)', (type, price, date))
	conn.commit()
conn.commit()

@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.send_message(message.from_user.id, 'Добро пожаловать, \n "buy"- записать расходы \n "income" - записать поступления \n Что-то другое - любой символ'  ) 
    bot.register_next_step_handler(msg, vibor)
     
    
    
    
def vibor(message):     
    print(message.text) 
    if (message.text == "buy"):
        msg= bot.send_message(message.from_user.id, "Привет, что вы купили и сколько это стоило? Данные вводите в формате ""Что купили+цена""")
        bot.register_next_step_handler(msg, get_buy)
    if (message.text == "income"):
        msg= bot.send_message(message.from_user.id, "Привет, какие у вас были поступления ""Откуда+сумма""")
        bot.register_next_step_handler(msg, get_income)
    msg = bot.send_message(message.from_user.id, '\n "/outcome" - получить все расходы \n "/deleted - Удалить таблицу расходов \n "/deleted1 - Удалить таблицу доходов'  )       

  
                   
#Записываем покупки

def get_buy(message):
    if message:
        arr=message.text.split("+")
       
        type = arr[0]
        price = arr[1]
        date = datetime.datetime.now()
        db_table_val(type=type, price=price, date=date)
# Записываем поступления

def get_income(message):
    if message:
        arr=message.text.split("+")
        type = arr[0]
        price = arr[1]
        date = datetime.datetime.now()
        db_cash(type=type, price=price, date=date)

#Сумма всех трат     
@bot.message_handler(commands=['outcome'])
def outcome(message):
    sql = "SELECT SUM(price) FROM test"
    cursor.execute(sql)
    vivod=cursor.fetchall()
    bot.send_message(message.from_user.id, vivod)

#Удаление таблицы расходов    
@bot.message_handler(commands=['deleted'])
def deletet(message):
    sql = "DELETE FROM test"
    cursor.execute(sql)
    vivod=cursor.fetchall()
    bot.send_message(message.from_user.id, vivod)

#Удаление таблицы доходов
@bot.message_handler(commands=['deleted1'])
def deletet1(message):
    sql = "DELETE FROM test1"
    cursor.execute(sql)
    vivod=cursor.fetchall()
    bot.send_message(message.from_user.id, vivod)


bot.polling(none_stop=True, interval=0)