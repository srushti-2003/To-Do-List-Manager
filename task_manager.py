import logging

# Set up logging using logging module & Logs are written in todolist.log
logging.basicConfig(filename='todolist.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#This class represents the task of To-do list.Different methods and attributes are encapsulated in this task
class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False
        self.due_date = None
        self.tags = []

    def set_due_date(self, due_date):
        self.due_date = due_date

    def add_tags(self, tags):
        self.tags.extend(tags)

    def mark_completed(self):
        try:
            self.completed = True
        except Exception as e:
            logging.error(f"Error marking task as completed: {e}")

    def mark_pending(self):
        try:
            self.completed = False
        except Exception as e:
            logging.error(f"Error marking task as pending: {e}")

    #I have used here memento pattern to keep track of current state of task
    def create_memento(self):
        return {
            'description': self.description,
            'completed': self.completed,
            'due_date': self.due_date,
            'tags': self.tags.copy()
        }
    #Here it will help us in doing undo/redo actions to the task as it restores the previous state 
    def restore_from_memento(self, memento):
        try:
            self.description = memento['description']
            self.completed = memento['completed']
            self.due_date = memento['due_date']
            self.tags = memento['tags']
        except Exception as e:
            logging.error(f"Error restoring from memento: {e}")

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"{self.description} - {status}, Due: {self.due_date}, Tags: {', '.join(self.tags) if self.tags else 'None'}"

#Taskbuilder pattern is used to build description,Due Date and tags 
class TaskBuilder:
    def __init__(self, description):
        self.task = Task(description)

    def set_due_date(self, due_date):
        try:
            self.task.set_due_date(due_date)
        except Exception as e:
            logging.error(f"Error setting due date: {e}")
        return self

    def add_tags(self, tags):
        try:
            self.task.add_tags(tags)
        except Exception as e:
            logging.error(f"Error adding tags: {e}")
        return self

    def build(self):
        return self.task

#This class will manage tasks like if we complete the task then its status changes to completed and if the task is still pending then it shows pending.
#If the task is deleted then it is deleted and if we undo the task then completed task will be shown as pending and pending class will beshow as completed.
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.history = []

    def add_task(self, task):
        try:
            self.tasks.append(task)
            self.save_state()
        except Exception as e:
            logging.error(f"Error adding task: {e}")

    def mark_completed(self, description):
        try:
            for task in self.tasks:
                if task.description == description:
                    task.mark_completed()
                    self.save_state()
                    return
            logging.warning(f"No task found with description: {description}")
        except Exception as e:
            logging.error(f"Error marking task as completed: {e}")

    def mark_pending(self, description):
        try:
            for task in self.tasks:
                if task.description == description:
                    task.mark_pending()
                    self.save_state()
                    return
            logging.warning(f"No task found with description: {description}")
        except Exception as e:
            logging.error(f"Error marking task as pending: {e}")

    def delete_task(self, description):
        try:
            self.tasks = [task for task in self.tasks if task.description != description]
            self.save_state()
        except Exception as e:
            logging.error(f"Error deleting task: {e}")
            
# You can filter the tasks based on completed,pending and view all tasks
    def view_tasks(self, filter_option=None):
        try:
            if filter_option == "completed":
                filtered_tasks = [task for task in self.tasks if task.completed]
            elif filter_option == "pending":
                filtered_tasks = [task for task in self.tasks if not task.completed]
            else:
                filtered_tasks = self.tasks

            for task in filtered_tasks:
                print(task)
        except Exception as e:
            logging.error(f"Error viewing tasks: {e}")
# this undo function will restore the previous state from restore memento
    def undo(self):
        try:
            if len(self.history) > 1:
                self.history.pop()
                previous_state = self.history[-1]
                for task, state in zip(self.tasks, previous_state):
                    task.restore_from_memento(state)
            else:
                logging.info("No commands to undo")
        except Exception as e:
            logging.error(f"Error during undo: {e}")

    def save_state(self):
        try:
            current_state = [task.create_memento() for task in self.tasks]
            self.history.append(current_state)
        except Exception as e:
            logging.error(f"Error saving state: {e}")


if __name__ == "__main__":
    task_manager = TaskManager()

    while True:
        print("\nCommands:")
        print("1. Add Task: 'add description, Due: due_date, Tags: tag1, tag2, ...'")
        print("2. Mark Completed: 'complete description'")
        print("3. Mark Pending: 'pending description'")
        print("4. Delete Task: 'delete description'")
        print("5. View Tasks: 'view all', 'view completed', 'view pending'")
        print("6. Undo: 'undo'")

        user_input = input("Enter command: ")

        if user_input.startswith("add"):
            try:
                _, params = user_input.split(" ", 1)
                description, *options = [p.strip() for p in params.split(",")]
                builder = TaskBuilder(description)
                for option in options:
                    key, value = option.split(":")
                    if key.lower() == "due":
                        builder.set_due_date(value.strip())
                    elif key.lower() == "tags":
                        tags = [tag.strip() for tag in value.split(",")]
                        builder.add_tags(tags)
                task = builder.build()

                task_manager.add_task(task)
            except Exception as e:
                logging.error(f"Error adding task: {e}")

        elif user_input.startswith("complete"):
            try:
                _, description = user_input.split(" ", 1)
                task_manager.mark_completed(description)
            except Exception as e:
                logging.error(f"Error marking task as completed: {e}")

        elif user_input.startswith("pending"):
            try:
                _, description = user_input.split(" ", 1)
                task_manager.mark_pending(description)
            except Exception as e:
                logging.error(f"Error marking task as pending: {e}")

        elif user_input.startswith("delete"):
            try:
                _, description = user_input.split(" ", 1)
                task_manager.delete_task(description)
            except Exception as e:
                logging.error(f"Error deleting task: {e}")

        elif user_input.startswith("view"):
            try:
                _, filter_option = user_input.split(" ", 1) if " " in user_input else ("view", None)
                task_manager.view_tasks(filter_option)
            except Exception as e:
                logging.error(f"Error viewing tasks: {e}")

        elif user_input == "undo":
            try:
                task_manager.undo()
            except Exception as e:
                logging.error(f"Error during undo: {e}")

        else:
            print("Invalid command. Please try again.")

