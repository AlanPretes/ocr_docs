import re
import uuid
from apps.user.models import User


class Utils:
    def set_username(self, id: str, email: str):
        User.objects.filter(id=id).update(username=email)

    def check_password(self, password: str):
        not_valid = False
        if (len(password) < 8):
            not_valid = 'Senha deve conter pelo menos 8 caracteres!'
            return not_valid
        if not re.search("[a-z]", password):
            not_valid = 'Senha deve conter pelo menos uma letra minuscula!'
            return not_valid
        if not re.search("[A-Z]", password):
            not_valid = 'Senha deve conter pelo menos uma letra maiuscula!'
            return not_valid
        if not re.search("[0-9]", password):
            not_valid = 'Senha deve conter pelo menos um número!'
            return not_valid
        if not re.search("[_@!()&+$]", password):
            not_valid = 'Senha deve conter pelo menos uma dos seguintes simbolos: _, @, !, (, ), &, +, $'
            return not_valid
        if re.search("\s", password):
            not_valid = 'Senha informada não é válida!'

        return not_valid

    def forgot_password(self, user: User):
        new_password = str(uuid.uuid4())
        user.set_password(new_password)
        user.save()
        print(new_password)

    def change_password(self, user: User, current_password: str, new_password):
        if user.check_password(current_password):
            user.set_password(new_password)
            user.first_login = False
            user.save()
            return True
        return False
