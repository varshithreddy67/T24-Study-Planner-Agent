class StudyMemory:

    def __init__(self):
        self.tasks = []
        self.conversation = []

    def add_task(self, name, due):

        task = {
            "name": name,
            "due": due
        }

        self.tasks.append(task)

        return task

    def get_tasks(self):

        return self.tasks

    def add_message(self, role, content):

        self.conversation.append(
            {
                "role": role,
                "content": content
            }
        )

    def get_conversation(self):

        return self.conversation

    def clear(self):

        self.tasks = []
        self.conversation = []