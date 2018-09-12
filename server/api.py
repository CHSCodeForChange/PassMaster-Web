from rest_framework import generics

from .models import *
from .serializers import *


class PassList(generics.ListAPIView):
	"""
	retrieve:
	Return the given user.

	list:
	Return a list of all the existing users.

	create:
	Create a new user instance.
	"""
	queryset = Pass.objects.all()
	serializer_class = Read_PassSerializer
	permission_classes = ()

	def get_queryset(self):
		if self.request.user.profile.is_student():
			queryset = Pass.get_student_passes(self.request.user)
		elif self.request.user.profile.is_teacher():
			queryset = Pass.get_teacher_passes(self.request.user)

		return queryset


class PassGet(generics.RetrieveAPIView):
	"""
	retrieve:
	Return the given user.

	list:
	Return a list of all the existing users.

	create:
	Create a new user instance.
	"""
	serializer_class = Read_PassSerializer

	def get_queryset(self):
		return Pass.get_passes(self.request.user)


class LocationPassGet(generics.RetrieveAPIView):
	"""
	retrieve:
	Return the given user.

	list:
	Return a list of all the existing users.

	create:
	Create a new user instance.
	"""
	queryset = LocationPass.objects.all()
	serializer_class = Read_LocationPassSerializer


class SRTPassGet(generics.RetrieveAPIView):
	"""
	retrieve:
	Return the given user.

	list:
	Return a list of all the existing users.

	create:
	Create a new user instance.
	"""
	queryset = SRTPass.objects.all()
	serializer_class = Read_SRTPassSerializer


class TeacherPassGet(generics.RetrieveAPIView):
	"""
	retrieve:
	Return the given user.

	list:
	Return a list of all the existing users.

	create:
	Create a new user instance.
	"""
	queryset = TeacherPass.objects.all()
	serializer_class = Read_TeacherPassSerializer


class PassUpdate(generics.UpdateAPIView):
	"""
	retrieve:
	Return the given user.

	list:
	Return a list of all the existing users.

	create:
	Create a new user instance.
	"""
	serializer_class = StudentCreate_LocationPassSerializer

	def get_queryset(self):
		return Pass.get_passes(self.request.user)


class LocationPassCreate(generics.CreateAPIView):
	"""
	retrieve:
	Return the given user.

	list:
	Return a list of all the existing users.

	create:
	Create a new user instance.
	"""
	permission_classes = ()

	def get_serializer_class(self):
		if (self.request.user.profile.is_teacher()):
			return TeacherCreate_LocationPassSerializer
		else:
			return StudentCreate_LocationPassSerializer

	def perform_create(self, serializer):
		if (self.request.user.profile.is_teacher()):
			new_pass = serializer.save(approved=True, originTeacher=self.request.user.profile.teacher)
		else:
			serializer.save(student=self.request.user.profile.student)


class SRTPassCreate(generics.CreateAPIView):
	"""
	retrieve:
	Return the given user.

	list:
	Return a list of all the existing users.

	create:
	Create a new user instance.
	"""
	serializer_class = StudentCreate_SRTPassSerializer
	permission_classes = ()


class TeacherPassCreate(generics.CreateAPIView):
	"""
	retrieve:
	Return the given user.

	list:
	Return a list of all the existing users.

	create:
	Create a new user instance.
	"""
	permission_classes = ()

	def get_serializer_class(self):
		if (self.request.user.profile.is_teacher()):
			return TeacherCreate_TeacherPassSerializer
		else:
			return StudentCreate_TeacherPassSerializer

	def perform_create(self, serializer):
		if (self.request.user.profile.is_teacher()):
			new_pass = serializer.save(approved=True)
			if (new_pass.destinationTeacher == self.request.user.profile.teacher):
				new_pass.approved = True
				new_pass.save()
		else:
			serializer.save(student=self.request.user.profile.student)
