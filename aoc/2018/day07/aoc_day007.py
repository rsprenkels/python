from collections import namedtuple

with open('input_day07.txt', 'r') as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]

# lines = [
# 'Step C must be finished before step A can begin.',
# 'Step C must be finished before step F can begin.',
# 'Step A must be finished before step B can begin.',
# 'Step A must be finished before step D can begin.',
# 'Step B must be finished before step E can begin.',
# 'Step D must be finished before step E can begin.',
# 'Step F must be finished before step E can begin.',
# ]

steps_todo = set()
steps_done = list()

required_steps = {}

for line in lines:
    words = line.split()
    step_first = words[1]
    step_before = words[7]
    print(f"{step_first} before {step_before}")
    steps_todo.add(step_first)
    steps_todo.add(step_before)
    if step_before in required_steps:
        required_steps[step_before].append(step_first)
    else:
        required_steps[step_before] = list(step_first)

print(steps_todo)

print(required_steps)

# while len(steps_done) < len(steps_todo):
#     options = sorted(list(steps_todo - set(steps_done) - required_steps.keys()))
#     print(f"required steps are {required_steps}")
#     print(f"options are {options}")
#     take_step = options[0]
#     steps_done.append(take_step)
#     for step in  required_steps:
#         print(f"step {step} has {required_steps[step]}")
#         if take_step in required_steps[step]:
#             required_steps[step].remove(take_step)
#     required_steps = {x: required_steps[x] for x in required_steps if len(required_steps[x]) > 0}

Worker = namedtuple('Worker', 'number state end_time')

class Worker():
    def __init__(self):
        self.state = '.'
        self.end_time = None

    def __repr__(self):
        if self.state == '.':
            return ".     "
        else:
            return f"{self.state} {self.end_time:4}"

workers = [Worker() for x in range(4)]

current_second = 0
while len(steps_done) < len(steps_todo):
    # process completed work
    for worker in workers:
        if worker.end_time == current_second:
            just_done = worker.state
            steps_done.append(just_done)
            worker.state = '.'
            for step in required_steps:
                if just_done in required_steps[step]:
                    required_steps[step].remove(just_done)
            required_steps = {x: required_steps[x] for x in required_steps if len(required_steps[x]) > 0}

    # start new work
    working_on = set([worker.state for worker in workers if worker.state != '.'])
    options = sorted(list(steps_todo - working_on - set(steps_done) - required_steps.keys()), reverse=True)
    print(f"T {current_second:4} options are {options}")
    idle_workers = [worker for worker in workers if worker.state == '.']
    print(f"T {current_second:4} idle workers {idle_workers} options {options}")
    while len(idle_workers) > 0 and len(options) > 0:
        worker = idle_workers.pop()
        worker.state = options.pop()
        worker.end_time = current_second + ord(worker.state) - ord('A') + 61
        idle_workers = [worker for worker in workers if worker.state == '.']
        print(f"T {current_second:4} workers: {workers}")

    working_on = set([worker for worker in workers if worker.state != '.'])
    print(f"T {current_second:4} working on {working_on}")

    # on to next second
    current_second += 1

print(f"result: total_seconds {current_second - 1}  steps taken: {''.join(steps_done)}")