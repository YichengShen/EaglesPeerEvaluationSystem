from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(
            self, email, first_name, last_name, eagle_id, 
            is_student, is_instructor,
            password=None, commit=True):
        """
        Creates and saves a User with the given email, first name, last name, 
        eagle id, and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))
        if not eagle_id:
            raise ValueError(_('Users must have a eagle id'))
        if not is_student:
            raise ValueError(_('Users must have a student status'))
        if not is_instructor:
            raise ValueError(_('Users must have a instructor status'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            eagle_id=eagle_id,
            is_student=is_student,
            is_instructor=is_instructor,
        )

        user.set_password(password)

        if user.is_instructor or user.is_staff: # user cannot be a student if he/she is an instructor
            user.is_student = False
        else:
            user.is_student = True

        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, eagle_id,
                         password, is_student, is_instructor):
        """
        Creates and saves a superuser with the given email, first name,
        last name, eagle_id, and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            eagle_id=eagle_id,
            commit=False,
            is_student=is_student,
            is_instructor=is_instructor,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True
    )
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    eagle_id = models.CharField(max_length = 8, unique=True)

    is_student = models.BooleanField(
        _('student status'),
        default=False,
        help_text=_(
            'Shows whether this user is a student. '
        ),
    )
    is_instructor = models.BooleanField(
        _('instructor status'),
        default=False,
        help_text=_(
            'Shows whether this user is a instructor. '
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('admin status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'eagle_id', 'is_student', 'is_instructor']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_eagle_id(self):
        """
        Return the eagle_id.
        """
        e_id = self.eagle_id
        return e_id

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True