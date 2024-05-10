import flet as ft
# import flet_material as fm
import sqlite3

from database import Database
from local_storage import local_storage

#db = Database()

#fm.Theme.set_theme(theme="blue")

class Task(ft.Column):
    def __init__(self, task_name, task_status_change, task_delete, database:local_storage, completed=False, pk=None):
        super().__init__()
        self.pk = pk # primary key for database entry
        self.task_name = task_name
        self.task_delete = task_delete
        self.completed = completed
        self.task_status_change = task_status_change
        # self.db = database
        self.storage = database

    def build(self):
        self.display_task = ft.Checkbox(value=self.completed, label=self.task_name, on_change=self.status_changed)
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip='Edit To-Do',
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            tooltip='Delete To-Do',
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return ft.Column(controls=[self.display_view, self.edit_view])

    def set_status(self, status):
        self.completed = status

    def status_changed(self, e):
        self.completed = self.display_task.value
        # update database entry
        #self.db.change_completed(self.pk, self.completed)
        self.storage.update_completed(self.pk, self.completed)
        self.task_status_change(self)

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        # update database entry
        #self.db.edit_task(self.pk, self.display_task.label)
        self.storage.update_task(self.pk, self.display_task.label)
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        # delete database entry
        #self.db.delete_task(self.pk)
        self.task_delete(self)

class TodoApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        # self.db = database
        self.storage = local_storage(page)

    def build(self):
        self.new_task = ft.TextField(hint_text="What needs to be done?", expand=True)
        self.tasks = ft.Column()

        # populate task list from database
        # db_tasks = self.db.get_tasks()
        # for t in db_tasks:
        #     task = Task(t[1], self.task_status_change, self.task_delete, self.db, completed=bool(t[2]), pk=t[0])
        #     self.tasks.controls.append(task)

        st_tasks, st_completed = self.storage.read()

        for index, t in enumerate(st_tasks):
            task = Task(t, self.task_status_change, self.task_delete, self.storage, completed=bool(st_completed[index]), pk=index)
            self.tasks.controls.append(task)

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text='all'), ft.Tab(text='active'), ft.Tab(text='completed')],
        )

        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD,
                            on_click=self.add_clicked
                        ),
                    ],
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                    ],
                ),
            ],
        )

    def add_clicked(self, e):
        # pk = self.db.create_task(self.new_task.value)[0]  # add new task to db and assign primary key
        pk = self.storage.create(self.new_task.value)
        task = Task(self.new_task.value, self.task_status_change, self.task_delete, self.storage, pk=pk)

        self.tasks.controls.append(task)
        # self.page.client_storage.set("tasks", self.tasks.controls)

        self.new_task.value = ''
        self.update()

    def task_status_change(self, task):
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and task.completed == False)
                or (status == "completed" and task.completed)
            )
        super().update()

    def tabs_changed(self, e):
        self.update()

def main(page: ft.Page):

    db = Database()

    page.title = "Todo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    #page.bgcolor = fm.Theme.bgcolor
    page.update()

    # create application instance
    todo = ft.View("/", [TodoApp(page)])
    todo.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # add application's root control to the page
    page.views.append(todo)

    page.go(page.route)

ft.app(main)