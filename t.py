from nicegui import ui
from requests import get

import quasar

table = quasar.table()
table.selection.type("single")

table.columns.add("title", "Title", "title")
table.columns.add("completed", "Completed", "completed")

ui.button("Add ID column", on_click=lambda: table.columns.add("id", "id", "id"))

req = get("https://jsonplaceholder.typicode.com/todos")
todos = req.json()

for todo in todos:
    table.rows.add(todo)