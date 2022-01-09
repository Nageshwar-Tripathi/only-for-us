from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Students, Semester, AdminData, Subjects, Course, Tutorials, PollSubmitted, Polls, ContactQueries
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

def index(request):
	return HttpResponse("Hello world")

def home(request):
	if request.session.has_key('username'):
		username = request.session['username']
		no_of_semesters = len(Semester.objects.all()) + 1
		no_of_tutorials = len(Tutorials.objects.all())
		data = {
			'username': username,
			'no_of_tutorials': no_of_tutorials,
			'no_of_semesters': no_of_semesters
		}
		return render(request, 'main/home.html', data)
	else:
		return redirect('/login/')

def my_account(request):
	if request.session.has_key('username'):
		username = request.session['username']

		student_details = Students.objects.get(username=username)
		data = {
			'username': username,
			'student': student_details,
		}
		return render(request, 'main/account.html', data)
	else:
		return redirect('/login/')

def about(request):
	if request.session.has_key('username'):
		username = request.session['username']
		data = {
			'username': username
		}
		return render(request, 'main/about.html', data)
	else:
		return redirect('/login/')

def semesters(request):
	if request.session.has_key('username'):
		username = request.session['username']

		all_semesters = Semester.objects.all()

		data = {
			'username' : username,
			'semesters': all_semesters,
		}

		return render(request, 'main/semesters.html', data)
	else:
		return redirect('/login/')

def login(request):
	if request.session.has_key('username'):
		return redirect('/home/')
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		try:
			find_user = Students.objects.get(username=username)
			user_password = find_user.password
		except:
			find_user = None

		if find_user != None and check_password(password, user_password):
			print("user logged in")
			request.session['username'] = find_user.username
			return redirect('/home/')

		elif find_user != None and user_password != password:
			messages.info(request, 'Incorrect Password!')

		else:
			messages.info(request, 'Username not Found!')

		return redirect('/login/')

	else:
		return render(request, 'main/login.html')


def register(request):
	if request.session.has_key('username'):
		return redirect('/home/')

	elif request.method == 'POST':
		fullname = request.POST['fullname']
		username = request.POST['username']
		email = request.POST['email']
		gender = request.POST['gender']
		course = request.POST['course']
		admission_id= request.POST['admission_id']
		password = request.POST['password']
		course_year = request.POST['course_year']

		data = {
			'username' : username,
			'email' : email,
			'fullname' : fullname,
		}

		valid_username = True
		invalid_characters = ".! #$%^&*()<>?/;:'=+-[]|\""

		for char in username:
			if(char in invalid_characters):
				valid_username = False

		if valid_username == False:
			messages.warning(request, 'Special Characters not allowed in Username!')
			return render(request, 'main/register.html', data)


		email_pre_exists = False
		username_pre_exists = False
		valid_password = True
		admission_id_pre_exists = False

		data_from_database = Students.objects.all()

		for user in data_from_database:
			if(user.email == email):
				email_pre_exists = True
				messages.warning(request, 'Email already exists!')
				return render(request, 'main/register.html', data)

		for user in data_from_database:
			if(user.username == username):
				username_pre_exists = True
				messages.warning(request, 'Username not available!')
				return render(request, 'main/register.html', data)

		for user in data_from_database:
			if(user.admission_no == admission_id):
				admission_id_pre_exists = True
				messages.warning(request, 'Admission Id is already registered!')
				return render(request, 'main/register.html', data)

		password_invalidity = 0

		length_of_password = len(password)
		if(length_of_password < 6):
			password_invalidity+=1

		if(password_invalidity!=0):
			valid_password = False
			messages.warning(request, 'Password length must be 6 or more!')
			return render(request, 'main/register.html', data)

		encrypted_password = make_password(password)

		registering_user = Students(
									username=username,
									email=email,
									fullname=fullname,
									gender=gender,
									course=course,
									admission_no=admission_id,
									password=encrypted_password,
									datetime=datetime.now(),
									course_year=course_year,
									)
		registering_user.save()
		print("user registered!!")
		request.session['username'] = username
		return redirect('/home/')
	return render(request, 'main/register.html')


def logout(request):
	if request.session.has_key('username'):
		try:
			del request.session['username']
			return redirect('/login/')
		except:
			pass
	return redirect('/')