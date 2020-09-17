#imports from django
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from django.contrib import messages

from django.utils import timezone
from django.contrib.auth.decorators import login_required

#Imports from this folder
from .models import (Quiz,Question,Answer,
					QuizAnalysis,StoredStudentAnswer)


					
class QuizListView(ListView):
    '''Class Based View for Product List'''
    template_name = 'quiz_app/quiz_list.html' #default is appname/model_list.html
    queryset      = Quiz.objects.all()


@login_required
def start_quiz(request,slug,ques_no):
	"""This function handles starting of quiz,
	finds the quiz object, updates QuizAnalysis to start time"""
	
	print("User asked for question number ",ques_no)
	user         = request.user
	msg          = ""
	quiz_object  = get_object_or_404(Quiz,slug=slug)
	start_time     = QuizAnalysis.objects.filter(user=user,quiz=quiz_object)
	if not start_time.exists():
		QuizAnalysis.objects.create(user=user,quiz=quiz_object,start=timezone.now())
	# try:
	print(quiz_object.questions.count(),ques_no-1)
	if quiz_object.questions.count() == ques_no-1:
		question_obj  = quiz_object.questions.all()[ques_no-2]
		next_question = ques_no
		msg           = "You have reached last question"
	elif quiz_object.questions.count() > ques_no-2:
		question_obj  = quiz_object.questions.all()[ques_no-1]  #Since python follows 0 based index so I am querying ques_no-1
		next_question = ques_no + 1


	answer_obj   = question_obj.answers.all()

	context      = {'quiz_object':quiz_object,
					'question_object':question_obj,
					'answer_object':answer_obj,
					'next_question':next_question,
					'msg':msg
					}
	return render(request,'quiz_app/start_quiz.html',context)




def check_correct(request,slug,ques_no):
	"""Check if the user submitted answer is right or wrong?"""
	right     = False
	first_try = False
	user        = request.user
	quiz_object = get_object_or_404(Quiz,slug=slug)
	student_answered = request.POST.get('answer_chosen')
	chosen_answer_id=request.POST.get('chosen_answer_id')

	try:
		question_obj   = quiz_object.questions.all()[ques_no]

		if not StoredStudentAnswer.objects.filter(user=user,quiz=quiz_object,question=question_obj).exists():
			first_try = True # if its the fist try by user then save his/her answer otherwise show answer but don't save

		answer_obj     = question_obj.answers.get(correct=True)
		correct_answer = answer_obj.answer
		right_answer_id= str(answer_obj.id)

		print(type(correct_answer))
		print(type(student_answered))
		if correct_answer == student_answered:
			right = True
			if first_try:
				StoredStudentAnswer.objects.get_or_create(user=user,quiz=quiz_object,question=question_obj,correct_answer=correct_answer,student_answered=student_answered,is_correct=True)
			return JsonResponse({'right':right,'right_answer':right_answer_id,'chosen_answer':chosen_answer_id})
		else:
			print("firsttt",first_try)
			if first_try:
				StoredStudentAnswer.objects.get_or_create(user=user,quiz=quiz_object,question=question_obj,correct_answer=correct_answer,student_answered=student_answered,is_correct=False)
			return JsonResponse({'right':right,'right_answer':right_answer_id,'chosen_answer':chosen_answer_id})
	except:
		return JsonResponse({'error':'error'})



@login_required
def submit(request,slug):
	user         = request.user
	quiz_object  = get_object_or_404(Quiz,slug=slug)
	score        = 0 
	total        = 0

	analysis     = QuizAnalysis.objects.filter(user=user,quiz=quiz_object)



	questions    = quiz_object.questions.all()
	for question_obj in questions:
		saved_answer = StoredStudentAnswer.objects.filter(user = user,question=question_obj)
		if saved_answer.exists():
			saved_answer = saved_answer.first()
			print(saved_answer.is_correct)
			if saved_answer.is_correct:
				score = score + 10
			total = total + 10

	analysis     = QuizAnalysis.objects.filter(user=user,quiz=quiz_object).first()
	if not analysis.completed:
		analysis.end = timezone.now()
		analysis.score= score
		analysis.completed = True
		analysis.save()

	stored = StoredStudentAnswer.objects.filter(user=user,quiz=quiz_object)
	if score >= total//2:
		success_msg = "You have <strong>Passed</strong> the test"
	else:
		success_msg = "<strong>Fail</strong>,Please Try later."

	context = {
	'score':score,
	'total':total,
	'quiz_object':quiz_object,
	'analysis':analysis,
	'stored_answer':stored,
	'success_msg':success_msg,
	} 
	return render(request,'quiz_app/score.html',context)



