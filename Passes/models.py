from itertools import chain

from django.db import models
from datetime import datetime

from django.db.models import QuerySet, Q

from Student.models import Student
from Teacher.models import Teacher
from django.utils.timezone import now


# Create your models here.
class Pass(models.Model):
	objects = models.Manager()

	approved = models.BooleanField(
		default=False)  # """always needed, will be approved by destination teacher if its a teacher pass, or the origin teacher if its an other pass"""

	date = models.DateField(null=True, blank=True)
	startTimeRequested = models.TimeField(null=True, blank=True)  # """always needed"""
	endTimeRequested = models.TimeField(null=True, blank=True)  # """always needed"""

	timeLeftOrigin = models.TimeField(null=True, blank=True)  # """always needed"""
	timeArrivedDestination = models.TimeField(null=True, blank=True)

	student = models.ForeignKey(
		Student,
		on_delete=models.CASCADE,
		related_name="pass_student"
	)

	originTeacher = models.ForeignKey(
		Teacher,
		on_delete=models.CASCADE,
		related_name="pass_origin_teacher"
	)

	# """ The String description of the reason for the pass. This is mainly just for the destination teacher to know what the
	# student will need from them. """
	description = models.CharField(max_length=960, null=True)



	def __str__(self):
		if self.description != None:
			return self.description
		else:
			return 'None'

			

	# methods related to type of pass
	def pass_type(self):
		if (self.is_location_pass()):
			return 'LocationPassi'
		elif (self.is_srt_pass()):
			return 'SRTPass'
		elif (self.is_teacher_pass()):
			return 'TeacherPass'
	
	def is_location_pass(self):
		try:
			return self.locationpass != None
		except:
			return False

	def is_srt_pass(self):
		try:
			return self.srtpass != None
		except:
			return False

	def is_teacher_pass(self):
		try:
			return self.teacherpass != None
		except:
			return False

	# methods that change pass fields
	def approve(self):
		self.approved = True
		self.save()

	def leave(self):
		self.timeLeftOrigin = datetime.now()
		self.save()

	def arrive(self):
		self.timeArrivedDestination = datetime.now()
		self.save()

	# def return(self):
	#    self.timeReturned = datetime.now()

	def has_left(self):
		return self.timeLeftOrigin is not None

	def has_arrived(self):
		return self.timeArrivedDestination is not None

	
	def get_student_passes(user):
		return Pass.get_students_active_passes(user) | Pass.get_students_pending_passes(user) | Pass.get_students_old_passes(user)

	@staticmethod
	def get_students_active_passes(user):
		profile = user.profile
		if profile.is_student:
			student = profile.student
			return Pass.objects.filter(student=student, approved=True, timeArrivedDestination=None)
		else:
			return None

	@staticmethod
	def get_students_pending_passes(user):
		profile = user.profile
		if profile.is_student:
			student = profile.student
			return Pass.objects.filter(student=student, approved=False, timeArrivedDestination=None)
		else:
			return None

	@staticmethod
	def get_students_old_passes(user):
		profile = user.profile
		if profile.is_student:
			student = profile.student
			return Pass.objects.filter(student=student, approved=True).exclude(
				timeArrivedDestination=None)
		else:
			return None

	def get_teacher_passes(user):
		return Pass.get_teachers_unapproved_passes(user) | Pass.get_teachers_old_passes(user) | Pass.get_teachers_incoming_student_passes(user) | Pass.get_teachers_outgoing_student_passes(user)

	@staticmethod
	def get_teachers_unapproved_passes(user):
		profile = user.profile
		if profile.is_teacher:
			teacher = user.profile.teacher
			return Pass.objects.filter(approved=False, originTeacher=teacher)

		else:
			return None

	@staticmethod
	def get_teachers_old_passes(user):
		profile = user.profile
		if profile.is_teacher:
			teacher = profile.teacher
			query = Q(approved=True, originTeacher=teacher) | Q(approved=True, teacherpass__destinationTeacher=teacher)
			return Pass.objects.filter(query).exclude(timeArrivedDestination=None)
		else:
			return None

	@staticmethod
	def get_teachers_incoming_student_passes(user):
		profile = user.profile
		if profile.is_teacher:
			teacher = profile.teacher
			return Pass.objects.filter(approved=True, timeArrivedDestination=None, teacherpass__destinationTeacher=teacher)
		else:
			return None

	@staticmethod
	def get_teachers_outgoing_student_passes(user):
		profile = user.profile
		if profile.is_teacher:
			teacher = profile.teacher
			return Pass.objects.filter(approved=True, timeArrivedDestination=None, originTeacher=teacher)
		else:
			return None


class LocationPass(Pass):
	objects = models.Manager()
	location = models.CharField(max_length=12, null=True, blank=True)


class SRTPass(Pass):
	objects = models.Manager()

	destinationTeacher = models.ForeignKey(
		Teacher,
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name="destinationTeacherSRT"
	)

	# Options: "1" is session one, "2" is session two, and "3" is both sessions

	session = models.CharField(max_length=1, null=True, blank=True)

	# If session is "1", the origin teacher will need to fill this in for when they get back
	# Else, this will be null
	timeLeftDestination = models.TimeField(null=True, blank=True)

	timeArrivedOrigin = models.TimeField(null=True, blank=True)


class TeacherPass(Pass):
	objects = models.Manager()
	destinationTeacher = models.ForeignKey(
		Teacher,
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name="destinationTeacher"
	)
	pass_ptr = models.OneToOneField(
		Pass, on_delete=models.CASCADE,
		parent_link=True,
	)
