from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import make_response
import data
import pygal
import emailPecan

from flask import Flask, request, jsonify
import flask_excel as excel


#create app
app = Flask(__name__)
@app.route("/export", methods=['GET'])
def export_records():
    return excel.make_response_from_array([[1,2], [3, 4]], "xls", file_name="export_data")

# goes to login page when first opened
@app.route('/')
def goToLogin():
	return render_template("login.html")
@app.route('/getSurveyData/',methods=['POST'])
def downloadFile():
	email = request.form['email']
	surveyName = request.form['surveyName']
	fileType = request.form['fileType']
	if fileType == 'csv':
		response = make_response(data.getDataForForm(surveyName))
		surveyName = surveyName.replace(" ","")
		response.headers["Content-Disposition"] = "attachment; filename=DataFrom"+surveyName+".csv"
		return response
	else:
		return excel.make_response_from_array(data.getDataForFormArray(surveyName), "xls", file_name=surveyName)
@app.route('/', methods=['POST'])
def login():
	email = request.form['email']
	passW = request.form['passW']
	if data.loginUser(email,passW) == 1:
		username = data.getUserName(email)
		createdLinks, createdLinksName = data.getHubLinks(username)
		completedLinks, completedLinksName = data.getSubmittedLinks(username)
		savedLinks, savedLinksName = data.getSavedLinks(username)
		fullName = data.getFullName(email)
		first_name = fullName.split()[0]
		numNew = len(data.getCurrentSurveys())
		numClosed = len(data.getClosedSurveys())
		return render_template("home.html",email=email, completedLinks = completedLinks, completedLinksName = completedLinksName,first_name=first_name,createdLinks=createdLinks,createdLinksName=createdLinksName,savedLinks=savedLinks,savedLinksName=savedLinksName,numNew=numNew,numClosed=numClosed)
	return render_template("login.html",mess="Invalid Credentials",color="red")
@app.route('/home/',methods=['POST'])
def goHome():
	try:
		email = request.form['email']
		#print "email: "+email
		code = request.form['code']
		if code != "chini":
			return render_template("login.html",mess="Error Occured",color="red")
		username = data.getUserName(email)
		createdLinks, createdLinksName = data.getHubLinks(username)
		completedLinks, completedLinksName = data.getSubmittedLinks(username)
		savedLinks, savedLinksName = data.getSavedLinks(username)
		fullName = data.getFullName(email)
		first_name = fullName.split()[0]
		numNew = len(data.getCurrentSurveys())
		numClosed = len(data.getClosedSurveys())
		return render_template("home.html",email=email, completedLinks = completedLinks, completedLinksName = completedLinksName,first_name=first_name,createdLinks=createdLinks,createdLinksName=createdLinksName,savedLinks=savedLinks,savedLinksName=savedLinksName,numNew=numNew,numClosed=numClosed)
	except:
		return render_template("login.html",mess="Error Occured",color="red")
@app.route('/signUp/')
def goToSignUp():
	return render_template("signUp.html")

@app.route('/signUp/', methods=['POST'])
def signUp():
	email = request.form['email']
	passW = request.form['passW']
	fname = request.form['first_name']
	lname = request.form['last_name']
	check = data.signUpUser(email,passW,fname,lname)
	if check == 1:
		return render_template("login.html",mess="Account Created",color="green")
	if check == 2:
		return render_template("signUp.html",mess="Invalid Character",color="red")
	return render_template("signUp.html",mess="Username already in system",color="red")

@app.route('/manage/', methods=['POST'])
def goToManage():
	email = request.form['email']
	fullName = data.getFullName(email)
	return render_template("manage.html",email=email, fullName = fullName)

@app.route('/deleteAccount/', methods=["POST"])
def deleteUserAccount():
	email = request.form['email']
	passW = request.form['passW']
	if data.deleteAccount(email,passW) == 1:
		return render_template("login.html",mess="Account Deleted",color="red")
	return render_template("manage.html",mess="Incorrect Password",email=email)
@app.route('/addMailingList/', methods=["POST"])
def admailinglistforuser():
	email = request.form['email']
	emailList = request.form['emailList']
	nameOfList = request.form['nameOfList']
	fullName = data.getFullName(email)
	if data.addMailingList(email,emailList,nameOfList) == 1:
		return render_template("manage.html",mess="Error Occured",email = email,fullName=fullName)
	return render_template("manage.html",mess="Mailing List Added",email=email,fullName=fullName)
@app.route('/surveyWall/',methods=['POST'])
def goToSurveyWall():
	email = request.form['email']
	surveys = data.getCurrentSurveys()
	surveyLinks = []
	closedSurvey = data.getClosedSurveys()
	closedSurveyLinks = []
	for i in surveys:
		print i
		surveyLinks.append("http://127.0.0.1:5000/survey/"+i+"/")
	print "BREAK-----"
	for i in closedSurvey:
		print i
		closedSurveyLinks.append("http://127.0.0.1:5000/survey/"+i+"/")
	return render_template("surveyWall.html",email=email,surveys=surveys,surveyLinks=surveyLinks,closedSurvey=closedSurvey,closedSurveyLinks=closedSurveyLinks)

