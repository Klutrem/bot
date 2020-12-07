import vk_api 
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import bs4 as bs4
import requests
import random
import datetime 
import sqlite3 as sql

class VkBot():
	def __init__(self, user_id):
		self.user_id = user_id 
		self.idontknowcommands =['Извините, я не понимаю', 'Не знаю такой команды. Напишите "Команды, чтобы узнать, что я умею', 
		'Не понимаю о чем вы...', 'Не могу распознать.', 'Меня такому ещё не научили.']
		self.commands = [['время'], 
		['записать дз', "записать домашку", "записать", "запись"],
		['узнать домашку', "дз", "домашка", "че задали", "чё задали", "чё задали?", "узнать дз"]]
		self.day = datetime.date.today().isoweekday()
		if self.day == 1 :
			self.next_day = 2
		elif self.day == 2 :
			self.next_day = 3
		elif self.day == 3 :
			self.next_day = 4
		elif self.day == 4 :
			self.next_day = 5
		elif self.day == 5 :
			self.next_day = 6
		else : 
			self.next_day = 1

		self.test = []
		self.day_2 = self.next_day
				

		self.status = 0

	@staticmethod 
	def _clean_all_tag_from_str(string_line):
		result = ''
		not_skip = True 
		for i in list(string_line):
			if not_skip:
				if i == '<':
					not_skip = False
				else :
					result += i 
			else :
				if i == '>':
					not_skip = True
		return result

	def get_time(self):
		request = requests.get('https://my-calend.ru/date-and-time-today')
		b = bs4.BeautifulSoup(request.text, 'html.parser')
		return self._clean_all_tag_from_str(str(b.select('.page')[0].findAll('h2')[1])).split()[1]

	def create_keyboard(self, message):
		keyboard = VkKeyboard(one_time = True)
		keyboard.add_button('Записать дз', color = VkKeyboardColor.PRIMARY)
		keyboard.add_button('Узнать дз', color = VkKeyboardColor.POSITIVE)

		return keyboard.get_keyboard()

	def home_work(self, message):
		if self.status == 1 :
			day_2 = self.next_day
			message_ = str(message).split(' : ')
			lesson = message_[0]
			task = message_[1]			
			con = sql.connect('homework.db')
			cur = con.cursor()
			answer = []
			while answer == self.test :
				if day_2 > 6 : 
					day_2 = 1
				cur.execute('''SELECT "task" FROM "{0}" WHERE "lesson" = "{1}"'''.format(day_2, lesson))
				answer = cur.fetchall()
				day_2 += 1 
				if answer != self.test :
					cur.execute('UPDATE "{}" SET "task" = "{}" WHERE "lesson" = "{}"'.format(str(day_2 - 1), task, lesson))
					con.commit()
					cur.close()
					con.close()
					break
			print('\n' + 'записано' )
			return 'Задание записано.'
			self.status = 0 
			#искать предмет во всех таблицах с помощью цикла for
		else : 
			print('abs')

	def new_message(self, message):
		for i in self.commands[0] :
			if message == i : 
				return self.get_time()
		for i in self.commands[1] :
			if message == i :
				self.status = 1
				return 'Напишите название предмета и задание через двоеточие'
		for i in self.commands[2] :
			if message == i :
				con = sql.connect('homework.db')
				cur = con.cursor()
				cur.execute('SELECT * FROM "{}"'.format(self.next_day))
				task = cur.fetchall()	
				con.commit()
				cur.close()
				con.close()
				result = []
				for i in task :
					try :
						result.append(str(i[0] + ':' + i[1]))
					except TypeError :
						pass
				final_message = str(result)
				return final_message.replace("'", "").replace('[', '').replace(']', '')
		else :
			return random.choice(self.idontknowcommands)
				


