from datetime import datetime, time

from django.db import models
from django.db.models import Q


# Create your models here.
class Pass(models.Model):
	objects = models.Manager()

	# Always needed, will be approved by destination teacher if its a teacher pass, or the origin teacher if its an other pass
	approved = models.BooleanField(
		default=False)

	date = models.DateField(null=True, blank=True)
	startTimeRequested = models.TimeField(null=True, blank=True)  # always needed
	endTimeRequested = models.TimeField(null=True, blank=True)  # always needed

	timeLeftOrigin = models.TimeField(null=True, blank=True)  # always needed
	timeArrivedDestination = models.TimeField(null=True, blank=True)

	student = models.ForeignKey(
		'Student',
		on_delete=models.CASCADE,
		related_name="pass_student"
	)

	originTeacher = models.ForeignKey(
		'Teacher',
		on_delete=models.CASCADE,
		related_name="pass_origin_teacher"
	)

	#  The String description of the reason for the pass. This is mainly just for the destination teacher to know what the
	# student will need from them.
	description = models.CharField(max_length=960, null=True)

	def __str__(self):
		if self.description is not None:
			return self.description
		else:
			return 'None'

	# methods related to type of pass
	def pass_type(self):
		if self.is_location_pass():
			return 'LocationPass'
		elif self.is_srt_pass():
			return 'SRTPass'
		elif self.is_teacher_pass():
			return 'TeacherPass'

	def is_location_pass(self):
		try:
			return self.locationpass is not None
		except:
			return False

	def is_srt_pass(self):
		try:
			return self.srtpass is not None
		except:
			return False

	def is_teacher_pass(self):
		try:
			return self.teacherpass is not None
		except:
			return False

	def child(self):
		if self.is_location_pass():
			return self.locationpass
		elif self.is_srt_pass():
			return self.srtpass
		elif self.is_teacher_pass():
			return self.teacherpass

	def get_destinationTeacher(self):
		if self.is_location_pass():
			return None
		elif self.is_srt_pass():
			return self.srtpass.destinationTeacher
		elif self.is_teacher_pass():
			return self.teacherpass.destinationTeacher

	# methods that change pass fields
	def approve(self, teacher):
		if teacher == self.originTeacher:
			self.approved = True
			self.save()

	def leave(self, teacher):
		# Check permissions
		if teacher != self.originTeacher:
			return
		# If the pass is a location pass and the user is the origin teacher sign them out
		# The pass must not be signed out yet
		if self.is_location_pass() and self.timeLeftOrigin is None:
			self.timeLeftOrigin = datetime.now()
			self.save()
		# They have not left the origin
		if self.timeLeftOrigin is None:
			self.timeLeftOrigin = datetime.now()
			self.save()
		# If they have left the origin, have an srt pass for session one and have not arrived back in their home room
		elif self.is_srt_pass() and self.srtpass.session == '1' and self.srtpass.timeArrivedDestination is not None:
			self.srtpass.timeLeftDestination = datetime.now()
			self.save()

	def arrive(self, teacher):
		# If the pass is a location pass and the user is the origin teacher sign them in
		# The pass must have been signed out but not in yet
		if self.is_location_pass() and teacher == self.originTeacher and self.timeLeftOrigin is not None and self.timeArrivedDestination is None:
			self.timeArrivedDestination = datetime.now()
			self.save()
		# Check permissions
		# This must be done after location pass stuff because location passes use the originTeacher
		if teacher != self.get_destinationTeacher() and teacher != self.get_destinationTeacher():
			return
		# If they have not arrived at the destination yet
		if self.timeArrivedDestination is None:
			self.timeArrivedDestination = datetime.now()
			self.save()
		# If they have left the destination, have an srt pass for session one and have not yet arrived back at their home room
		elif self.is_srt_pass() and self.srtpass.session == '1' and self.srtpass.timeLeftDestination is not None:
			self.srtpass.timeArrivedOrigin = datetime.now()
			self.save()

	def has_left(self):
		return self.timeLeftOrigin is not None

	def has_arrived(self):
		return self.timeArrivedDestination is not None

	def is_permitted(self, user):
		return self in Pass.get_passes(user)

	@staticmethod
	def get_passes(user, dt=None):
		if dt is None:
			if user.profile.is_student():
				student = user.profile.student
				return Pass.get_student_passes(student)
			elif user.profile.is_teacher():
				teacher = user.profile.teacher
				return Pass.get_teacher_passes(teacher)
		else:
			if user.profile.is_student():
				student = user.profile.student
				return Pass.get_student_passes(student, dt)
			elif user.profile.is_teacher():
				teacher = user.profile.teacher
				return Pass.get_teacher_passes(teacher, dt)

	@staticmethod
	def get_student_passes(user, dt=None):
		if dt is None:
			return Pass.get_students_active_passes(user) | Pass.get_students_pending_passes(
				user) | Pass.get_students_old_passes(user)
		else:
			return Pass.get_students_active_passes(user, dt) | Pass.get_students_pending_passes(
				user, dt) | Pass.get_students_old_passes(user, dt)

	@staticmethod
	def get_students_active_passes(user, dt=None):
		profile = user.profile
		if profile.is_student:
			student = profile.student

			if dt is None:
				return Pass.objects.filter(student=student, approved=True, timeArrivedDestination=None)
			else:
				return Pass.objects.filter(student=student, approved=True, timeArrivedDestination=None, date=dt)
		else:
			return None

	@staticmethod
	def get_students_pending_passes(user, dt=None):
		profile = user.profile
		if profile.is_student:
			student = profile.student

			if dt is None:
				return Pass.objects.filter(student=student, approved=False, timeArrivedDestination=None)
			else:
				return Pass.objects.filter(student=student, approved=False, timeArrivedDestination=None, date=dt)
		else:
			return None

	@staticmethod
	def get_students_old_passes(user, dt=None):
		profile = user.profile
		if profile.is_student:
			student = profile.student

			if dt is None:
				return Pass.objects.filter(student=student, approved=True).exclude(
					timeArrivedDestination=None)
			else:
				return Pass.objects.filter(student=student, approved=True, date=dt).exclude(
					timeArrivedDestination=None)
		else:
			return None

	@staticmethod
	def get_teacher_passes(user, dt=None):
		if dt is None:
			return Pass.get_teachers_unapproved_passes(user) | Pass.get_teachers_old_passes(
				user) | Pass.get_teachers_incoming_student_passes(user) | Pass.get_teachers_outgoing_student_passes(
				user)
		else:
			return Pass.get_teachers_unapproved_passes(user, dt) | Pass.get_teachers_old_passes(
				user, dt) | Pass.get_teachers_incoming_student_passes(user,
			                                                          dt) | Pass.get_teachers_outgoing_student_passes(
				user, dt)

	@staticmethod
	def get_teachers_unapproved_passes(user, dt=None):
		profile = user.profile
		if profile.is_teacher:
			teacher = user.profile.teacher

			if dt is None:
				return Pass.objects.filter(approved=False, originTeacher=teacher)
			else:
				return Pass.objects.filter(approved=False, date=dt, originTeacher=teacher)
		else:
			return None

	@staticmethod
	def get_teachers_old_passes(user, dt=None):
		profile = user.profile
		if profile.is_teacher:
			teacher = profile.teacher

			if dt is None:
				query = Q(approved=True, originTeacher=teacher) | Q(approved=True,
				                                                    teacherpass__destinationTeacher=teacher)
			else:
				query = Q(approved=True, originTeacher=teacher, date=dt) | Q(approved=True,
				                                                             teacherpass__destinationTeacher=teacher,
				                                                             date=dt)

			return Pass.objects.filter(query).exclude(timeArrivedDestination=None)
		else:
			return None

	@staticmethod
	def get_teachers_incoming_student_passes(user, dt=None):
		profile = user.profile
		if profile.is_teacher:
			teacher = profile.teacher
			if dt is None:
				return Pass.objects.filter(approved=True, timeArrivedDestination=None,
				                           teacherpass__destinationTeacher=teacher)
			else:
				return Pass.objects.filter(approved=True, timeArrivedDestination=None,
				                           teacherpass__destinationTeacher=teacher, date=dt)
		else:
			return None

	@staticmethod
	def get_teachers_outgoing_student_passes(user, dt=None):
		profile = user.profile
		if profile.is_teacher:
			teacher = profile.teacher
			if dt is None:
				return Pass.objects.filter(approved=True, timeArrivedDestination=None, originTeacher=teacher)
			else:
				return Pass.objects.filter(approved=True, timeArrivedDestination=None, originTeacher=teacher, date=dt)
		else:
			return None

	@staticmethod
	def get_locations_old_passes(user, dt=None):
		profile = user.profile
		if profile.is_location:
			location = profile.location

			if dt is None:
				query = Q(approved=True, specialsrtpass__destinationTeacher=location)
			else:
				query = Q(approved=True, specialsrtpass__destinationTeacher=location, date=dt)

			return Pass.objects.filter(query).exclude(timeArrivedDestination=None)
		else:
			return None

	@staticmethod
	def get_locations_incoming_student_passes(user, dt=None):
		profile = user.profile
		if profile.is_location:
			location = profile.location
			if dt is None:
				return Pass.objects.filter(approved=True, timeArrivedDestination=None,
				                           specialsrtpass__destinationTeacher=location)
			else:
				return Pass.objects.filter(approved=True, timeArrivedDestination=None,
				                           specialsrtpass__destinationTeacher=location, date=dt)
		else:
			return None



	def get_destination(self):
		if self.is_location_pass():
			return self.locationpass.location
		elif self.is_teacher_pass():
			return self.teacherpass.destinationTeacher.__str__()
		elif self.is_srt_pass():
			self.srtpass.destinationTeacher.__str__()


