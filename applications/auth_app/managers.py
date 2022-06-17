from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError('Email was not provided')
        if not password:
            raise ValueError('Password was not provided')

        user = self.model(
            email=email,
            **extra
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self._create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user