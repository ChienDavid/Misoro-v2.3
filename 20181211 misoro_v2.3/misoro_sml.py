#!/usr/bin/env python
# license removed for brevity
#******************************************************************
#***************************** david ******************************
#******************************************************************
# Author        : Chien Van Dang
# Execution file: moral_reasoner.soar
#               : misoro2_3.py (previous version: misoro2_2.py)
# Updated date  : 11th Dec. 2018
# Application   : Soar Ethical Agent: top-down and bottom-up (3rd year)
# Update        : reduced inputs, integrated Emergency in mission
#******************************************************************
#******************************************************************
#==================================================================
import os
import sys
import rospy, time, thread
from datetime import date
from chatbot import chatbot
#dir = os.path.dirname(os.path.realpath(__file__))
#PATH_TO_SOAR = dir-"/../../"+"/SoarSuite960/"
PATH_TO_SOAR = "/home/airlab/ama/src/SoarSuite960/bin"
sys.path.append(PATH_TO_SOAR)
import Python_sml_ClientInterface as sml

#==================================================================
class misoro_sml:

	def __init__(self, agent_name, prog_path):

		self.agentName = agent_name
		self.SOAR_PROGRAM_PATH = prog_path

		self.newTask = "yes"
		self.mode = 1
		self.user_name = 'none'
		self.order_name = 'none'
		self.mission = 'new'
		self.guest = 'none'

		self.complaint = 'no'
		self.who_involved = 'none'
		self.what_involved = 'none'
		self.effect = 'none'

		self.situation = "none"
		self.target_person = "none"
		self.pre_food = "none"
		self.pre_user = "none"
		self.pre_priority = 0
		self.pre_act = "none"
		self.pre_emer_priority = 0
		self.pre_mission = "none"
		self.pre_behavior = "none"
		self.response_status = "none"
		self.behavior = "none"
		self.rl_dance = 0.0
		self.rl_sing = 0.0
		self.rl_play = 0.0
		self.alpha = 0.3	# learning rate
		self.gamma = 0.9	# discount rate
		self.q = 0.0		# learning policy (on-policy)

		self.member_list = ["Juho Kim", "Seonmi Lee", "Jinwoo Kim", "Mina Kim"]
		self.food_list = ["candy", "lemon juice", "cheese", "stir-fried anchovies", "rolled omelette", "shellfish", "strawberries", "orange juice", "cookie", "ice cream", "water", "onion", "banana", "milk", "vegetable"]
		self.game_list = ["toy", "liquid monster toy", "kitchen toys"]
		self.entertainment_list = ["entertainment"]
		self.info_list = ["wifi password", "home phone number", "phone number", "email address", "ID number", "credit card numbers", "date of birth"]
		self.errand_list = ["nothing"]
		self.emergency_list = ["heart attack", "bleeding"]

		self.chat = chatbot(self.user_name, self.agentName)
		self.time = date.today()
	#==================================================================
	def getRequest(self):
		incorrect = True
		while incorrect:
			request = raw_input("user: ")
			#print "request[:10] = %s" %request[:10]
			#print "request[:4] = %s" %request[:4]
			#print "request[:7] = %s" %request[:7]
			respond = self.chat.toChatScript(request)
			print "%s: %s" %(self.agentName, respond)

			#print "============================================"
			#print "Choose mode"
			#print "respond[:4] = %s" %respond[:4]
			if respond[:4] == "Okay":
				self.mode = 2
			#elif respond[:4] == "Sorry":
			#	self.mode = 1

			if respond[:10] == "Be careful":
				print "misoro: (contact to parents about this situation)"

			#print "============================================"
			#print "Get user"
			if request[:10] == "my name is":
				#print "Get user"
				user_res = str(respond[4:-20])
				if user_res in self.member_list:
					self.user_name = user_res
				else:
					user_res = str(respond[18:-21])
					self.user_name = "Stranger"
				#print "user_res: %s" %user_res
				#print "User: %s" %self.user_name

			#print "============================================"
			#print "Get service"
			if request[:7] == "give me" or request[:10] == "let's play" or request[:14] == "I want to play" or request[:6] == "I have" or request[:8] == "bring me" or request[:7] == "tell me":
				#print "Get service"
				self.order_name = str(respond[13:-1].lower())
				order_info = str(self.order_name.lower())
				order_game = str(respond[12:-13].lower())
				self.target_person = str(request[24:])
				order_emergency = str(respond[13:-1].lower())
				#print "order_name = %s" %self.order_name
				#print "order_game = %s" %order_game
				#print "order_info = %s" %order_info
				#print "target_person = %s" %self.target_person
				#print "order_emergency = %s" %order_emergency

				if self.order_name in self.emergency_list:
					self.mission = 'Emergency'
					self.situation = self.order_name
				elif self.order_name in self.food_list or order_game in self.game_list:
					if order_game in self.game_list:
						self.order_name = order_game
					self.mission = 'Delivery'
				elif self.order_name in self.entertainment_list:
					self.mission = 'Entertainment'
				elif self.order_name in self.info_list:
					self.mission = 'Information'
				elif self.order_name in self.errand_list:
					self.mission = 'Errand'
				#else:
				#	print "Fail"
				#print "Service: %s" %self.order_name
				#print "Mission: %s" %self.mission
			if request[4:-16] == "make" or request[4:-18] == "make" or request[19:-18] == "make" or request[19:-16] == "make" or request[-13:] == "too long time":
				self.complaint = 'yes'
				#print "self.complaint = %s" %self.complaint

			if self.mode == 2:
				if request == "I chop vegetable by a knife" or request == "yes, I took it from kitchen" or request == "the knife is sharp":
					print "#####################################################################"
					request = "who"
					respond = self.chat.toChatScript(request)
					print "who           : %s" %respond
					request = "what_DoAn"
					respond = self.chat.toChatScript(request)
					if respond.lower() in self.food_list:
						print "what (food)   : %s" %respond.lower() 
						request = "what_DoVat"
						respond = self.chat.toChatScript(request)
						print "what (object) : %s" %respond.lower()
						request = "how"
						respond = self.chat.toChatScript(request)
						print "how           : %s" %respond.lower()
						#request = "where_DiaDiem"
						#respond = self.chat.toChatScript(request)
						#print "where         : %s" %respond.lower()
					print "#####################################################################"

			if self.user_name != 'none' and self.order_name != 'none':
				if self.mission != 'new' or self.situation != 'none':
					request = "who"
					respond = self.chat.toChatScript(request)
					#print "who   : %s" %respond
					request = "what"
					respond = self.chat.toChatScript(request)
					#print "what  : %s" %respond.lower()
					request = "how"
					respond = self.chat.toChatScript(request)
					#print "how   : %s" %respond.lower()

					if self.complaint == 'yes':
						self.complaint = str("yes")
						request = "ai"
						respond = self.chat.toChatScript(request)
						self.who_involved = str(respond)
						request = "caigi"
						respond = self.chat.toChatScript(request)
						self.what_involved = str(respond.lower())
						request = "anhuong"
						respond = self.chat.toChatScript(request)
						self.effect = str(respond.lower())
						if self.effect != ["bad", "worse", "good", "better"]:
							self.effect = "none"
					else:
						self.complaint = "no"
						self.who_involved = "none"
						self.what_involved = "none"
						self.effect = "none"
					#print "complaint      : %s" %self.complaint
					#print "who involved   : %s" %self.who_involved
					#print "what involved  : %s" %self.what_involved
					#print "effect         : %s" %self.effect
					incorrect = False
			else:
				incorrect = True
			if respond == "See you!":
				incorrect = False
				self.mode = 0
				self.user_name = 'none'
				self.order_name = 'none'
				self.mission = 'new'
				self.guest = 'none'
				self.newTask = "no"

	#==================================================================
	def computeAge(self, dateOfBirth):
		year = int(dateOfBirth/10000)
		month = int((dateOfBirth%10000)/100)
		day = (dateOfBirth%10000)%100
		if year != 0:
			user_age = self.time.year - year + 1
		else:
			user_age = 0
		return user_age

	def updateRLRuleValues(self):
		update_value = 0.0

		if self.behavior == "dance":
			value = self.rl_dance
		elif self.behavior == "sing":
			value = self.rl_sing
		elif self.behavior == "play":
			value = self.rl_play

		if self.response_status == "like":
			reward = 1
		elif self.response_status == "dislike":
			reward = -1

		update_value = value + self.alpha*(reward + self.gamma*self.q - value)

		if self.behavior == "dance":
			self.rl_dance = update_value
		elif self.behavior == "sing":
			self.rl_sing = update_value
		elif self.behavior == "play":
			self.rl_play = update_value

	#==================================================================
	def entertainmentMission(self):
		if self.pre_behavior == "none":
			if self.behavior != "play":
				print "misoro: Okay. I will %s for %s" %(self.behavior, self.user_name)
			else:
				print "misoro: Okay. I will %s with %s" %(self.behavior, self.user_name)
		else:
			if self.pre_behavior != "play":
				print "misoro: Now, I will %s for %s" %(self.pre_behavior, self.pre_user)
			else:
				print "misoro: Now, I will %s with %s" %(self.pre_behavior, self.pre_user)
		self.inService()

	def deliveryMission(self):
		if self.user_name == "Stranger":
			user_name = "you"
			print "misoro: I will bring %s to %s" %(self.order_name, user_name)
		else:
			print "misoro: I will bring %s to %s" %(self.order_name, self.user_name)
		self.inService()

	#==================================================================
	def inputThread(self, L):
		raw_input(L)
		L.append(None)

	def inService(self):
		print "misoro: In service..."
		L = []
		delivery = ["Start", "--->", "   ", "--->", "   ", "--->", "   ", "--->", "   ", "--->", "Finish"]
		thread.start_new_thread(self.inputThread, (L,))
		i = 0
		incorrect = True
		while incorrect:
			if L:
				self.pre_act = "pending"
				print "misoro: The service is interrupted"
				incorrect = False
			if i < 11:
				time.sleep(1)
				i+=1
			if i == 11:
				self.pre_act = "accomplished"
				print "\nmisoro: The service is Finished!\n"
				incorrect = False
	#==================================================================
	def delAgent(self):
		self.kernel.Shutdown()
		del self.kernel

	def monitorState(self):
		io_cmd = 'print --depth 5 s1'
		checkio = self.agent.ExecuteCommandLine(io_cmd)
		return checkio

	def monitorSmem(self):
		smem_cmd = 'print @'
		checksmem = self.agent.ExecuteCommandLine(smem_cmd)
		return checksmem

	def saveAgent(self):
		save_cmd = 'save agent david'
		checksave = self.agent.ExecuteCommandLine(save_cmd)

	def inputSummary(self):
		print "\n#####################################################################"
		print "#####################################################################"
		print "   === Input Summary ===   "
		print ("User name   : %s" %self.user_name if self.guest == 'none' else "User name   : %s" %self.guest)
		print "Mission name: %s" %self.mission
		if self.mission == "Emergency":
			print "Situation   : %s" %self.situation
		elif self.mission == "Delivery":
			print "Order name  : %s" %self.order_name
		elif self.mission == "Entertainment":
			print "Reinforcement learning task"
		elif self.mission == "Information":
			if self.target_person in self.member_list:
				print "Request     : %s of %s" %(self.order_name, self.target_person)
			else:
				print "Request     : %s" %self.order_name
		print "#####################################################################"

	#==================================================================
	def runAgent(self):
		while self.newTask == "yes":

			self.kernel = sml.Kernel.CreateKernelInNewThread()
			if not self.kernel or self.kernel.HadError():
				print self.kernel.GetLastErrorDescription()
				exit(1)

			self.agent = self.kernel.CreateAgent(self.agentName)
			if not  self.agent:
				print  self.kernel.GetLastErrorDescription()
				exit(1)

			self.agentName = self.agent.GetAgentName()

			self.agent.LoadProductions(self.SOAR_PROGRAM_PATH)
			if self.agent.HadError():
				print self.agent.GetLastErrorDescription()
				exit(1)

			self.InputLink = self.agent.GetInputLink()
			self.OutputLink = self.agent.GetOutputLink()

			if self.response_status != "dislike":
				self.getRequest()
				if self.mode == 2:
					self.inputSummary()
			else:
				self.user_name = self.pre_user
				self.mission = 'Entertainment'
			# get new mission
			topId_get = self.agent.CreateIdWME(self.InputLink, "get")
			get_mission = self.agent.CreateStringWME(topId_get, "mission", self.mission)
			Id1_get = self.agent.CreateIdWME(topId_get, "user")
			get_user = self.agent.CreateStringWME(Id1_get, "user_name", self.user_name)
			Id2_get = self.agent.CreateIdWME(Id1_get, "order")
			get_order = self.agent.CreateStringWME(Id2_get, "order_name", self.order_name)
			Id3_get = self.agent.CreateIdWME(Id2_get, "include")
			get_sit = self.agent.CreateStringWME(Id3_get, "situation", self.situation)
			get_target_person = self.agent.CreateStringWME(Id3_get, "target_person", self.target_person)
			# save pre_order, pre_user, pre_priority, pre_emer_priority
			topId_save = self.agent.CreateIdWME(self.InputLink, "save")
			save_food = self.agent.CreateStringWME(topId_save, "pre_food", self.pre_food)
			Id1_save = self.agent.CreateIdWME(topId_save, "pre_user")
			save_user = self.agent.CreateStringWME(Id1_save, "pre_user", self.pre_user)
			save_priority = self.agent.CreateIntWME(Id1_save, "pre_priority", self.pre_priority)
			save_emer_priority = self.agent.CreateIntWME(Id1_save, "pre_emer_priority", self.pre_emer_priority)
			Id2_save = self.agent.CreateIdWME(Id1_save, "pre_action")
			save_act = self.agent.CreateStringWME(Id2_save, "pre_act", self.pre_act)
			# Complaint
			topId_complaint = self.agent.CreateIdWME(self.InputLink, "complaint")
			input_complaintSTT = self.agent.CreateStringWME(topId_complaint, "complaintSTT", self.complaint)
			input_whoInvolved = self.agent.CreateStringWME(topId_complaint, "whoInvolved", self.who_involved)
			input_whatInvolved = self.agent.CreateStringWME(topId_complaint, "whatInvolved", self.what_involved)
			input_effect = self.agent.CreateStringWME(topId_complaint, "effect", self.effect)
			# RL
			topId_rl = self.agent.CreateIdWME(self.InputLink, "rl")
			input_rl_dance = self.agent.CreateFloatWME(topId_rl, "rl_dance", self.rl_dance)
			input_rl_sing = self.agent.CreateFloatWME(topId_rl, "rl_sing", self.rl_sing)
			input_rl_play = self.agent.CreateFloatWME(topId_rl, "rl_play", self.rl_play)

			self.kernel.RunAllAgentsForever()
			#self.saveAgent()
			self.OutputLink = self.agent.GetOutputLink()

			if self.OutputLink:
				numchild = self.OutputLink.GetNumberChildren()
				for i in range(numchild):
					LinkChild = self.OutputLink.GetChild(i)
					att = LinkChild.GetAttribute()
					# monitor user information
					if att == "user_name":
						self.user_name = LinkChild.GetValueAsString()
					elif att == "user_position":
						user_position = LinkChild.GetValueAsString()
					elif att == "user_gender":
						user_gender = LinkChild.GetValueAsString()
					elif att == "user_dateOfBirth":
						user_dateOfBirth = int(LinkChild.GetValueAsString())
					elif att == "user_disease":
						user_disease = LinkChild.GetValueAsString()
					elif att == "user_normal_priority":
						user_normal_priority = int(LinkChild.GetValueAsString())
					elif att == "user_emergency_priority":
						user_emergency_priority = int(LinkChild.GetValueAsString())
					elif att == "mission":
						self.mission = LinkChild.GetValueAsString()
					elif att == "endMission":
						endMission = LinkChild.GetValueAsString()
					elif att == "user_phone_no":
						user_phone_no = LinkChild.GetValueAsString()
					elif att == "user_hobby":
						user_hobby = LinkChild.GetValueAsString()
					elif att == "user_weakness":
						user_weakness = LinkChild.GetValueAsString()
					# monitor item information
					elif att == "game_name":
						game_name = LinkChild.GetValueAsString()
					elif att == "food_name":
						food_name = LinkChild.GetValueAsString()
					elif att == "food_type":
						food_type = LinkChild.GetValueAsString()
					elif att == "food_status":
						food_status = LinkChild.GetValueAsString()
					elif att == "food_ingredient":
						food_ingredient = LinkChild.GetValueAsString()
					elif att == "food_nutrient":
						food_nutrient = LinkChild.GetValueAsString()
					elif att == "disease_worsened1":
						disease_worsened1 = LinkChild.GetValueAsString()
					elif att == "disease_worsened2":
						disease_worsened2 = LinkChild.GetValueAsString()
					elif att == "disease_worsened3":
						disease_worsened3 = LinkChild.GetValueAsString()
					# complaint
					elif att == "complaintSTT":
						out_complaintSTT = LinkChild.GetValueAsString()
					elif att == "who_involved":
						out_who_involved = LinkChild.GetValueAsString()
					elif att == "what_involved":
						out_what_involved = LinkChild.GetValueAsString()
					elif att == "effect":
						out_effect = LinkChild.GetValueAsString()
					# monitor evaluation
					elif att == "person":
						person = LinkChild.GetValueAsString()
					elif att == "request_phone_no":
						request_phone_no = int(LinkChild.GetValueAsString())
					elif att == "request_hobby":
						request_hobby = LinkChild.GetValueAsString()
					elif att == "request_weakness":
						request_weakness = LinkChild.GetValueAsString()
					elif att == "request_wifiPassword":
						request_wifiPassword = LinkChild.GetValueAsString()
					elif att == "authorization":
						authorization = LinkChild.GetValueAsString()
					elif att == "is_item_good_for_health":
						is_item_good_for_health = LinkChild.GetValueAsString()
					elif att == "behavior":
						self.behavior = LinkChild.GetValueAsString()
					elif att == "score_dance":
						score_dance = float(LinkChild.GetValueAsString())
					elif att == "score_sing":
						score_sing = float(LinkChild.GetValueAsString())
					elif att == "score_play":
						score_play = float(LinkChild.GetValueAsString())
					elif att == "obey":
						obey_score = int(LinkChild.GetValueAsString())
					elif att == "disobey":
						disobey_score = int(LinkChild.GetValueAsString())
					elif att == "mdecision":
						mdecision = LinkChild.GetValueAsString()
					# monitor emergency cases
					elif att == "emergency_situation":
						emer_situation = LinkChild.GetValueAsString()
					elif att == "emergency_action1":
						emer_action1 = LinkChild.GetValueAsString()
					elif att == "emergency_action2":
						emer_action2 = LinkChild.GetValueAsString()
					elif att == "emergency_action3":
						emer_action3 = LinkChild.GetValueAsString()
					# Response
					elif att == "act_name":
						act_name = LinkChild.GetValueAsString()
					elif att == "extra_act":
						extra_act = LinkChild.GetValueAsString()
					elif att == "recommend1":
						recommend1 = LinkChild.GetValueAsString()
					elif att == "recommend2":
						recommend2 = LinkChild.GetValueAsString()
					elif att == "recommend3":
						recommend3 = LinkChild.GetValueAsString()

				user_age = self.computeAge(user_dateOfBirth)

				#io_cmd = 'print --depth 5 i1'
				#checkio = agent.ExecuteCommandLine(io_cmd)
				#smem_cmd = 'print @'
				#smem_cmd = 'smem --print'
				#checksmem = self.agent.ExecuteCommandLine(smem_cmd)
				#print "\n SMem structures\n" + checksmem


				if self.mode == 2:
					if self.response_status != "dislike":
						# display on screen
						print "   === Agent's Retrieving ===   "
						print "***User information***"
						print "Identification  : %s" %self.user_name
						print ("Age             : %s" %user_age if user_age != 0 else "Age             : unknown")
						print "Gender          : %s" %user_gender
						print "Position        : %s" %user_position
						print "Current disease : %s" %user_disease
						print "Normal priority : %s" %user_normal_priority
						print "Emer. priority  : %s" %user_emergency_priority
						if self.mission == "Information" and self.user_name != "Stranger":
							print ("Phone number    : %s" %user_phone_no if user_phone_no != '0' else "Phone number    : unknown")
							print ("Hobby           : %s" %user_hobby if user_hobby != 'none' else "Hobby           : unknown")
							print ("Weakness        : %s" %user_weakness if user_weakness != 'none' else "Weakness        : unknown")
						#print "+++"
						#if emergency_status == "no": print "***Mission name : %s" %mission
						#print "***End mission  : %s" %endMission
						#print "+++"
						if self.mission == "Emergency":
							print "\n***Emergency***"
							print "Situation: %s" %emer_situation
							print "Action 1 : %s" %emer_action1
							print "Action 2 : %s" %emer_action2
							print "Action 3 : %s" %emer_action3
						else:
							if self.mission == "Delivery":
								print "\n***Delivery service***"
								print ("Item name       : %s" %game_name if food_name == "none" else "Item name       : %s" %food_name)
								print "Type            : %s" %food_type
								print "Status          : %s" %food_status
								print "Ingredient      : %s" %food_ingredient
								print "Nutrient        : %s" %food_nutrient
								print "Disease worsened: %s" %disease_worsened1,
								if disease_worsened2 != "no2":
									print ", %s" %disease_worsened2,
								if disease_worsened3 != "no3":
									print ", %s" %disease_worsened3
								else:
									print ""
							elif self.mission == "Entertainment":
								print "\n***Entertainment service***"
							elif self.mission == "Information":
								print "\n***Information service***"
								print "Information request: %s" %self.order_name
								print ("Target info        : %s" %person if person else "Target info        : home")
								print "Phone number       : %s" %request_phone_no
								print "Hobbies            : %s" %request_hobby
								print "Weakness           : %s" %request_weakness
								print "Authorization      : %s" %authorization
								print "Wifi password      : %s" %request_wifiPassword
							if self.complaint == "yes":
								print "\n***Complaint***"
								print "ComplaintSTT   : %s" %out_complaintSTT
								print "Who involved   : %s" %out_who_involved
								print "What involved  : %s" %out_what_involved
								#print "Effect         : %s" %out_effect
						# Reasoning
						print "\n   === Agent's Reasoning ===   "
						if self.mission == "Delivery":
							print "Good item?      : %s" %is_item_good_for_health
						print "Obey score      : %s" %obey_score
						print "Disobey score   : %s" %disobey_score
						if self.pre_act == "pending":
							print "Priority of %s is %s" %(self.pre_user, self.pre_priority)
							print "Priority of %s is %s" %(self.user_name, user_emergency_priority)
						if self.mission == "Entertainment":
							#print "Score dance   : %s" %score_dance
							#print "Score sing    : %s" %score_sing
							rl_cmd = 'print --rl'
							checkrl = self.agent.ExecuteCommandLine(rl_cmd)
							print "\nUpdate RL rule values" + "\n" + checkrl
						# Response
						print "\n   === Agent's Response ===   "
						print "Moral decision  : %s" %mdecision
						#if mission == "Delivery" and mdecision == "disobey":
						#	print "recommend1      : %s" %recommend1
						#	print "recommend2      : %s" %recommend2
						#	print "recommend3      : %s" %recommend3
						#elif mission == "Entertainment":
						#	print "Behavior        : %s" %behavior
						if extra_act != "none":
							print "Notification    : %s, %s" %(self.user_name, extra_act)
						print "#####################################################################"
						print "#####################################################################\n"
					else:
						print "\n#####################################################################"
						print "#####################################################################"
						print "   === Agent's Reasoning ===   "
						rl_cmd = 'print --rl'
						checkrl = self.agent.ExecuteCommandLine(rl_cmd)
						print "Update RL rule values" + "\n" + checkrl
						# Response
						print "   === Agent's Response ===   "
						print "Moral decision  : %s" %mdecision
						if self.mission == "Delivery" and mdecision == "disobey":
							print "recommend1      : %s" %recommend1
							print "recommend2      : %s" %recommend2
							print "recommend3      : %s" %recommend3
						elif self.mission == "Entertainment":
							print "Behavior        : %s" %self.behavior
						if extra_act != "none":
							print "Notification    : %s, %s" %(self.user_name, extra_act)
						print "#####################################################################"
						print "#####################################################################\n"

				if mdecision == "obey":
					if extra_act == "none":
						#print "Case 1"
						if self.mission == "Emergency":
							print "misoro: Okay. I will %s to %s" %(emer_action3, self.user_name)
							self.inService()
						elif self.mission == "Delivery":
							self.deliveryMission()
							self.newTask = "no"
						elif self.mission == "Entertainment":
							if self.behavior != "play":
								print "misoro: Shall I %s for you?" %self.behavior
							else:
								print "misoro: Shall I %s with you?" %self.behavior
							response = raw_input("user: ")
							if response == "yes" or response == "YES" or response == "Y" or response == "y" or response == "":
								self.response_status = "like"
								self.updateRLRuleValues()
								self.entertainmentMission()
								self.newTask = "no"
							else:
								self.response_status = "dislike"
								self.updateRLRuleValues()
								self.pre_user = self.user_name
								self.newTask = "yes"
						elif self.mission == "Information":
							if self.order_name != "wifi password":
								print "misoro: %s of %s is %s\n" %(self.order_name,self.target_person,request_phone_no)
							else:
								print "misoro: %s is '%s'\n" %(self.order_name,request_wifiPassword)
							self.newTask = "no"
					elif extra_act == "your order will be served FIRST":
						#print "Case 2.1"
						if self.mission == "Emergency":
							print "misoro: Okay. I will %s to %s" %(emer_action3, self.user_name)
							self.inService()
						else:
							if self.mission == "Delivery":
								self.deliveryMission()
						#print "Case 2.2"
						if self.pre_mission == "Delivery":
							self.user_name, self.pre_user = self.pre_user, self.user_name
							self.order_name, self.pre_food = self.pre_food, self.order_name
							self.deliveryMission()
							self.user_name, self.pre_user = self.pre_user, self.user_name
							self.order_name, self.pre_food = self.pre_food, self.order_name
						elif self.pre_mission == "Entertainment":
							self.entertainmentMission()
						self.newTask = "no"
					elif extra_act == "your order will be served NEXT":
						#print "Case 3.1"
						if self.pre_mission == "Delivery":
							self.user_name, self.pre_user = self.pre_user, self.user_name
							self.order_name, self.pre_food = self.pre_food, self.order_name
							self.deliveryMission()
							self.user_name, self.pre_user = self.pre_user, self.user_name
							self.order_name, self.pre_food = self.pre_food, self.order_name
						#print "Case 3.2"
						if self.mission == "Delivery":
							self.deliveryMission()
							self.newTask = "no"
						elif self.mission == "Entertainment":
							if self.behavior != "play":
								print "misoro: Shall I %s for you, %s?" %(self.behavior, self.user_name)
							else:
								print "misoro: Shall I %s with you, %s?" %(self.behavior, self.user_name)
							response = raw_input("user: ")
							if response == "yes" or response == "YES" or response == "Y" or response == "y" or response == "":
								self.response_status = "like"
								self.updateRLRuleValues()
								self.entertainmentMission()
								self.newTask = "no"
							else:
								self.response_status = "dislike"
								self.updateRLRuleValues()
								self.pre_user = self.user_name
								self.newTask = "yes"
				elif mdecision == "disobey":
					if self.mission == "Delivery":
						if game_name != "none":
							print "misoro: %s is NOT good for your %s" %(game_name, user_disease)
						else:
							print "misoro: %s is NOT good for your %s" %(food_name, user_disease)
						print "misoro: The service is Finished!\n"
						self.newTask = "no"
					elif self.mission == "Information":
						print "misoro: Sorry! You are not allowed"
						print "misoro: The service is finished.\n"
						self.newTask = "no"
				if self.newTask == "no":
				   # save pre_order, pre_user, pre_priority
					self.pre_mission = self.mission
					self.pre_food = self.order_name
					self.pre_user = self.user_name
					self.pre_priority = user_normal_priority
					self.pre_emer_priority = user_emergency_priority
					self.pre_behavior = self.behavior
				   # start a new task
					self.newTask = "yes"

			request = "new task"
			respond = self.chat.toChatScript(request)
			print "%s: %s" %(self.agentName, respond)
			self.mission = 'new'
			self.situation = 'none'

			self.delAgent()

