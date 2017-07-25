import pyrebase
import writeCSV
import emailPecan
import datetime
config = {
  "apiKey": "API_KEY",
  "authDomain": "pecan-9d633.firebaseapp.com",
  "databaseURL": "https://pecan-9d633.firebaseio.com",
  "storageBucket": "pecan-9d633.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
def getData(name):
	dat = db.child(name).get()
	s = str(dat.val())
	if s.startswith("OrderedDict") == False:
		return s
	return s
def getDataForForm(name):
	q = db.child(name).child("questions").get()
	q = str(q.val())
	questions = eval(q)
	#print questions
	result = ','.join(questions)
	r = db.child(name).child("responses").get()
	r = str(r.val())
	resp = eval(r)
	for i in resp:
		s = ','.join(i)
		result = result+"\n"+s
	return result
def getDataForFormArray(name):
	q = db.child(name).child("questions").get()
	q = str(q.val())
	questions = eval(q)
	#print questions
	result = ','.join(questions)
	r = db.child(name).child("responses").get()
	r = str(r.val())
	resp = eval(r)
	res = []
	res.append(questions)
	for i in resp:
		res.append(i)
	return res
#print getDataForForm("Resposssss")
def deleteSurvey(i):
	forms = eval(getData("surveys"))
	forms.remove(i)
	email = db.child(i).child("notificationEmail").get()
	email = str(email.val())
	userName = getUserName(email)
	userForms = db.child(userName).child("createdForms").get()
	userForms = str(userForms.val())
	userFormsArr = eval(userForms)
	userFormsArr.remove(i)
	emailPecan.sendEmail("Your survey '"+i+"' is now Closed and Deleted","Your survey '"+i+"' is now deleted.",email)
	db.child(userName).child("createdForms").set(str(userFormsArr))
	db.child(i).remove()
	db.child("surveys").set(str(forms))
def loginUser(name,passW):
	users = eval(getData("users"))
	passwords = eval(getData("passwords"))
	for i in range(len(users)):
		if users[i] == name:
			if passwords[i] == passW:
				return 1
			else:
				return 0
	return 0
def exportToCSV(name):
	s = db.child(name).child("questions").get()
	s = str(s.val())
	header = eval(s)
	print header
	s = db.child(name).child("responses").get()
	s = str(s.val())
	resp = eval(s)
	res = header+resp
	return writeCSV.writeCSVFile(res)
#exportToCSV("Email")
def signUpUser(email,passW,first_name,last_name):
	try:
		fullName = first_name+ " "+last_name
		users = eval(getData("users"))
		for i in users:
			if i == email:
				return 0
		passwords = eval(getData("passwords"))
		users.append(email)
		passwords.append(passW)

		userName = getUserName(email)
		db.child(userName).child("createdForms").set("[]")
		db.child(userName).child("submittedForms").set("[]")
		db.child(userName).child("savedForms").set("[]")
		db.child(userName).child("name").set(fullName)
		db.child(userName).child("email").set(email)
		db.child(userName).child("mailingList").set("[]")
		db.child("passwords").set(str(passwords))
		db.child("users").set(str(users))
		return 1
	except:
		return 2
def getUserEmail(name):
	s = db.child(name).child("email").get()
	s = str(s.val())
	return s

def getUserName(email):
	email = email.replace("@","").replace(".","")
	return email


def getFullName(email):
	userName = getUserName(email)
	s = db.child(userName).child("name").get()
	s = str(s.val())
	return s
#print getUserName("abirshukla@gmail.com")

def deleteAccount(name,passW):
	users = eval(getData("users"))
	passwords = eval(getData("passwords"))
	for i in range(len(users)):
		if users[i] == name:
			if passwords[i] == passW:
				users.remove(name)
				passwords.remove(passW)
				db.child("users").set(str(users))
				userName = getUserName(name)
				db.child("passwords").set(str(passwords))
				s = db.child(userName).child("createdForms").get()
				s = str(s.val())
				forms = eval(s)
				globalForms = eval(getData("surveys"))
				for i in forms:
					db.child(i).remove()
					globalForms.remove(i)
				db.child("surveys").set(str(globalForms))
				db.child(userName).remove()
				return 1
			else:
				return 0
	return 0
#deleteAccount("test","Breh")
def getSurveyContact(name):
	s = db.child(name).child("contact").get()
	s = str(s.val())
	return s
def getSurveyContactNoti(name):
	s = db.child(name).child("notificationEmail").get()
	s = str(s.val())
	return s
def getSurveyLen(name):
	s = db.child(name).child("notiNum").get()
	s = str(s.val())
	data = eval(s)
	return data[0]
def checkNameSurvey(name):
	surveys = eval(getData("surveys"))
	for i in surveys:
		if i == name:
			return 1
	return 0
#db.child("test").remove()

def addSurvey(name,email,questions,formLen,contact,date,notificationEmail,notiNum,formTheme,block,vid,pic,surveyBackground):
	try:
		userName = getUserName(email)
		s = db.child(userName).child("createdForms").get()
		s = str(s.val())
		forms = eval(s)
		#print forms
		forms.append(name)
		db.child(userName).child("createdForms").set(str(forms))
		globalForms = eval(getData("surveys"))

		
		
		today = datetime.date.today()
		tomm = today + datetime.timedelta(days=1)
		if str(today) == date or str(tomm) == date:
			closedSur = eval(getData("closedSurveys"))
			closedSur.append(name)
			db.child("closedSurveys").set(str(closedSur))
		else:
			globalForms.append(name)
			db.child("surveys").set(str(globalForms))

		db.child(name).child("length").set(str(formLen))

		db.child(name).child("questions").set(str(questions))
		db.child(name).child("responses").set("[]")
		db.child(name).child("contact").set(contact)
		db.child(name).child("date").set(date)
		db.child(name).child("formTheme").set(formTheme)
		db.child(name).child("notificationEmail").set(notificationEmail)
		db.child(name).child("block").set(block)
		noti = [0,notiNum]
		db.child(name).child("notiNum").set(str(noti))
		if formTheme != "custom":
			return 1
		db.child(name).child("vid").set(vid)
		db.child(name).child("pic").set(pic)
		db.child(name).child("surveyBackground").set(surveyBackground)
		return 1
	except:
		return 0
def getFormTheme(name):
	s = db.child(name).child("formTheme").get()
	s = str(s.val())
	return s
def getMailingLists(email):
	userName = getUserName(email)
	s = db.child(userName).child("mailingList").get()
	s = str(s.val())
	data = eval(s)
	return data
def getBlock(name):
	s = db.child(name).child("block").get()
	s = str(s.val())
	return s

def getMailingListResp(email,nameOfList):
	userName = getUserName(email)
	s = db.child(userName).child(nameOfList).get()
	s = str(s.val())
	data = s.split(",")
	return data
def addMailingList(email,emailList,nameOfList):
	try:
		userName = getUserName(email)
		s = db.child(userName).child("mailingList").get()
		s = str(s.val())
		data = eval(s)
		if nameOfList in data:
			#print str(db.child(userName).child(nameOfList).get())
			s = db.child(userName).child(nameOfList).get()
			s = str(s.val())
			data = s.split(",")
			#data = eval(s)
			emails = emailList.split(",")
			for i in emails:
				data.append(i)
			#data.append(nameOfList)
			#db.child(userName).child("mailingList").set(str(data))
			db.child(userName).child(nameOfList).set(str(data))
			return 0
		else:
			data.append(nameOfList)
			db.child(userName).child("mailingList").set(str(data))
			db.child(userName).child(nameOfList).set(str(emailList))
			return 0
	except:
		return 1
#print addMailingList("shukla14@purdue.edu","abirshukla@gmail.com,aadishukla@gmail.com,123@123.com","test222Mail")
def getCurrentSurveys():
	globalForms = eval(getData("surveys"))
	return globalForms
def getClosedSurveys():
	closedForms = eval(getData("closedSurveys"))
	return closedForms
#print getCurrentSurveys()
def getQuestionsForSurvey(name):
	s = db.child(name).child("questions").get()
	s = str(s.val())
	res = eval(s)
	return res
def getPicFromCutom(name):
	s = db.child(name).child("pic").get()
	s = str(s.val())
	res = s.split(",")
	return res
def getVidFromCutom(name):
	s = db.child(name).child("vid").get()
	s = str(s.val())
	return s
def getBackFromCustom(name):
	s = db.child(name).child("surveyBackground").get()
	s = str(s.val())
	return s

def getNotiData(name):
	try:
		s = db.child(name).child("notiNum").get()
		s = str(s.val())
		data = eval(s)
		res = db.child(name).child("responses").get()
		res = str(res.val())
		length = len(eval(res))
		print length
		if length%data[1] == 0 and length != data[0]:
			data[0] = length
			db.child(name).child("notiNum").set(str(data))
			return True
		else:
			return False
	except:
		return False
#print getQuestionsForSurvey("Abir's Form")

# @param name: username of the user
# returns an array of links to the survey
def getHubLinks(name):
    s = db.child(name).child("createdForms").get()
    s = str(s.val())
    surveys = eval(s)
    linkArray = []
    surveyNames = []
    for survey in surveys:
        linkArray.append("http://127.0.0.1:5000/survey/" + survey + "/")
        surveyNames.append(survey)
    return linkArray, surveyNames

def getSubmittedLinks(name):
    s = db.child(name).child("submittedForms").get()
    s = str(s.val())
    surveys = eval(s)
    linkArray = []
    surveyNames = []
    for survey in surveys:
        linkArray.append("http://127.0.0.1:5000/survey/" + survey + "/")
        surveyNames.append(survey)
    return linkArray, surveyNames

def getSavedLinks(name):
    s = db.child(name).child("savedForms").get()
    s = str(s.val())
    surveys = eval(s)
    linkArray = []
    surveyNames = []
    for survey in surveys:
        linkArray.append("http://127.0.0.1:5000/survey/" + survey + "/")
        surveyNames.append(survey)
    return linkArray, surveyNames

def submitResponse(name,responses):
	s = db.child(name).child("responses").get()
	s = str(s.val())
	res = eval(s)
	res.append(responses)
	db.child(name).child("responses").set(str(res))
	return 1

def addSurveyComplete(email,name):
	userName = getUserName(email)
	s = db.child(userName).child("submittedForms").get()
	s = str(s.val())
	forms = eval(s)
	forms.append(name)
	db.child(userName).child("submittedForms").set(str(forms))
def getNumResponses(name):
	s = db.child(name).child("responses").get()
	s = str(s.val())
	res = eval(s)
	return len(res)
def getFormData(name):
	s = db.child(name).child("responses").get()
	s = str(s.val())
	resp = eval(s)
	return resp
def getFormQuestionData(resp,index):
	res = []
	for i in resp:
		res.append(i[index])
	dictionary = {}
	for i in res:
		if dictionary.has_key(i) == False:
			dictionary[i] = ((float(res.count(i))/float(len(res)))*100)
	return dictionary
#print getFormQuestionData(getFormData("Test"),1)

#addSurveyComplete("shukla14@purdue.edu","food test breh")
