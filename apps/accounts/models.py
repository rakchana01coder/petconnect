from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email address must be set.")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADOPTER = "adopter", _("Adopter")
        OWNER = "owner", _("Pet owner")
        SHELTER = "shelter", _("Shelter / Rescue")
        VET = "vet", _("Veterinarian")
        VOLUNTEER = "volunteer", _("Volunteer")
        ADMIN = "admin", _("Administrator")

    username = None
    email = models.EmailField(_("email address"), unique=True, db_index=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ADOPTER, db_index=True)
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=32, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ("-date_joined",)
        indexes = [models.Index(fields=["role", "is_active"])]

    def __str__(self):
        return self.email

    @property
    def display_name(self):
        return self.get_full_name() or self.email.split("@")[0]