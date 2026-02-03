from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

from subject.models import Subject
from common.models import BaseModel


class Teacher(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='teacher_profile', on_delete=models.PROTECT)

    class Meta:
        db_table = "teachers"
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ['-created_at']

    def __str__(self):
        return self.user.full_name


class Certificate(BaseModel):
    attachment = models.FileField(upload_to="teacher_attachments")

    def __str__(self):
        return self.attachment.url


class Academic(BaseModel):
    teacher = models.ForeignKey(Teacher, related_name='academics', on_delete=models.CASCADE)
    institution = models.CharField(max_length=250)
    degree = models.CharField(max_length=250)
    major = models.CharField(max_length=250)
    grade = models.FloatField()
    grade_margin = models.FloatField()
    passing_year = models.IntegerField(null=True, blank=True)
    cartificate = models.ForeignKey(Certificate, on_delete=models.PROTECT)

    class Meta:
        db_table = "academics"
        verbose_name = "Academic"
        verbose_name_plural = "Academics"
        ordering = ['-created_at']


class ExtraInformation(BaseModel):
    teacher = models.OneToOneField(Teacher, related_name='extra_information', on_delete=models.CASCADE)
    teaching_experience = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    bio = models.CharField(max_length=1000)

    class Meta:
        db_table = "extrainformation"
        verbose_name = "Extra Information"
        verbose_name_plural = "Extra Information"
        ordering = ['-created_at']

    def __str__(self):
        return self.teacher.user.full_name


class ProfessionalExperience(BaseModel):
    teacher = models.ForeignKey(Teacher, related_name='professional_experiences', on_delete=models.CASCADE)
    institution = models.CharField(max_length=150)
    from_time = models.DateField(null=True, blank=True)
    to_time = models.DateField(null=True, blank=True)
    current_working = models.BooleanField(default=False)

    class Meta:
        db_table = "professional_experiences"
        verbose_name = "Professional Experience"
        verbose_name_plural = "Professional Experiences"
        ordering = ['-created_at']

    def __str__(self):
        return self.teacher.user.full_name


class Batch(BaseModel):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='batches', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='batches', on_delete=models.PROTECT)
    name = models.CharField(max_length=250)
    from_time = models.TimeField()
    to_time = models.TimeField()
    notes = models.TextField(help_text="Describe what you teach in shortly such topics so that student can understand")
    monthly_fee = models.DecimalField(max_digits=12, decimal_places=2)
    admission_fee = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ['name']
        db_table = "batches"
        verbose_name = "Batch"
        verbose_name_plural = "Batches"

    def __str__(self):
        return self.name
