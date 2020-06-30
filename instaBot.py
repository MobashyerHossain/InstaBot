from selenium import webdriver as driver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from faker import Faker
from PIL import Image
from sys import stdout as std
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import numpy as np
import regex as re
import random
import os
import sys

########### Get Famous Joker Quates Starts ###########

def uncensor(line):
	line = line
	line = re.sub(r"[s|S][h|H|\*][i|I|\*][t|T]", "shit", line)
	line = re.sub(r"[f|F][u|U|\*][c|C|\*][k|K]", "fuck", line)
	line = re.sub(r"[b|B][i|i|\*][t|T|\*][c|C|\*][h|H]", "bitch", line)
	line = re.sub(r"[\*|a|A][s|S|\*][s|S|\*]", "ass", line)
	line = re.sub(r"[d|D][\*|a|A][\*|m|M][n|N]", "damn", line)
	line = re.sub(r"[b|B][\*|a|A][s|S|\*][t|T]\w*", "bastard", line)
	return line

def clean_list(items):
	newList = []
	for item in items:
		item = uncensor(item)
		newList.append(item)

	return newList

def select_random_quates(quates, author):
	choice = random.randint(0, len(quates))
	# print(choice)
	file = "used_{}_Quates.txt".format(author)

	if not os.path.exists(file):
		f = open(file, "x")
		f.close()

	try:
		with open(file, "r") as f:
			used = [int(x) for x in list(f.read().splitlines()) if x != '']
			if choice in used:
				quates = quates.remove(quates[choice])
				select_random_quates(quates, author)
			else:
				f.close()
	except Exception as e:
		pass

	with open(file, "a") as f:
		f.write(str(choice))
		f.write('\n')
	f.close()

	return quates[choice]

def full_caption(quate, author, tags, cc = 'Sexy_With_Madness'):
	caption = []

	if len(quate) > 1:
		caption.append(uncensor(quate))

	if len(author) > 1:
		caption.append('By - {}'.format(author))

	caption.append('CC-{}'.format(cc))

	tags.append('Madness_Rules')

	for tag in tags:
		tag = tag.replace(' ', '_')
		caption.append('#{}\n'.format(tag))
	
	return caption

########### Get Famous Joker Quates Ends ###########

def rand_Sleep(startTime = 1, endTime = 4):
	total_time = round(random.uniform(startTime, endTime), 3)
	progress_display(total_time)

def progress_display(total_time):
	tt = total_time
	gap_time = round(total_time/100, 3)

	counter = 0
	while total_time > 0:
		counter += 1
		total_time = round(total_time - gap_time, 3)
		std.write("\r")
		std.write("Sleep Progress {} seconds: {} %".format(tt, counter))
		std.flush()
		sleep(gap_time)

	std.write("\r")
	std.write("{} Second Sleep Over!\n".format(round(tt,2)))
	std.flush()