@app.route('/addSurvey/', methods=['POST'])
def goToAddSurvey():
	print "In add survey method"
	email = request.form['email']
	#print email
	return render_template("addSurveyPart1.html",email=email)

@app.route('/addSurvey2/',methods=['POST'])
def addSurveyPart2():
	#print "In add survey method 2"
	email = request.form['email']
	formTheme = request.form['formTheme']
	block = request.form['block']
	#print "1"
	contact = request.form['contact']
	date = request.form['date']
	
	notiNum = request.form['notiNum']
	print "Date: "+date
	print "Contact: "+contact
	formName = request.form['formName']
	notificationEmail = request.form['notificationEmail']

	if data.checkNameSurvey(formName) == 1:
		return render_template("addSurveyPart1.html",email=email,mess="Survey Name Taken")
	formlen = int(request.form['formlen'])
	if formTheme == "custom":
		return render_template("addSurveyHalf.html",email=email,formlen=formlen,formName=formName,contact=contact,date=date,notificationEmail=notificationEmail,notiNum = notiNum,formTheme=formTheme,block = block)
	#print "Last"
	vid = ""
	pic = ""
	surveyBackground = ""
	return render_template("addSurveyPart2.html",email=email,formlen=formlen,formName=formName,contact=contact,date=date,notificationEmail=notificationEmail,notiNum = notiNum,formTheme=formTheme,block = block,vid=vid,pic=pic,surveyBackground=surveyBackground)
@app.route('/deleteSurvey/',methods=['POST'])
def delteSurveyForUser():
	email = request.form['email']
	surveyName = request.form['surveyName']
	data.deleteSurvey(surveyName)
	surveys = data.getCurrentSurveys()
	surveyLinks = []
	print email
	for i in surveys:
		surveyLinks.append("http://127.0.0.1:5000/survey/"+i+"/")
	message="Survey Deleted"
	return render_template("surveyWall.html",email=email,surveys=surveys,surveyLinks=surveyLinks,message=message)

@app.route("/addSurveyHalf/",methods=['POST'])
def halfWaySurvey():
	email = request.form['email']
	formTheme = request.form['formTheme']
	block = request.form['block']
	#print "1"
	contact = request.form['contact']
	date = request.form['date']
	notiNum = request.form['notiNum']
	print "Date: "+date
	print "Contact: "+contact
	formName = request.form['formName']
	notificationEmail = request.form['notificationEmail']
	formlen = int(request.form['formlen'])
	surveyBackground = request.form['surveyBackground']
	pic = request.form['pic']
	vid = request.form['vid']
	return render_template("addSurveyPart2.html",email=email,formlen=formlen,formName=formName,contact=contact,date=date,notificationEmail=notificationEmail,notiNum = notiNum,formTheme=formTheme,block = block,vid=vid,pic=pic,surveyBackground=surveyBackground)
@app.route('/submitSurvey/',methods=['POST'])
def submitSurvey():
	#print "In submit survey"
	email = request.form['email']
	formName = request.form['formName']
	formTheme = request.form['formTheme']
	#print "2"
	block = request.form['block']
	formlen = int(request.form['formlen'])
	contact = request.form['contact']
	notiNum = int(request.form['notiNum'])
	date = request.form['date']
	notificationEmail = request.form['notificationEmail']
	#print "3"
	questions = []
	vid = request.form['vid']
	pic = request.form['pic']
	surveyBackground = request.form['surveyBackground']
	for i in range(formlen):
		questions.append(request.form['q'+str(i)])
	#print "4"
	if data.addSurvey(formName,email,questions,formlen,contact,date,notificationEmail,notiNum,formTheme,block,vid,pic,surveyBackground) == 1:
		link = "http://pecan.pythonanywhere.com/survey/"+formName+"/"
		return render_template("succ.html",link=link,email = email,formName=formName)
	return render_template("addSurveyPart2.html",email=email,formlen=formlen,formName=formName,mess="Error Occured")
@app.route('/emailFormCreated/',methods=['POST'])
def emailForYouCreated():
	link = request.form["link"]
	email = request.form["email"]
	formName=request.form["formName"]
	emailReps = request.form['emailReps']
	mailingLists = data.getMailingLists(email)
	emails = emailReps.split(",")
	for i in emails:
		if i in mailingLists:
			l = data.getMailingListResp(email,i)
			for k in l:
				print "Sending to "+k
				emailPecan.sendEmail("Check out my Survey '"+formName+"'","Respond to my survey at: "+link,k)
		else:
			print "Sending to "+i
			emailPecan.sendEmail("Check out my Survey '"+formName+"'","Respond to my survey at: "+link,i)
	message = "Emails Sent!"
	return render_template("succ.html",link=link,email = email,formName=formName,message=message)


