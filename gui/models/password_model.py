from core.password_generator import generate_password, generate_multiple_passwords

class PasswordModel:
    def generate_password(self, **kwargs):
        return generate_password(**kwargs)

    def generate_multiple(self, count=1, **kwargs):
        return generate_multiple_passwords(count=count, **kwargs) 