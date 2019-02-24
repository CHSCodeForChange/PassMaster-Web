from datetime import datetime, time, timedelta

from django.db import models


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

	creator = models.ForeignKey(
		'Teacher',
		null=True,
		blank=True,
		on_delete=models.CASCADE,
	 	related_name="pass_creator"
	 )

	requester = models.ForeignKey(
		'Student',
		null=True,
		blank=True,
		on_delete=models.CASCADE,
		related_name="pass_requester"
	)
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

	#todo add for new pass type

	#### methods related to type of pass ####
	def pass_type(self):
		if self.is_location_pass():
			return 'LocationPass'
		elif self.is_srt_pass():
			return 'SRTPass'
		elif self.is_teacher_pass():
			return 'TeacherPass'
		elif self.is_special_srt_pass():
			return 'SpecialSRTPass'

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

	def is_special_srt_pass(self):
		try:
			return self.specialsrtpass is not None
		except:
			return False

	def child(self):
		if self.is_location_pass():
			return self.locationpass
		elif self.is_srt_pass():
			return self.srtpass
		elif self.is_teacher_pass():
			return self.teacherpass
		elif self.is_special_srt_pass():
			return self.specialsrtpass


	#### information ####

	def get_destinationTeacher(self):
		if self.is_location_pass():
			return self.locationpass.get_destinationTeacher()
		elif self.is_srt_pass():
			return self.srtpass.get_destinationTeacher()
		elif self.is_teacher_pass():
			return self.teacherpass.get_destinationTeacher()
		elif self.is_special_srt_pass():
			return self.specialsrtpass.get_destinationTeacher()

	def get_destination(self):
		if self.is_location_pass():
			return self.locationpass.location
		elif self.is_teacher_pass():
			return self.teacherpass.destinationTeacher.__str__()
		elif self.is_srt_pass():
			return self.srtpass.destinationTeacher.__str__()
		elif self.is_special_srt_pass():
			return self.specialsrtpass.destinationTeacher.__str__()

	def has_left(self):
		return self.timeLeftOrigin is not None

	def has_arrived(self):
		return self.timeArrivedDestination is not None

	def is_permitted(self, user):
		return self in Pass.get_passes(user)

	#### permission checks ####

	def can_approve(self, teacher):
		if self.is_location_pass():
			return self.locationpass.can_approve(teacher)
		elif self.is_srt_pass():
			return self.srtpass.can_approve(teacher)
		elif self.is_teacher_pass():
			return self.teacherpass.can_approve(teacher)
		elif self.is_special_srt_pass():
			return self.specialsrtpass.can_approve(teacher)

	def can_sign_in(self, teacher):
		if self.is_location_pass():
			return self.locationpass.can_sign_in(teacher)
		elif self.is_srt_pass():
			return self.srtpass.can_sign_in(teacher)
		elif self.is_teacher_pass():
			return self.teacherpass.can_sign_in(teacher)
		elif self.is_special_srt_pass():
			return self.specialsrtpass.can_sign_in(teacher)

	def can_sign_out(self, teacher):
		if self.is_location_pass():
			return self.locationpass.can_sign_out(teacher)
		elif self.is_srt_pass():
			return self.srtpass.can_sign_out(teacher)
		elif self.is_teacher_pass():
			return self.teacherpass.can_sign_out(teacher)
		elif self.is_special_srt_pass():
			return self.specialsrtpass.can_sign_out(teacher)

	#### actions ####

	def approve(self, teacher):
		if self.is_location_pass():
			self.locationpass.approve(teacher)
		elif self.is_srt_pass():
			self.srtpass.approve(teacher)
		elif self.is_teacher_pass():
			self.teacherpass.approve(teacher)
		elif self.is_special_srt_pass():
			return self.specialsrtpass.approve(teacher)

	def sign_in(self, teacher):
		if self.is_location_pass():
			self.locationpass.sign_in(teacher)
		elif self.is_srt_pass():
			self.srtpass.sign_in(teacher)
		elif self.is_teacher_pass():
			self.teacherpass.sign_in(teacher)
		elif self.is_special_srt_pass():
			return self.specialsrtpass.sign_in(teacher)

	def sign_out(self, teacher):
		if self.is_location_pass():
			self.locationpass.sign_out(teacher)
		elif self.is_srt_pass():
			self.srtpass.sign_out(teacher)
		elif self.is_teacher_pass():
			self.teacherpass.sign_out(teacher)
		elif self.is_special_srt_pass():
			return self.specialsrtpass.sign_out(teacher)


	#### pass lists ####

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
		return Pass.get_students_active_passes(user, dt) | \
			   	Pass.get_students_pending_passes(user, dt) | \
			   	Pass.get_students_old_passes(user, dt)

	@staticmethod
	def get_students_active_passes(user, dt=None):
		profile = user.profile
		if profile.is_student:
			student = profile.student
			passes = Pass.objects.filter(student=student, approved=True, timeArrivedDestination=None).exclude(srtpass__session="1") | \
						Pass.objects.filter(student=student, approved=True, srtpass__session="1", srtpass__timeArrivedOrigin=None)

			if dt is not None:
				passes = passes.filter(date=dt)

			return passes

		else:
			return None

	@staticmethod
	def get_students_pending_passes(user, dt=None):
		profile = user.profile
		if profile.is_student:
			student = profile.student
			passes = Pass.objects.filter(student=student, approved=False)

			if dt is not None:
				passes = passes.filter(date=dt)

			return passes

		else:
			return None

	@staticmethod
	def get_students_old_passes(user, dt=None):
		profile = user.profile
		if profile.is_student:
			student = profile.student
			passes = Pass.objects.filter(student=student, approved=True).exclude(timeArrivedDestination=None).exclude(srtpass__session="1") | \
					 Pass.objects.filter(student=student, approved=True, srtpass__session="1").exclude(srtpass__timeArrivedOrigin=None)

			if dt is not None:
				passes = passes.filter(date=dt)

			return passes

		else:
			return None

	@staticmethod
	def get_teacher_passes(user, dt=None):
		return Pass.get_teachers_unapproved_passes(user, dt) | \
				Pass.get_teachers_old_passes(user, dt) | \
			   	Pass.get_teachers_incoming_student_passes(user, dt) | \
			   	Pass.get_teachers_outgoing_student_passes(user, dt)

	@staticmethod
	def get_teachers_unapproved_passes(user, dt=None):
		profile = user.profile
		if profile.is_teacher:
			teacher = user.profile.teacher
			passes = Pass.objects.filter(approved=False, originTeacher=teacher) | \
						Pass.objects.filter(approved=False, teacherpass__destinationTeacher=teacher) | \
						Pass.objects.filter(approved=False, srtpass__destinationTeacher=teacher)

			if dt is not None:
				passes = passes.filter(date=dt)

			return passes

		else:
			return None

	@staticmethod
	def get_teachers_old_passes(user, dt=None):
		profile = user.profile
		if profile.is_teacher:
			teacher = profile.teacher
			passes = Pass.objects.filter(approved=True, originTeacher=teacher) | \
						 Pass.objects.filter(approved=True, teacherpass__destinationTeacher=teacher) | \
						 Pass.objects.filter(approved=True, srtpass__destinationTeacher=teacher)

			passes = passes.exclude(timeArrivedDestination=None).exclude(srtpass__session="1").exclude(specialsrtpass__session="1") | \
					 passes.filter(srtpass__session="1").exclude(srtpass__timeArrivedOrigin=None) | \
					 passes.filter(specialsrtpass__session="1").exclude(specialsrtpass__timeArrivedOrigin=None)

			if dt is not None:
				passes = passes.filter(date=dt)

			return passes

		else:
			return None

	@staticmethod
	def get_teachers_incoming_student_passes(user, dt=None):
		profile = user.profile
		if profile.is_teacher:
			teacher = profile.teacher
			passes = Pass.objects.filter(approved=True, timeArrivedDestination=None, teacherpass__destinationTeacher=teacher) | \
						Pass.objects.filter(approved=True, timeArrivedDestination=None, srtpass__destinationTeacher=teacher).exclude(srtpass__session="1") | \
						Pass.objects.filter(approved=True, srtpass__timeArrivedOrigin=None, srtpass__destinationTeacher=teacher, srtpass__session="1")
						# Pass.objects.filter(approved=True, timeArrivedDestination=None, specialsrtpass__destinationTeacher=location).exclude(specialsrtpass__session="1") | \

						# Pass.objects.filter(approved=True, specialsrtpass__timeArrivedOrigin=None, specialsrtpass__destinationTeacher=teacher, specialsrtpass__session="1")

			if dt is not None:
				passes = passes.filter(date=dt)

			return passes

		else:
			return None

	@staticmethod
	def get_teachers_outgoing_student_passes(user, dt=None):
		profile = user.profile
		if profile.is_teacher:
			teacher = profile.teacher
			passes = Pass.objects.filter(approved=True, timeArrivedDestination=None, originTeacher=teacher).exclude(srtpass__session="1").exclude(specialsrtpass__session="1") | \
					 Pass.objects.filter(approved=True, srtpass__timeArrivedOrigin=None, originTeacher=teacher, srtpass__session="1") | \
					 Pass.objects.filter(approved=True, specialsrtpass__timeArrivedOrigin=None, originTeacher=teacher, specialsrtpass__session="1")

			if dt is not None:
				passes = passes.filter(date=dt)

			return passes

		else:
			return None

	@staticmethod
	def get_locations_old_passes(user, dt=None):
		profile = user.profile
		if profile.is_location:
			location = profile.location
			passes = Pass.objects.filter(approved=True, specialsrtpass__destinationTeacher=location).exclude(timeArrivedDestination=None)

			if dt is None:
				return passes
			else:
				return passes.filter(date=dt)
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


