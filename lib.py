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
    white_points = 0
    black_points = 0
    if res == 0:
        white_points = 1
        black_points = 0
    elif res == 1:
        white_points = 0.5
        black_points = 0.5
    elif res == 2:
        white_points = 0
        black_points = 1

    kw = -1
    if kw >= 2400:
        kw = 10
    else:
        kw = 20

    kb = -1
    if kb >= 2400:
        kb = 10
    else:
        kb = 20

    ew = 1 / (1 + 10 ** ((rb - rw) / 400))
    eb = 1 / (1 + 10 ** ((rw - rb) / 400))

    rw = rw + kw * (white_points - ew)
    rb = rb + kb * (black_points - eb)

    return rw, rb


def random_tournament_name(length=10):
    res = []
    for i in range(length):
        res.append(random.choice(string.ascii_lowercase))
    return ''.join(res)


def random_tournament_date(length=9, year_from=2019, year_to=2020):
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


def get_result_by_real_rating(r1, r2):
    if r1 > r2:
        return 0
    else:
        return 2
    e1 = 1 / (1 + 10 ** ((r2 - r1) / 400))
    p = random.randrange(0, 1000) / 1000
    draw_dist = min(e1, 1 - e1) * 0.3
    if e1 - draw_dist < p and p < e1 + draw_dist:
        return 1
    elif p <= e1 - draw_dist:
        return 0
    elif p >= e1 + draw_dist:
        return 2
    else:
        return 0


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
