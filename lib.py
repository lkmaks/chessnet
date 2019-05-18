import random
import string
from math import floor, sqrt

def sql_date(date):
    """
    transforms date in human format to date used in sql query
    :param date: str like '13.02.2005'
    :return: str
    """
    return "to_date('{}', 'dd.mm.yyyy')".format(date)


def new_ratings(rw, rb, res):
    # res: 0 - white, 1 - draw, 2 - black
    delta = int(floor(sqrt(abs(rw - rb)))) + 5
    if res == 0:
        rw += delta
        rb -= delta
    elif res == 2:
        rw -= delta
        rb += delta
    elif res == 1:
        if rw < rb:
            rw += delta // 2
            rb -= delta // 2
        else:
            rw -= delta // 2
            rb += delta // 2
    return rw, rb


def random_tournament_name(length=10):
    res = []
    for i in range(length):
        res.append(random.choice(string.ascii_lowercase))
    return ''.join(res)


def random_tournament_date(length=9, year_from=2019, year_to=2029):
    d = random.randint(1, 15)
    m = random.randint(1, 12)
    y = random.randint(year_from, year_to)
    d1 = str(d) + '.' + str(m) + '.' + str(y)
    d2 = str(d + length - 1) + '.' + str(m) + '.' + str(y)
    return (d1, d2)


def rand_time_left():
    h = random.randint(0, 2)
    m = random.randint(1, 59)
    return str(h) + ':' + str(m)


def get_result_by_rating(r1, r2):
    p2 = int(floor(r1 / (r1 + r2 + 1000) * 100))
    p1 = 100 - p2
    p1 -= 20
    p2 -= 20
    p1 = max(p1, 0)
    p2 = max(p2, 0)
    x = random.randint(1, p1 + p2 + 40)
    if x <= p1:
        return 0
    elif x >= p1 + 40:
        return 2
    else:
        return 1


def shift(date, dist):
    # assume day + dist is in same month
    d, m, y = map(int, date.split('.'))
    d += dist
    return '{}.{}.{}'.format(d, m, y)


def random_username(length=7):
    res = []
    for i in range(length):
        res.append(random.choice(string.ascii_letters + string.digits))
    return ''.join(res)


def random_email(length=7):
    name = []
    for i in range(length):
        name.append(random.choice(string.ascii_letters + string.digits))
    res = ''.join(name)
    res += '@'
    res += random.choice(['yandex.ru', 'gmail.com', 'mipt.edu', 'mail.ru'])
    return res


def random_password(length=10):
    res = []
    for i in range(length):
        res.append(random.choice(string.ascii_letters + string.digits + '_-@!#$;^'))
    return ''.join(res)
