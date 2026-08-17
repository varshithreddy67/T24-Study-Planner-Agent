from tools import add_task, build_schedule, get_tasks


print("ADDING TASKS")
print("--------------------")

result1 = add_task(
    "Python Assignment",
    "2026-08-22"
)

print(result1)


result2 = add_task(
    "Java Exam",
    "2026-08-25"
)

print(result2)


print("\nMEMORY")
print("--------------------")

print(get_tasks())


print("\nBUILDING SCHEDULE")
print("--------------------")

schedule = build_schedule()

print(schedule)