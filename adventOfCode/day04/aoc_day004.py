from collections import namedtuple
import datetime

with open('guard_data.txt', 'r') as f:
    loglines = f.read().splitlines()

# Logrecord = namedtuple('Logrecord', 'guard_id minutes')

class Sleeplog():
    def __init__(self):
        self.dates = []
        self.ids = []
        self.minutes = []

    def add_loglines(self, loglines):
        self.loglines = sorted(loglines)
        curdate = None
        for line in self.loglines:
            date_part = line[1:17]
            event, rest = line[19:].split(' ', 1)
            # print(f"{line}   date[{date_part}] event[{event}] rest[{rest}]")
            if event == 'Guard':
                log_datetime = datetime.datetime.strptime(date_part, '%Y-%m-%d %H:%M')
                if log_datetime.hour == 23:
                    curdate = log_datetime + datetime.timedelta(days=1)
                else:
                    curdate = log_datetime
                guard_id = int(rest.split()[0][1:])
                print(f"Guardevent: curdate[{curdate.strftime('%m-%d %H:%M')}] guard_id[{guard_id}]")
                self.dates.append(curdate)
                self.ids.append(guard_id)
                self.minutes.append(['.' for min in range(60)])
                # print(f"minutes {self.minutes[-1:]}")
            elif event == 'falls':
                log_datetime = datetime.datetime.strptime(date_part, '%Y-%m-%d %H:%M')
                if log_datetime.hour == 23:
                    curdate = log_datetime + datetime.timedelta(days=1)
                else:
                    curdate = log_datetime
                print(f"sleepevent: curdate[{curdate.strftime('%m-%d %H:%M')}] guard_id[{guard_id}]")
                # print(f"curdate {curdate} {curdate.minute}")
                for min in range(curdate.minute, 60):
                    self.minutes[-1][min] = '#'
            elif event == 'wakes':
                log_datetime = datetime.datetime.strptime(date_part, '%Y-%m-%d %H:%M')
                if log_datetime.hour == 23:
                    curdate = log_datetime + datetime.timedelta(days=1)
                else:
                    curdate = log_datetime
                print(f"wakeevent:  curdate[{curdate.strftime('%m-%d %H:%M')}] guard_id[{guard_id}]")
                for min in range(curdate.minute, 60):
                    self.minutes[-1][min] = '.'

    def __str__(self):
        out = ''
        for index in range(len(self.dates)):
            out += f"{self.dates[index].strftime('%m-%d')} {self.ids[index]:5} "
            for min in range(60):
                out += self.minutes[index][min]
            out += '\n'
        return out

sleeplog = Sleeplog()
sleeplog.add_loglines(loglines)
print(f"{sleeplog}")

# calc the per guard sleep time
guards = {}
for index in range(len(sleeplog.dates)):
    day_sleep = len([minute for minute in range(60) if sleeplog.minutes[index][minute] == '#'])
    print(f"guard {sleeplog.ids[index]} date {sleeplog.dates[index]} sleep {day_sleep}")
    guard_id = sleeplog.ids[index]
    if guard_id in guards:
        guards[guard_id] += day_sleep
    else:
        guards[guard_id] = day_sleep

# get the most sleeping guard
sorted_guards = sorted((value, key) for (key,value) in guards.items())
most_sleepy = sorted_guards[-1][1]
print(most_sleepy)

# for that guard, calc the sleep per indiv. minute
total_sleep = [0 for min in range(60)]
for index in range(len(sleeplog.dates)):
    if sleeplog.ids[index] == most_sleepy:
        for min in range(60):
            if sleeplog.minutes[index][min] == '#':
                total_sleep[min] += 1

most_slept_minute = total_sleep.index(max(total_sleep))

print(f"result is {most_sleepy * most_slept_minute}")

# and your'e done.

#part 2
guards = {}
for index in range(len(sleeplog.dates)):
    guard_id = sleeplog.ids[index]
    if guard_id in guards:
        hour_list = guards[guard_id]
    else:
        hour_list = [0 for min in range(60)]
        guards[guard_id] = hour_list
    for min in range(60):
        if sleeplog.minutes[index][min] == '#':
            hour_list[min] += 1

data = []
for guard in guards:
    data.append((guard, max(guards[guard]), guards[guard].index(max(guards[guard]))))

from operator import itemgetter

strat2 = max(data, key=itemgetter(1))
print(f"strategy 2 gives {strat2} and endresult {strat2[0] * strat2[2]}")