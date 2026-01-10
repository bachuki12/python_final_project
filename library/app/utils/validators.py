import string


class ValidationError(ValueError):
    """საერთო ვალიდაციის შეცდომა"""
    pass


class InputValidator:
    # ---------- BASIC ----------
    @staticmethod
    def non_empty(value, msg="ველი არ უნდა იყოს ცარიელი"):
        value = value.strip()
        if not value:
            raise ValidationError(msg)
        return value

    @staticmethod
    def choice(value, allowed, msg="არასწორი არჩევანი"):
        if value not in allowed:
            raise ValidationError(msg)
        return value

    # ---------- NUMBERS ----------
    @staticmethod
    def digits_exact(value, length, msg="არასწორი ციფრების რაოდენობა"):
        if not value.isdigit() or len(value) != length:
            raise ValidationError(msg)
        return value

    @staticmethod
    def int_in_range(value, min_v=None, max_v=None, msg="არასწორი რიცხვი"):
        try:
            iv = int(value)
        except ValueError:
            raise ValidationError(msg)

        if min_v is not None and iv < min_v:
            raise ValidationError(msg)
        if max_v is not None and iv > max_v:
            raise ValidationError(msg)
        return iv

    @staticmethod
    def float_in_range(value, min_v=None, max_v=None, msg="არასწორი რიცხვი"):
        try:
            fv = float(value)
        except ValueError:
            raise ValidationError(msg)

        if min_v is not None and fv < min_v:
            raise ValidationError(msg)
        if max_v is not None and fv > max_v:
            raise ValidationError(msg)
        return fv

    # ---------- TEXT ----------
    @staticmethod
    def name(value, msg="სახელი არ უნდა შეიცავდეს ციფრებს"):
        value = InputValidator.non_empty(value, msg)
        if any(char.isdigit() for char in value):
            raise ValidationError(msg)
        return value

    @staticmethod
    def password(value, min_len=3):
        allowed = string.ascii_letters + string.digits
        if len(value) < min_len:
            raise ValidationError(f"პაროლი უნდა იყოს მინიმუმ {min_len} სიმბოლო")

        if not all(c in allowed for c in value):
            raise ValidationError("პაროლი უნდა შეიცავდეს მხოლოდ ინგლისურ ასოებს და ციფრებს")

        if not (any(c.isalpha() for c in value) and any(c.isdigit() for c in value)):
            raise ValidationError("პაროლი უნდა შეიცავდეს მინიმუმ ერთ ასოს და ერთ ციფრს")

        return value