class LocationPass(Pass):
	objects = models.Manager()
	location = models.CharField(max_length=12, null=True, blank=True)

	#### information ####

	def parent(self):
		return Pass.objects.get(locationpass=self)

	def get_destinationTeacher(self):
		return self.originTeacher

	#### actions ####

	def approve(self, teacher):
		if self.can_approve(teacher):
			self.approved = True;
			self.save()

	def sign_in(self, teacher):
		if self.can_sign_in(teacher):
			self.timeArrivedDestination = (datetime.now() - timedelta(hours=5)).time()
			self.save()

	def sign_out(self, teacher):
		if self.can_sign_out(teacher):
			self.timeLeftOrigin = (datetime.now() - timedelta(hours=5)).time()
			self.save()

	#### permissions ####

	def can_approve(self, teacher):
		return teacher == self.originTeacher and not self.approved

	def can_sign_in(self, teacher):
		return teacher == self.originTeacher and self.timeArrivedDestination is None

	def can_sign_out(self, teacher):
		return teacher == self.originTeacher and self.timeLeftOrigin is None


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
	def create(approved, date, student, originTeacher, description, destinationTeacher, session, creator, requester):
		if session == '1':
			startTimeRequested = time(hour=9, minute=50)
			endTimeRequested = time(hour=10, minute=20)
		elif session == '2':
			startTimeRequested = time(hour=10, minute=20)
			endTimeRequested = time(hour=11, minute=00)
		elif session == '3':
			startTimeRequested = time(hour=9, minute=50)
			endTimeRequested = time(hour=11, minute=00)

		return SRTPass(approved=approved,
		               date=date,
		               student=student,
		               originTeacher=originTeacher,
		               description=description,
		               destinationTeacher=destinationTeacher,
		               session=session,
		               startTimeRequested=startTimeRequested,
		               endTimeRequested=endTimeRequested,
					   creator=creator,
					   requester=requester)

	def fill_time(self):
		if self.session == '1':
			self.startTimeRequested = time(hour=9, minute=50)
			self.endTimeRequested = time(hour=10, minute=20)
		elif self.session == '2':
			self.startTimeRequested = time(hour=10, minute=20)
			self.endTimeRequested = time(hour=11, minute=00)
		elif self.session == '3':
			self.startTimeRequested = time(hour=9, minute=50)
			self.endTimeRequested = time(hour=11, minute=00)

		print(self.startTimeRequested)

		self.save()

	#### information ####

	def sessionStr(self):
		if self.session == '1':
			return "Session 1"
		elif self.session == '2':
			return "Session 2"
		elif self.session == '3':
			return "Both sessions"

	def parent(self):
		return Pass.objects.get(srtpass=self)

	def get_destinationTeacher(self):
		return self.destinationTeacher

	#### actions ####

	def approve(self, teacher):
		if self.can_approve(teacher):
			self.approved = True
			self.save()

	def sign_in(self, teacher):
		if self.can_sign_in(teacher):
			time = (datetime.now() - timedelta(hours=5)).time()
			if teacher == self.originTeacher:
				self.timeArrivedOrigin = time
			else:
				self.timeArrivedDestination = time
			self.save()

	def sign_out(self, teacher):
		if self.can_sign_out(teacher):
			time = (datetime.now() - timedelta(hours=5)).time()
			if teacher == self.originTeacher:
				self.timeLeftOrigin = time
			else:
				self.timeLeftDestination = time
			self.save()

	#### permissions ####

	def can_approve(self, teacher):
		return (teacher == self.originTeacher or teacher == self.destinationTeacher) and not self.approved

	def can_sign_in(self, teacher):
		if teacher == self.destinationTeacher and self.timeArrivedDestination is None and self.timeLeftOrigin is not None:
			return True
		if self.session == "1" and teacher == self.originTeacher and self.timeArrivedOrigin is None and self.timeLeftDestination is not None:
			return True
		return False

	def can_sign_out(self, teacher):
		if teacher == self.originTeacher and self.timeLeftOrigin is None:
			return True
		if self.session == "1" and teacher == self.destinationTeacher and self.timeLeftDestination is None and self.timeLeftOrigin is not None:
			return True
		return False


