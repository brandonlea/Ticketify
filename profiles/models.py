from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    UserProfile model to extend Django User model with additional information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    street_address1 = models.CharField(max_length=80, blank=True)
    street_address2 = models.CharField(max_length=80, blank=True)
    town_or_city = models.CharField(max_length=40, blank=True)
    county = models.CharField(max_length=80, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=40, blank=True, default='Ireland')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    Signal to automatically create/update profile when user is created/updated
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Save the profile for existing users
    instance.userprofile.save()