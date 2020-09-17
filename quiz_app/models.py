from django.db import models
from django.conf import settings
from django.utils.text import slugify


#Third Party imports
from ckeditor.fields import RichTextField


SUBJECT_CHOICES = (
	('1','Physics'),
	('2','Chemistry'),
	('3','Programming'),
	('4','Frontend'),
	('5','Backend'),
)


class Quiz(models.Model):
	"""This model is the one that handles making of quiz"""

	user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	title           = models.CharField(max_length=200)
	slug            = models.SlugField(unique=True,blank=True,
						null=True,help_text="let it be empty",db_index=True)
	# Used db_index for faster query resolving 
	subject         = models.CharField(max_length=29,default='1',
						choices = SUBJECT_CHOICES)
	total_question  = models.PositiveSmallIntegerField(default=10)
	created         = models.DateField(auto_now_add=True)
	is_active       = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Quiz'
		verbose_name_plural = 'Quizs'
		ordering = ['-created']

	def save(self):
		if not self.id:
			self.slug = slugify(self.title)
		super(Quiz, self).save()

	def __str__(self):
		return str(self.title)[:20]

	def get_absolute_url(self):
		return "/{slug}/1/".format(slug=self.slug)


#########--------------Question Model--------------###############

class Question(models.Model):
	quiz           = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="questions")
	question       = RichTextField()

	def __str__(self):
		return str(self.question)[:20]



#######-------------------Answer Model---------------##############

class Answer(models.Model):
	question       = models.ForeignKey(Question,on_delete=models.CASCADE,related_name="answers")
	answer         = models.CharField(max_length=255)
	correct        = models.BooleanField(default=False)

	def __str__(self):
		return str(self.question)[:20]



#######------------------QuizAnalysis---------------#################

class QuizAnalysis(models.Model):
	user           = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	quiz           = models.ForeignKey(Quiz,on_delete=models.CASCADE)
	score          = models.CharField(default=0,max_length=8)
	start          = models.DateTimeField()
	end            = models.DateTimeField(blank=True,null=True)
	completed      = models.BooleanField(default=False)
	
	def __str__(self):
		return str(self.user.email) + " scored " + str(self.score) + " in " + str(self.quiz)

	class Meta:
		verbose_name = "QuizAnalysis"
		verbose_name_plural = "QuizAnalysis"

	def convert_sec(self,seconds):
		seconds = seconds % (24 * 3600) 
		hour = seconds // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		return "%d Hour:%02d Minutes:%02d Seconds" % (hour, minutes, seconds) 

	def get_time_difference(self):
		return self.convert_sec((self.end - self.start).total_seconds())

######------------------StoredStudentAnswer----------################

class StoredStudentAnswer(models.Model):
	"""Since it was the required of the project to store answer"""

	user             = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	quiz             = models.ForeignKey(Quiz,on_delete=models.CASCADE)
	question         = models.ForeignKey(Question,on_delete=models.CASCADE)
	correct_answer   = models.CharField(max_length=255)
	# I am storing correct_answer again , however it is not required, Its just for admin's help. 
	# Denormalization
	student_answered = models.CharField(max_length=255)
	is_correct       = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user.email) + "answered" + str(self.student_answered)[:20]