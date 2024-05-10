import flet as ft

class local_storage(ft.Page):
    def __init__(self, page):
        self.task = []
        self.completed = []
        self.primary_key = None
        self.page = page

    def create(self, task):
        st_task, st_completed = self.read()

        st_task.append(task)
        st_completed.append(False)

        self.page.client_storage.set("task", st_task)
        self.page.client_storage.set("completed", st_completed)

        return len(st_task)-1 # returns primary key location

    def read(self):
        """Returns a tuple of lists.
        storage tasks , storage completed"""

        if self.page.client_storage.contains_key("tasks"):
            st_task = self.page.client_storage.get("task")
            st_completed = self.page.client_storage.get("completed")

            if st_task is None:
                st_task = []
                st_completed = []
        else:
            st_task = []
            st_completed = []

        return st_task, st_completed

    def update_task(self, pk, task):
        st_task, st_completed = self.read()

        st_task[pk] = task

        self.page.client_storage.set("task", st_task)

    def update_completed(self, pk, completed):
        st_task, st_completed = self.read()

        st_completed[pk] = completed

        self.page.client_storage.set("completed", st_completed)


    def delete(self, pk):
        # This setup will require a list of primary keys. Future variations of this method will implement
        pass
