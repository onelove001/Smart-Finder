import datetime



def calcEpochSec(dt):
    epochZero = datetime.datetime(1970,1,1,tzinfo = dt.tzinfo)
    return (dt - epochZero).total_seconds()



def EpochSec(dt):
    epochZero = datetime.datetime(1970,1,1,tzinfo = dt.tzinfo)
    return (dt - epochZero).total_seconds()



def timesince(dt, default="Just Now"):
    dt = datetime.datetime(1970,1,1,tzinfo = dt.tzinfo)
    now = datetime.datetime.now()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@", now)
    diff = now - dt
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )
    for period, singular, plural in periods:
        if period >= 1:
            return "%d %s ago" % (period, singular if period == 1 else plural)
    return default

# 2021-02-28 15:39:51.651678