class InstaBot:
	def __init__(self, username, password):
		self.faker = Faker()

		# mobile emulution setting
		mobile_emulation = {
			"deviceMetrics": {"width": 360, "height": 600, "pixelRatio": 3.0},
			"userAgent": "Mozilla/5.0 (Linux; Android 5.1.1; en-us; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36" }

		chrome_options = Options()
		chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

		# driver setting
		self.driver = driver.Chrome(chrome_options = chrome_options)
		# self.driver.implicitly_wait(10)
		self.driver.maximize_window()
		self.driver.get("https://www.instagram.com/")
		rand_Sleep()
		self.login(username, password)

	def dummy_clicks(self, name, xpath, ctype=1, sleep_time=[3, 5]):
		try:
			button = self.driver.find_element_by_xpath(xpath)
		except Exception as e:
			pass
		else:
			if ctype == 1:
				print('JS click of {} Button'.format(name))
				self.driver.execute_script("arguments[0].click();", button)
			else:
				print('Normal click of {} Button'.format(name))
				button.click()
			rand_Sleep(sleep_time[0], sleep_time[1])


	def dummy_writes(self, name, xpath, content, clear_flag = 1, sleep_time=[3, 5]):
		try:
			field = self.driver.find_element_by_xpath(xpath)
		except Exception as e:
			pass
		else:
			print('Filling {} Field'.format(name))
			if clear_flag == 1:
				field.clear()
				field.send_keys(content)
			else:
				field.send_keys(content)
				sleep(0.01)
				ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
				sleep(0.01)
			
			rand_Sleep(sleep_time[0], sleep_time[1])

	def close_extras(self):
		# close remember tab
		test = self.driver.find_elements_by_xpath('//*[contains(text(), "Save Your Login Info?")]')
		if len(test) > 0:
			self.dummy_clicks('Close Remember', '//*[contains(text(), "Not Now")]')
		else:
			print("'Close Remember' not Encountered")

		# close Add to Home tab
		test = self.driver.find_elements_by_xpath('//*[contains(text(), "Add Instagram to your Home screen?")]')
		if len(test) > 0:
			self.dummy_clicks('Close Add to HomePage', '//*[contains(text(), "Cancel")]')
		else:
			print("'Close Add to HomePage' not Encountered")

		# close notification tab
		test = self.driver.find_elements_by_xpath('//*[contains(text(), "Turn on Notifications")]')
		if len(test) > 0:
			self.dummy_clicks('Close Notification', '//*[contains(text(), "Not Now")]')
		else:
			print("'Close Notification' not Encountered")

		# close notification tab
		test = self.driver.find_elements_by_xpath('//*[contains(text(), "Action Blocked")]')
		if len(test) > 0:
			self.dummy_clicks('Action Blocked', '//*[contains(text(), "Action Blocked")]')
		else:
			print("'Action Blocked' not Encountered")

	# ######### Login Procedure Starts #########
	def login(self, username, password):
		self.dummy_clicks('Login Page Link', '//*[@id="react-root"]/section/main/article/div/div/div/div[2]/button')

		self.dummy_writes('Username', '//*[@id="react-root"]/section/main/article/div/div/div/form/div[4]/div/label/input', username)

		self.dummy_writes('Password', '//*[@id="react-root"]/section/main/article/div/div/div/form/div[5]/div/label/input', password)

		self.dummy_clicks('Login', '//*[@id="react-root"]/section/main/article/div/div/div/form/div[7]/button')

		self.close_extras()
	######### Login Procedure Ends #########

	######### Notification cheack Procedure Starts #########
	def check_notification(self):
		self.dummy_clicks('Notification', '//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[4]/a')
		print("Notification Page")

		# school to end of page
		ght = self.driver.execute_script("return document.body.scrollHeight")
		print("Page Height : {}".format(ght))

		follow_btns = []

		for i in range(round(int(ght/300))+1):
			print("Current Height : {}".format(i*300))
			self.driver.execute_script("window.scrollBy(0,500)")
			rand_Sleep(5,10)

			total_btns = self.driver.find_elements_by_xpath("//button[text()='Follow']")
			print("No. of Total Buttons : {}".format(len(total_btns)))

			following_btns = self.driver.find_elements_by_xpath("//button[text()='Following']")
			print("No. of Following Buttons : {}".format(len(following_btns)))

			current_follow_btns = [x for x in total_btns if x not in following_btns]
			print("No. of Current Follow Buttons : {}".format(len(current_follow_btns)))

			follow_btns.extend([x for x in current_follow_btns if x not in follow_btns])
			print("No. of Main Follow Buttons : {}".format(len(follow_btns)))

		rand_Sleep(10, 20)
		for i, btn in enumerate(follow_btns, 1):
			# check if action is blocked
			unfBtn = self.driver.find_elements_by_xpath('//*[contains(text(), "Unfollow")]')
			if len(unfBtn) > 0:
				following_btn = self.driver.find_elements_by_xpath('//button[contains(text(), "Cancel")]')
				self.dummy_clicks('Cancel', '//button[contains(text(), "Cancel")]')

			self.driver.execute_script("arguments[0].scrollIntoView()", btn)
			rand_Sleep(3, 6)

			print('JS click of #{} Follower Button'.format(i))
			self.driver.execute_script("arguments[0].click();", btn)
			rand_Sleep(3, 6)

			# check if action is blocked
			test = self.driver.find_elements_by_xpath('//*[contains(text(), "Action Blocked")]')
			if len(test) > 0:
				print('Action Blocked')
				break
			else:
				print('Action not Blocked yet')

		print("Notification Check Complete")

		# return to homepage
		self.dummy_clicks('Home', '//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[1]/a')
		rand_Sleep(3, 5)

		self.close_extras()
	######### Notification cheack Procedure Ends #########

	######### Notification cheack Procedure Starts #########
	def check_suggestion(self):
		self.dummy_clicks('Notification', '//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[4]/a')
		print("Suggestion Check")

		# notification section
		try:
			suggestion_section = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[3]/div/div')
		except Exception as e:
			pass
		else:
			print('Got Suggestions')
			suggestions = suggestion_section.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div[3]/div/div/div')[:10]
			rand_Sleep()

			random.shuffle(suggestions)
			for suggestion in suggestions[:5]:
				try:
					follow_btn = suggestion.find_element_by_tag_name('button')
				except Exception as e:
					pass
				else:
					if follow_btn.text == 'Follow':
						print('JS click of {} Button'.format("Follow Button"))
						self.driver.execute_script("arguments[0].click();", follow_btn)
						rand_Sleep(3, 6)

		# return to homepage
		self.dummy_clicks('Home', '//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[1]/a')
		rand_Sleep(3, 6)

		self.close_extras()
	######### Notification cheack Procedure Ends #########

	######### Upload Procedure Starts #########
	def upload_pic(self, image_path, caption, c_flag=1):
		self.dummy_clicks('Upload', '//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]', 2, [1, 1])

		###### for windows ######
		# handle file select
		# rand_Sleep(1, 2)
		# autokey.win_active("Open")
		# rand_Sleep(1, 2)
		# autokey.control_send("Open", "Edit1", image_path)
		# rand_Sleep(1, 2)
		# autokey.control_send("Open", "Edit1","{ENTER}")
		# rand_Sleep(1, 2)
		###### for windows ends ######

		###### for linex ######
		k = PyKeyboard()
		m = PyMouse()

		x_dim, y_dim = m.screen_size()

		for i in image_path:
			sleep(0.01)
			k.tap_key(i)

		rand_Sleep(1, 2)

		# to click open button
		m.click(x_dim-60, 50, 1)

		# to click browser button

		###### for linex ends ######
		m.click(20, y_dim-20, 1)
		rand_Sleep(2, 3)
		# image fit button
		try:
			img_fit_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/div[2]/div[2]/div/div/div/button[1]')
		except Exception as e:
			pass
		else:
			img_fit_class = str(img_fit_btn.find_element_by_tag_name('span').get_attribute('class'))
			print(img_fit_class)
			if "Expand" in img_fit_class:
				self.dummy_clicks('Next', '//*[@id="react-root"]/section/div[2]/div[2]/div/div/div/button[1]')

		# next button
		self.dummy_clicks('Next', '//*[@id="react-root"]/section/div[1]/header/div/div[2]/button')

		if c_flag == 1:
			# add fake location
			self.dummy_clicks('Add Location', '//*[@id="react-root"]/section/div[2]/section[2]/button')

			options = 0
			tr = 0
			while options == 0 and tr < 5:
				tr += 1
				self.dummy_writes('Location', '//*[@id="react-root"]/section/div[2]/input', self.faker.country())
				options = len(self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/div[3]/div/div/button'))

			if options == 0:
				self.dummy_clicks('Go Back', '//*[@id="react-root"]/section/div[1]/header/div/div[1]/button')
			else:			
				pick = random.randint(0, options)
				print('No. of Location picked is {}'.format(pick))			

				# pick a location
				rand_Sleep(3, 5)
				self.dummy_clicks('Pick Location', '//*[@id="react-root"]/section/div[3]/div/div/button[{}]'.format(pick))

		
		# write caption
		rand_Sleep(1, 2)

		for line in caption:
			self.dummy_writes('Caption', '//*[@id="react-root"]/section/div[2]/section[1]/div[1]/textarea', line, 2, [0, 0])
		rand_Sleep(1, 1)

		# share
		self.dummy_clicks('Share', '//*[@id="react-root"]/section/div[1]/header/div/div[2]/button')
		rand_Sleep(5, 10)

		self.close_extras()
	######### Upload Procedure Ends #########

	######### Photo Prephase Starts #########
	def photo(self, n_flag = 0, s_flag = 0, q_flag = 0, c_flag=1, author=''):
		#get famous joker quates
		if q_flag == 1:
			try:
				qu = open('{}quates.txt'.format(author), 'r')
			except:
				qu = open('quates.txt', 'r')

			quates = list(qu.read().splitlines())
			

		# Images
		images = os.listdir("Images/")
		print("{} Photos found in Upload Directory".format(len(images)))

		for i, image in enumerate(images):
			if(i%3 == 0):
				if n_flag == 1:
					# check notifications
					rand_Sleep(4, 6)
					self.check_notification()

				if s_flag == 1:
					# check suggestions
					rand_Sleep(4, 6)
					self.check_suggestion()

			print('Uploading Picture {}'.format(image))

			# Retriving random Quate
			if q_flag == 1:
				quate = select_random_quates(quates, author)
			else:
				quate = ''

			# making caption
			tags = ['Joker', 'Why So Serious', 'Arthur Fleck', 'Just a Comedian', 'Clown Prince of Crime']
			cc = 'Mr.J'
			caption = full_caption(quate, author, tags, cc)

			# Retriving Image Absolute path
			img_path = os.path.abspath("Images/{}".format(image))
			print('With Path {}'.format(img_path))

			self.upload_pic(img_path, caption, c_flag)
			rand_Sleep()

			# Remove Uploaded Image from Directory
			os.remove(img_path)
			print("On Break")
			rand_Sleep(60, 120)
	######### Photo Prephase Starts #########



def main():
	# taking inputs
	n_flag = int(input("Notification Cheack Flag (0 / 1) : "))
	s_flag = int(input("Suggestion Cheack Flag (0 / 1) : "))
	p_flag = int(input("Image Upload Flag (0 / 1) : "))
	q_flag = int(input("Image Caption Flag (0 / 1) : "))
	author = ''
	if q_flag == 1:			
		while author == '':
			author = str(input("Author of Quates: "))
			author = author.capitalize()
	c_flag = int(input("Country Flag (0 / 1) : "))

	# personal info
	username = 'Sexy_With_Madness'
	password = 'iamsingle'

	# Insatanciate Bot
	myInstaBot = InstaBot(username, password)

	if p_flag == 1:
		myInstaBot.photo(n_flag, s_flag, q_flag, c_flag, author)
	else:
		if n_flag == 1:
			# check notifications
			rand_Sleep(5, 7)
			myInstaBot.check_notification()

		if s_flag == 1:
			# check suggestions
			rand_Sleep(5, 7)
			myInstaBot.check_suggestion()



if __name__=="__main__":
	main()
