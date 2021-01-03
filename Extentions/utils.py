from django.utils import timezone
from . import jalali
import random
import string
from django.utils.text import slugify
import os
from random import randint

def jalali_convertor(time):
    jmonth = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

    time = timezone.localtime(time)

    time_to_str = f'{time.year} {time.month} {time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)
    for index, month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = f'{time_to_list[2]} {time_to_list[1]} {time_to_list[0]}, ساعت {time.hour}:{time.minute}'
    return persian_numbers(output)

def persian_numbers(myStr):
    numbers = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}
    for e, p in numbers.items():
        myStr = myStr.replace(e,p)
    return myStr

'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# print(random_string_generator())
# print(random_string_generator(size=50))

# before function File storage
def get_filename_ext_rand(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    random_id = randint(1000, 9999)
    return name, ext, random_id

def get_ext_file(filename):
    extesion = os.path.splitext(str(filename))[1].lower()
    extesion_allowed = ['.png', '.jpg', 'jpeg']
    for i in extesion_allowed:
        if extesion == i:
            return 'yes'
    return 'no'

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
