import pyrebase
import emailPecan
import time
import data
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


date = (time.strftime("%Y-%m-%d"))

forms = eval(getData("surveys"))
closed = eval(getData("closedSurveys"))
for i in closed:
	
	closed.remove(i)
	email = db.child(i).child("notificationEmail").get()
	email = str(email.val())
	userName = data.getUserName(email)
	userForms = db.child(userName).child("createdForms").get()
	userForms = str(userForms.val())
	userFormsArr = eval(userForms)
	userFormsArr.remove(i)
	emailPecan.sendEmail("Your survey '"+i+"' is now Closed and Deleted","Your survey '"+i+"' is now deleted.",email)
	db.child(userName).child("createdForms").set(str(userFormsArr))
	db.child(i).remove()

for i in forms:
	print i
	s = db.child(i).child("date").get()
	s = str(s.val())
	print i+": "+s
	if s == date:
		email = db.child(i).child("notificationEmail").get()
		email = str(email.val())
		emailPecan.sendEmail("Your survey '"+i+"' is now Closed","Your survey '"+i+"' is now closed and will be earased in 1 day. You have until tommorow to view/donwload your data. Login at: http://127.0.0.1:5000/",email)
		closed.append(i)
		forms.remove(i)

db.child("surveys").set(str(forms))
db.child("closedSurveys").set(str(closed))









