import json
import sqlite3

class Todos:
    def __init__(self):
        # try:
        #     with open("todos.json", "r") as f:
        #         self.todos = json.load(f)
        # except FileNotFoundError:
        #     self.todos = []
        with sqlite3.connect("data.db") as conn:
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS todos (
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                done INTEGER NOT NULL
            );""")
            conn.commit()
            c.execute("""SELECT title, description, done FROM todos; """)
            data = c.fetchall()
        self.todos = []
        for row in data:
            temp_dict = {'title': row[0], 'description': row[1], 'done': row[2],}
            self.todos.append(temp_dict)


    def all(self):
        return self.todos

    def get(self, id):
        return self.todos[id]

    def create(self, data):
        data.pop('csrf_token')
        self.todos.append(data)

    def save_all(self):
        with sqlite3.connect("data.db") as conn:
            c = conn.cursor()
            c.executemany("""INSERT INTO todos (title, description, done) VALUES
                    (:title, :description, :done);""", self.todos)
            conn.commit()

    def update(self, id, data):
        data.pop('csrf_token')
        self.todos[id] = data
        self.save_all()