@app.route('/survey/<name>/')
def loadSurvey(name):
	#print "in load"
	#print name
	block = data.getBlock(name)
	if len(block) != 0:
		return render_template("block.html")
	questions = data.getQuestionsForSurvey(name)
	formTheme = data.getFormTheme(name)

	print "Loading "+str(formTheme)
	length = len(questions)
	email = "noemail."
	#print questions[0]
	if formTheme == "themeA":
		return render_template("lavender.html",questions=questions,name=name,length=length,email=email)
	if formTheme == "themeB":
		return render_template("ocean.html",questions=questions,name=name,length=length,email=email)
	if formTheme == "custom":
		pics = data.getPicFromCutom(name)
		vid = data.getVidFromCutom(name)
		back = data.getBackFromCustom(name)
		return render_template("custom.html",questions=questions,name=name,length=length,email=email,pics=pics,vid=vid,back=back)
	return render_template("sunrise.html",questions=questions,name=name,length=length,email=email)


@app.route('/survey/<name>/',methods=['POST'])
def loadSurveyForUser(name):
	#print "in load"
	#print name

	questions = data.getQuestionsForSurvey(name)
	formTheme = data.getFormTheme(name)
	print "Loading "+str(formTheme)
	email = request.form['email']
	block = data.getBlock(name)
	if len(block) != 0:
		blockedUser = block.split(",")
		if email in blockedUser or data.getUserName(email) in blockedUser:
			return render_template("block.html")
	length = len(questions)
	#print questions[0]
	if formTheme == "themeA":
		return render_template("lavender.html",questions=questions,name=name,length=length,email=email)
	if formTheme == "themeB":
		return render_template("ocean.html",questions=questions,name=name,length=length,email=email)
	if formTheme == "custom":
		pics = data.getPicFromCutom(name)
		vid = data.getVidFromCutom(name)
		back = data.getBackFromCustom(name)

		return render_template("custom.html",questions=questions,name=name,length=length,email=email,pics=pics,vid=vid,back=back)
	return render_template("sunrise.html",questions=questions,name=name,length=length,email=email)

@app.route('/customtemplate/')
def customTemplate():
	return render_template("custom.html")

@app.route('/survey/<name>/response/', methods=['POST'])
def submitSurveyResponse(name):
	#print "Survey Submitted!"
	answers = []
	length = int(request.form['length'])

	for i in range(length):
		answers.append(request.form['q'+str(i)])
	#print answers
	data.submitResponse(name,answers)
	creatorContact = data.getSurveyContact(name)
	creator = ""
	if creatorContact != "h":
		creator = data.getFullName(creatorContact)

	link = "http://pecan.pythonanywhere.com/survey/"+name+"/"
	#print "1"
	email = request.form['email']
	notiEmail = data.getSurveyContactNoti(name)
	resps = str(data.getSurveyLen(name)+1)
	if data.getNotiData(name):
		emailPecan.sendEmail(resps+" People responded to your Survey!","Congrats! "+resps+" People responded to your Survey! Login in here to see more data: http://127.0.0.1:5000/",notiEmail)
	#print "2"
	if email != "noemail.":
		data.addSurveyComplete(email,name)
	return render_template("succSubmit.html",email=email,link=link,name=name,creator = creator,creatorContact=creatorContact)

@app.route('/surveyDetails/',methods=['POST'])
def getSurveyDetails():
	email = request.form['email']
	surveyName = request.form['surveyName']
	length = data.getNumResponses(surveyName)
	return render_template("surveyDetails.html",surveyName = surveyName,length=length,email=email)

@app.route('/surveyGraph1/', methods=['POST'])
def surveyGrpah1():
	email = request.form['email']
	surveyName = request.form['surveyName']
	ques = data.getQuestionsForSurvey(surveyName)
	return render_template("graph1.html",email=email,surveyName=surveyName,ques=ques)

@app.route("/graphSurvey/",methods=['POST'])
def graph_survey():
	email = request.form['email']
	surveyName = request.form['surveyName']
	question = request.form['question']
	graph = request.form['graph']
	q = data.getQuestionsForSurvey(surveyName)[int(question)]
	dictionary = data.getFormQuestionData(data.getFormData(surveyName),int(question))
	if graph == "pie":
		pie_chart = pygal.Pie()
		pie_chart.title = graph+" graph for question '"+q+"'"
		for key in dictionary:
			pie_chart.add(key, dictionary[key])
		return pie_chart.render_response()
	if graph == "pieD":
		pie_chart = pygal.Pie(inner_radius=.4)
		pie_chart.title = graph+" graph for question '"+q+"'"
		for key in dictionary:
			pie_chart.add(key, dictionary[key])
		return pie_chart.render_response()
	if graph == "pieR":
		pie_chart = pygal.Pie(inner_radius=.75)
		pie_chart.title = graph+" graph for question '"+q+"'"
		for key in dictionary:
			pie_chart.add(key, dictionary[key])
		return pie_chart.render_response()
	if graph == "barH":
		line_chart = pygal.HorizontalBar()
		line_chart.title = graph+" graph for question '"+q+"'"
		for key in dictionary:
			line_chart.add(key, dictionary[key])
		return line_chart.render_response()
	if graph == "barV":
		line_chart = pygal.Bar()
		line_chart.title = graph+" graph for question '"+q+"'"
		for key in dictionary:
			line_chart.add(key, dictionary[key])
		return line_chart.render_response()
	return graph+" for question #"+question

# run app
if __name__ == '__main__':
	app.run(debug=True)