class TeacherPass(Pass):
	objects = models.Manager()
	destinationTeacher = models.ForeignKey(
		'Teacher',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name="destinationTeacher"
	)

	#### information ####

	def parent(self):
		return Pass.objects.get(teacherpass=self)

	def get_destinationTeacher(self):
		return self.destinationTeacher

	#### actions ####

	def approve(self, teacher):
		if self.can_approve(teacher):
			self.approved = True;
			self.save()

	def sign_in(self, teacher):
		if self.can_sign_in(teacher):
			self.timeArrivedDestination = (datetime.now() - timedelta(hours=5)).time()
			self.save()

	def sign_out(self, teacher):
		if self.can_sign_out(teacher):
			self.timeLeftOrigin = (datetime.now() - timedelta(hours=5)).time()
			self.save()

	#### permissions ####

	def can_approve(self, teacher):
		return (teacher == self.originTeacher or teacher == self.destinationTeacher) and not self.approved

	def can_sign_in(self, teacher):
		return teacher == self.destinationTeacher and self.timeArrivedDestination is None

	def can_sign_out(self, teacher):
		return teacher == self.originTeacher and self.timeLeftOrigin is None


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
	def create(approved, date, student, srtTeacher, description, destination, session, initiatingTeacher, creator):
		if session == '1':
			startTimeRequested = time(hour=9, minute=50)
			endTimeRequested = time(hour=10, minute=20)
		elif session == '2':
			startTimeRequested = time(hour=10, minute=20)
			endTimeRequested = time(hour=11, minute=00)
		elif session == '3':
			startTimeRequested = time(hour=9, minute=50)
			endTimeRequested = time(hour=11, minute=00)

		return SpecialSRTPass(
			approved=approved,
			date=date,
			student=student,
			originTeacher=srtTeacher,
			description=description,
			destinationTeacher=destination,
			session=session,
			startTimeRequested=startTimeRequested,
			endTimeRequested=endTimeRequested,
			initiatingTeacher=initiatingTeacher,
			creator=creator
		)

	def fill_time(self):
		if self.session == '1':
			self.startTimeRequested = time(hour=9, minute=50)
			self.endTimeRequested = time(hour=10, minute=20)
		elif self.session == '2':
			self.startTimeRequested = time(hour=10, minute=20)
			self.endTimeRequested = time(hour=11, minute=00)
		elif self.session == '3':
			self.startTimeRequested = time(hour=9, minute=50)
			self.endTimeRequested = time(hour=11, minute=00)

		print(self.startTimeRequested)

		self.save()

	def sessionStr(self):
		if self.session == '1':
			return "Session 1"
		elif self.session == '2':
			return "Session 2"
		elif self.session == '3':
			return "Both sessions"

	def parent(self):
		return Pass.objects.get(specialsrtpass=self)

	def get_destinationTeacher(self):
		return self.destinationTeacher

	#### actions ####

	def approve(self, teacher):
		if self.can_approve(teacher):
			self.approved = True
			self.save()

	def sign_in(self, teacher):
		if self.can_sign_in(teacher):
			time = (datetime.now() - timedelta(hours=5)).time()
			if teacher == self.originTeacher:
				self.timeArrivedOrigin = time
			else:
				self.timeArrivedDestination = time
			self.save()

	def sign_out(self, teacher):
		if self.can_sign_out(teacher):
			time = (datetime.now() - timedelta(hours=5)).time()
			if teacher == self.originTeacher:
				self.timeLeftOrigin = time
			else:
				self.timeLeftDestination = time
			self.save()

	#### permissions ####

	def can_approve(self, teacher):
		return (teacher == self.originTeacher or teacher == self.destinationTeacher) and not self.approved

	def can_sign_in(self, teacher):
		if teacher == self.destinationTeacher and self.timeArrivedDestination is None and self.timeLeftOrigin is not None:
			return True
		if self.session == "1" and teacher == self.originTeacher and self.timeArrivedOrigin is None and self.timeLeftDestination is not None:
			return True
		return False

	def can_sign_out(self, teacher):
		if teacher == self.originTeacher and self.timeLeftOrigin is None:
			return True
		if self.session == "1" and teacher == self.destinationTeacher and self.timeLeftDestination is None and self.timeLeftOrigin is not None:
			return True
		return False


class Location(models.Model):
	profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)

	def __str__(self):
		return self.profile.user.get_full_name()


class Administrator(models.Model):
	profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)


class Student(models.Model):
	profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)

	teachers = models.ManyToManyField('Teacher', related_name="teacher_list")

	defaultOrigin = models.ForeignKey(
		'Teacher',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name="srt_teacher"
	)

	def __str__(self):
		return self.profile.user.get_full_name()

	def get_deforigin(self):
		return self.defaultOrigin


class Teacher(models.Model):
	profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)
	name = models.CharField(max_length=250, default='stuff')

	def __str__(self):
		return self.profile.user.get_full_name()

	def get_students(self):
		pass
