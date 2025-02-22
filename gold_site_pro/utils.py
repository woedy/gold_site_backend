import random
import re
import string
from django.contrib.auth import get_user_model, authenticate




def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_random_otp_code():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    return code



def generate_email_token():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    return code



def unique_user_id_generator(instance):
    """
    This is for a django project with a user_id field
    :param instance:
    :return:
    """

    size = random.randint(30,45)
    user_id = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(user_id=user_id).exists()
    if qs_exists:
        return
    return user_id






def unique_account_id_generator(instance):
    """
    This is for a account_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    account_id = "ACC-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(BNK)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(account_id=account_id).exists()
    if qs_exists:
        return None
    return account_id




def unique_tracking_number_generator(instance):
    """
    This is for a tracking_number field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    tracking_number = "GP-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(G)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(tracking_number=tracking_number).exists()
    if qs_exists:
        return None
    return tracking_number





def unique_transaction_id_generator(instance):
    """
    This is for a transaction_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    transaction_id = "TRN-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(P)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(transaction_id=transaction_id).exists()
    if qs_exists:
        return None
    return transaction_id