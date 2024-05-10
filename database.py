import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('todo.db', check_same_thread=False)
        self.cursor = self.con.cursor()
        self.create_task_table() # create tasks table

    def create_task_table(self):
        """Create tasks table"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks("
                            "id integer PRIMARY KEY AUTOINCREMENT,"
                            "task varchar(50) NOT NULL,"
                            "completed BOOLEAN NOT NULL )")
        self.con.commit()

    def create_task(self, task):
        """Create a task"""
        self.cursor.execute("INSERT INTO tasks(task, completed) "
                            "VALUES(?, ?)", (task, False))
        self.con.commit()

        # Getting the last entered item so we can add it to the task list
        created_task = self.cursor.execute("SELECT id, task FROM tasks WHERE task = ? and completed = 0", (task,)).fetchall()
        print(created_task)
        return created_task[-1]

    def get_tasks(self):
        """Get all completed and uncompleted tasks"""
        tasks = self.cursor.execute("SELECT id, task, completed FROM tasks").fetchall()

        # completed_tasks = self.cursor.execute("SELECT id, task FROM tasks WHERE completed = True").fetchall()
        return tasks

    def change_completed(self, taskid, completed):
        """Mark tasks as complete"""
        self.cursor.execute("UPDATE tasks SET completed=? WHERE id=?", (completed, taskid,))
        self.con.commit()

    def edit_task(self, taskid, text):
        """Edit task details"""
        self.cursor.execute("UPDATE tasks SET task=? WHERE id=?",(text, taskid))
        self.con.commit()

    def delete_task(self, taskid):
        """Delete a task"""
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskid,))
        self.con.commit()

    def close_db_connection(self):
        self.con.close()