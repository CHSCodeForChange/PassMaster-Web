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
		return Pass.get_students_active_passes(user) + Pass.get_students_pending_passes(user) + Pass.get_students_old_passes(user)

	@staticmethod
	def get_students_active_passes(user):
		profile = user.profile
		if profile.is_student:
			student = profile.student
			teacher_passes_o = TeacherPass.objects.filter(student=student, approved=True, timeArrivedDestination=None)
			teacher_passes_d = TeacherPass.objects.filter(student=student, approved=True, timeArrivedDestination=None)
			location_passes = LocationPass.objects.filter(student=student, approved=True, timeArrivedDestination=None)
			srt_passes = SRTPass.objects.filter(student=student, approved=True, timeArrivedDestination=None)
			return list(chain(teacher_passes_o, teacher_passes_d, location_passes, srt_passes))
		else:
			return None

	@staticmethod
	def get_students_pending_passes(user):
		profile = user.profile
		if profile.is_student:
			student = profile.student
			teacher_passes_o = TeacherPass.objects.filter(student=student, approved=False, timeArrivedDestination=None)
			teacher_passes_d = TeacherPass.objects.filter(student=student, approved=False, timeArrivedDestination=None)
			location_passes = LocationPass.objects.filter(student=student, approved=False, timeArrivedDestination=None)
			srt_passes = SRTPass.objects.filter(student=student, approved=False, timeArrivedDestination=None)
			return list(chain(teacher_passes_o, teacher_passes_d, location_passes, srt_passes))
		else:
			return None

	@staticmethod
	def get_students_old_passes(user):
		profile = user.profile
		if profile.is_student:
			student = profile.student
			teacher_passes_o = TeacherPass.objects.filter(student=student, approved=True).exclude(
				timeArrivedDestination=None)
			teacher_passes_d = TeacherPass.objects.filter(student=student, approved=True).exclude(
				timeArrivedDestination=None)
			location_passes = LocationPass.objects.filter(student=student, approved=True).exclude(
				timeArrivedDestination=None)
			srt_passes = SRTPass.objects.filter(student=student, approved=True).exclude(
				timeArrivedDestination=None)
			return list(chain(teacher_passes_o, teacher_passes_d, location_passes, srt_passes))
		else:
			return None

	def get_teacher_passes(user):
		return Pass.get_teachers_unapproved_passes(user) + Pass.get_teachers_old_passes(user) + Pass.get_teachers_incoming_student_passes(user) + Pass.get_teachers_outgoing_student_passes(user)

	@staticmethod
	def get_teachers_unapproved_passes(user):
		profile = user.profile
		if profile.is_teacher:
			teacher = user.profile.teacher
			teacher_passes = TeacherPass.objects.filter(approved=False, originTeacher=teacher)
			location_passes = LocationPass.objects.filter(approved=False, originTeacher=teacher)
			srt_passes = SRTPass.objects.filter(approved=False, originTeacher=teacher)
			return list(chain(teacher_passes, location_passes, srt_passes))

		else:
			return None

	@staticmethod
	def get_teachers_old_passes(user):
		profile = user.profile
		if profile.is_teacher:
			teacher = profile.teacher
			teacher_passes_o = TeacherPass.objects.filter(approved=True, originTeacher=teacher).exclude(timeArrivedDestination=None)
			teacher_passes_d = TeacherPass.objects.filter(approved=True, destinationTeacher=teacher).exclude(timeArrivedDestination=None)
			srt_passes_o = SRTPass.objects.filter(approved=True, originTeacher=teacher).exclude(timeArrivedDestination=None)
			srt_passes_d = SRTPass.objects.filter(approved=True, destinationTeacher=teacher).exclude(timeArrivedDestination=None)
			return list(chain(teacher_passes_o, teacher_passes_d, srt_passes_o, srt_passes_d))
		else:
			return None

	@staticmethod
	def get_teachers_incoming_student_passes(user):
		profile = user.profile
		if profile.is_teacher:
			teacher = profile.teacher
			return TeacherPass.objects.filter(approved=True, timeArrivedDestination=None, destinationTeacher=teacher)
		else:
			return None

	@staticmethod
	def get_teachers_outgoing_student_passes(user):
		profile = user.profile
		if profile.is_teacher:
			teacher = profile.teacher
			teacher_passes_o = TeacherPass.objects.filter(approved=True, timeArrivedDestination=None, originTeacher=teacher)
			teacher_passes_d = TeacherPass.objects.filter(approved=True, timeArrivedDestination=None, destinationTeacher=teacher)
			location_passes = LocationPass.objects.filter(approved=True, timeArrivedDestination=None, originTeacher=teacher)
			srt_passes_o = SRTPass.objects.filter(approved=True, timeArrivedDestination=None, originTeacher=teacher)
			srt_passes_d = SRTPass.objects.filter(approved=True, timeArrivedDestination=None, destinationTeacher=teacher)
			return list(chain(teacher_passes_o, teacher_passes_d, srt_passes_o, srt_passes_d, location_passes))
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
