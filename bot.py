TOKEN = '<здесь надо вставить токен тг-бота>'
read_bot = telebot.TeleBot(TOKEN)
manga_check = {}

@read_bot.message_handler(commands=['start'])  
def start(message):
  if manga_check.get(message.chat.id, 42) == 42:
    manga_check[message.chat.id] = {}
  read_bot.send_message(message.from_user.id, "Привет! Я - бот, который поможет тебе следить за обновлениями манги. Для того, чтобы узнать команды, напиши /help.")

@read_bot.message_handler(commands=['help'])
def help(message):
  if manga_check.get(message.chat.id, 42) == 42:
    manga_check[message.chat.id] = {}
  read_bot.send_message(message.from_user.id, "_Список команд:_ \n /new - добавляет новую мангу по запросу. Формат: `/new https://readmanga.live/<manga_id>` (принимаются *только* ссылки с ридманги) \n /check - проверяет по всему списку ссылок обновления, выводит все, которые изменились \n /list - выводит список названий отслеживаемых манг для данного пользователя \n /delete - позволяет удалить мангу из отслеживаемого списка. Формат: `/delete <название манги>`", parse_mode='Markdown')

@read_bot.message_handler(commands=['new'])
def new(message):
  if manga_check.get(message.chat.id, 42) == 42:
    manga_check[message.chat.id] = {}
  url = message.text[5:]
  if url == '' or (url.find('https://www.readmanga.live') == -1 and url.find('https://readmanga.live') == -1) or url.count('/') != 3:
    read_bot.send_message(message.from_user.id, "Неправильный формат! Пожалуйста, введи `/new https://readmanga.live/<manga_id>`", parse_mode='Markdown')
    return
  readmanga_html = requests.get(url)
  soup = BeautifulSoup(readmanga_html.content, 'html.parser')
  manga_name = soup.find_all('span', 'name')
  if manga_name != []:
    manga_name = soup.find_all('span', 'name')[0].contents[0]
  else:
    read_bot.send_message(message.from_user.id, "Такой манги нет!")
    return
  chapter_list = soup.find_all('td', ' ')
  if chapter_list != []:
    last_chapter = soup.find_all('td', ' ')[0].contents[1].contents[0].strip()
  else:
    last_chapter = 'Глав нет'
  manga_check[message.chat.id][manga_name] = [url, last_chapter]
  read_bot.send_message(message.from_user.id, "Готово :3")

  
@read_bot.message_handler(commands=['list'])
def view_list(message):
  if manga_check.get(message.chat.id, 42) == 42:
    manga_check[message.chat.id] = {}
  index = 1
  all_manga = ""
  for manga in manga_check[message.chat.id]:
    manga_url = '[{text}]({link})'.format(link=manga_check[message.chat.id][manga][0], text=manga)
    all_manga += str(index)+'. '+manga_url+' '+manga_check[message.chat.id][manga][1]+'\n'
    index += 1
  if all_manga == "":
    read_bot.send_message(message.from_user.id, "У тебя пустой список :(")
    return
  read_bot.send_message(message.from_user.id, all_manga, parse_mode='Markdown')

@read_bot.message_handler(commands=['check'])
def check(message):
  if manga_check.get(message.chat.id, 42) == 42:
    manga_check[message.chat.id] = {}
  all_updates = "_Обновления:_\n"
  for manga in manga_check[message.chat.id]:
    manga_url = '[{text}]({link})'.format(link=manga_check[message.chat.id][manga][0], text=manga)
    soup = BeautifulSoup(requests.get(manga_check[message.chat.id][manga][0]).content, 'html.parser')
    chapter_list = soup.find_all('td', ' ')
    if chapter_list != []:
      last_chapter = soup.find_all('td', ' ')[0].contents[1].contents[0].strip()
    else:
      last_chapter = 'Глав нет'
    if last_chapter != manga_check[message.chat.id][manga][1]:
      manga_check[message.chat.id][manga][1] = last_chapter
      all_updates += manga_url+': '+last_chapter+'\n'
  if all_updates == "_Обновления:_\n":
    all_updates = "Нет обнов :("
  read_bot.send_message(message.from_user.id, all_updates, parse_mode='Markdown')

@read_bot.message_handler(commands=['delete'])
def delete(message):
  if manga_check.get(message.chat.id, 42) == 42:
    manga_check[message.chat.id] = {}
  manga_name = message.text[8:]
  if manga_name == '':
    read_bot.send_message(message.from_user.id, "Неправильный формат! Пожалуйста, введи `/delete <название манги>` (название манги можно проверить в \list)", parse_mode='Markdown')
    return
  if manga_check[message.chat.id].pop(manga_name, 42) == 42:
    read_bot.send_message(message.from_user.id, "Такой манги в твоем списке нет :0")
    return
  read_bot.send_message(message.from_user.id, 'Готово!')

@read_bot.message_handler(content_types=['text'])
def text(message):
  if manga_check.get(message.chat.id, 42) == 42:
    manga_check[message.chat.id] = {}
  read_bot.send_message(message.from_user.id, "Привет! Я - бот, который поможет тебе следить за обновлениями манги. Для того, чтобы узнать команды, напиши /help.")


read_bot.polling(none_stop=True)
