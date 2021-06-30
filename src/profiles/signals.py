from .models import Profile
from administration.models import Score
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
# from djoser.signals import user_registered


User = get_user_model()

# @receiver(user_registered)
# def post_save_handler(user, request, **kwargs):

#     # print(user, request.data)
#     # return redirect('login')
#     pass

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff == False and instance.email:
            Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def post_save_create_job_status(sender, instance, created, **kwargs):
    if created:
        if instance.score is None:
            instance.score = Score.objects.create()
            instance.save()