class LocationPass(Pass):
	objects = models.Manager()
	location = models.CharField(max_length=12, null=True, blank=True)

	def parent(self):
		return Pass.objects.get(locationpass=self)


class SRTPass(Pass):
	objects = models.Manager()

	destinationTeacher = models.ForeignKey(
		'Teacher',
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

	@staticmethod
	def create(date, student, originTeacher, description, destinationTeacher, session):
		if session == '1':
			startTimeRequested = time(hour=9, minute=50)
			endTimeRequested = time(hour=10, minute=20)
		elif session == '2':
			startTimeRequested = time(hour=10, minute=20)
			endTimeRequested = time(hour=11, minute=00)
		elif session == '3':
			startTimeRequested = time(hour=9, minute=50)
			endTimeRequested = time(hour=11, minute=00)

		return SRTPass(date=date,
		               student=student,
		               originTeacher=originTeacher,
		               description=description,
		               destinationTeacher=destinationTeacher,
		               session=session,
		               approved=True,
		               startTimeRequested=startTimeRequested,
		               endTimeRequested=endTimeRequested)

	def leaveDestination(self):
		if self.session == '1':
			self.timeLeftDestination = datetime.now()
			self.save()

	def arriveOrigin(self):
		if self.session == '1':
			self.timeArrivedOrigin = datetime.now()
			self.save()

	def sessionStr(self):
		if self.session == '1':
			return "Session 1"
		elif self.session == '2':
			return "Session 2"
		elif self.session == '3':
			return "Both sessions"

	def parent(self):
		return Pass.objects.get(srtpass=self)


class TeacherPass(Pass):
	objects = models.Manager()
	destinationTeacher = models.ForeignKey(
		'Teacher',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name="destinationTeacher"
	)

	def parent(self):
		return Pass.objects.get(teacherpass=self)


class SpecialSRTPass(Pass):
	objects = models.Manager()
	destinationTeacher = models.ForeignKey(
		'Location',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name="destinationTeacher"
	)
	initiatingTeacher = models.ForeignKey(
		'Teacher',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name="initiatingTeacher"
	)
	# Options: "1" is session one, "2" is session two, and "3" is both sessions

	session = models.CharField(max_length=1, null=True, blank=True)

	# If session is "1", the origin teacher will need to fill this in for when they get back
	# Else, this will be null
	timeLeftDestination = models.TimeField(null=True, blank=True)

	timeArrivedOrigin = models.TimeField(null=True, blank=True)

	@staticmethod
	def create(date, student, srtTeacher, description, destination, session, initiatingTeacher):
		if session == '1':
			startTimeRequested = time(hour=9, minute=50)
			endTimeRequested = time(hour=10, minute=20)
		elif session == '2':
			startTimeRequested = time(hour=10, minute=20)
			endTimeRequested = time(hour=11, minute=00)
		elif session == '3':
			startTimeRequested = time(hour=9, minute=50)
			endTimeRequested = time(hour=11, minute=00)

		return SpecialSRTPass(date=date,
		               student=student,
		               originTeacher=srtTeacher,
		               description=description,
		               destinationTeacher=destination,
		               session=session,
		               approved=True,
		               startTimeRequested=startTimeRequested,
		               endTimeRequested=endTimeRequested,
					   initiatingTeacher=initiatingTeacher)


class Location(models.Model):
	profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)

	def __str__(self):
		return self.profile.user.get_full_name()


class Administrator(models.Model):
	profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)


class Student(models.Model):
	profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)

	teachers = models.ManyToManyField('Teacher', related_name="teacher_list")

	defaultOrgin = models.ForeignKey(
		'Teacher',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name="srt_teacher"
	)

	def __str__(self):
		return self.profile.user.get_full_name()

	def get_deforgin(self):
		return self.defaultOrgin


class Teacher(models.Model):
	profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)
	name = models.CharField(max_length=250, default='stuff')

	def __str__(self):
		return self.profile.user.get_full_name()

	def get_students(self):
		pass
