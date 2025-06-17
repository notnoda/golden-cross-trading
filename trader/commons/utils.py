import datetime

def get_date(fmt="%Y%m%d"):
    return datetime.datetime.now().strftime(fmt)
#

def add_date(days, fmt="%Y%m%d"):
    next_day = datetime.datetime.now() + datetime.timedelta(days=days)
    return next_day.strftime(fmt)

if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> test start")
    print(get_date("%Y%m%d%H%M%S"))
    print("2025061807" > "2025061808")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> test end")
