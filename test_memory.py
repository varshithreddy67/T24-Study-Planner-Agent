from memory import StudyMemory


memory = StudyMemory()


memory.add_task(
    "Python Assignment",
    "2026-08-22"
)

memory.add_task(
    "Java Exam",
    "2026-08-25"
)


print("MEMORY CONTENT:")
print(memory.get_tasks())