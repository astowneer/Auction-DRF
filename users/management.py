from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            return ValueError("is_superuser must be True")
        if extra_fields.get("is_staff") is not True:
            return ValueError("is_staff must be True")
        return self.create_user(email, password, **extra_fields)