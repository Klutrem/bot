import vk_api 
from vk_api.longpoll import VkLongPoll, VkEventType
from vkbot import VkBot
import random
import sys
import time 
import datetime 

def write_msg(user_id, message, keyboard):
	vk.method('messages.send', {'user_id':user_id, 'message':message, 'random_id':time.time(), 'keyboard' : keyboard })


token = 'f7d4e368b3687418d31cd63ca99a784964e527b633c079c62c6fff29594bbb23dba2f0720d1ce547d82be'
vk = vk_api.VkApi(token = token)
longpoll = VkLongPoll(vk)
my_id = 62310117
print('bot started')
bot = VkBot(my_id)





for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW :
		if event.to_me :
			print(f'New message from : {event.user_id}', end = '')			
			if bot.status == 1 :
				write_msg(event.user_id, bot.home_work(event.text.lower()), bot.create_keyboard(event.text.lower()))
				bot.status = 0 
			elif bot.status == 0 :
				write_msg(event.user_id, bot.new_message(event.text.lower()), bot.create_keyboard(event.text.lower()))