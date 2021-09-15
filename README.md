## Stack

- [`FastAPI`](https://github.com/tiangolo/fastapi)
- [`Pydantic`](https://github.com/samuelcolvin/pydantic)
- [`TortoiseORM`](https://github.com/tortoise/tortoise-orm)

## Installation
- `git clone https://github.com/MaximZayats/rest-api-example`
- `cd rest-api-example`
- `pip install -r requirements.txt`
- Create a `.env` file and copy the settings from `.env.dist`
    - Available database urls:
        - SQLite: `sqlite://database.db`
            - `pip install aiosqlite`
        - PostgreSQL: `postgres://postgres:pass@db.host:5432/somedb`
            - `pip install asyncpg`
        - MySQL: `mysql://myuser:mypass:pass@db.host:3306/somedb`
            - `pip install aiomysql`
- _Make "application" directory as "Sources Root" (PyCharm)_

## Run Server

- `cd application`
    - `python app.py`
    - `uvicorn app:app`

## _Initial task and solution_

Необходимо создать приложение предоставляющее REST интерфейс со следующим функционалом:

### 1. База данных PostgreSQL (либо SQLite, или MS SQL, или MySQL), содержит информацию о сущностях (моделях):

- Задача
- Элемент задачи

**Поля Задачи**:

- id - число
- name - строка
- description - строка
- start_date - дата
- end_date - дата
- status - число

**Поля Элемента задачи**:

- id - число
- name - строка
- description - строка
- value - строка

Связь Задача — Элемент Задачи — _Один ко многим_.

### 2. REST интерфейсы

**Задачи**:

Документация: [`.../docs/`](http://40.67.229.195/docs)

- создать задачу
    - [`POST: .../tasks`](http://40.67.229.195/docs)
- удалить задачу со всеми связанными элементами
    - [`DELETE: .../tasks/{task_id}`](http://40.67.229.195/docs#/Tasks/delete_task_tasks__task_id__delete)
- обновить задачу
    - [`PUT: .../tasks/{task_id}`](http://40.67.229.195/docs#/Tasks/update_task_tasks__task_id__put)
    - [`PATCH: .../tasks/{task_id}`](http://40.67.229.195/docs#/Tasks/patch_task_tasks__task_id__patch)
- получить список всех задач
    - [`GET: .../tasks/`](http://40.67.229.195/docs#/Tasks/get_tasks_tasks_get)
- получить список всех задачу у которых в `name` присутствует указанный текст
    - [`GET: .../tasks?name__contains=hello`](http://40.67.229.195/docs#/Tasks/get_tasks_tasks_get)
- получить список всех задачу у которых `status` равен указанному значению
    - [`GET: .../tasks?status=1`](http://40.67.229.195/docs#/Tasks/get_tasks_tasks_get)
- получить список всех задач у которых `start_date` больше или равно указанной (например, `start_date_search`)
  и  `end_date`  меньше или равной указанной (например, `end_date_search`)
    - [`GET: .../tasks?start_date__gt=2021-09-11T12%3A12%3A12`](http://40.67.229.195/docs#/Tasks/get_tasks_tasks_get)
    - [`GET: .../tasks?start_date__lt=2021-09-11T12%3A12%3A12`](http://40.67.229.195/docs#/Tasks/get_tasks_tasks_get)
    - `gt, gte, lt, lte`
        - `gt` — Больше
        - `gte` — Больше или равно
        - `lt` — Меньше
        - `lte` — Меньше или равно

_Реализацию получения списков желательно сделать одним методом, подумайте как это можно сделать. Если не получится — то
можно сделать отдельными методами._

- `ссылка на метод`

**Элементы**:

- создать элемент
    - [`POST: .../tasks/elements`](http://40.67.229.195/docs#/Task%20Elements/create_task_element_tasks__task_id__elements_post)
- удалить элемент
    - [`DELETE: .../tasks/elements/{task_element_id}`](http://40.67.229.195/docs#/Task%20Elements/delete_task_tasks_elements__task_element_id__delete)
- обновить элемент
    - [`PUT: .../tasks/elements/{task_element_id}`](http://40.67.229.195/docs#/Tasks/update_task_tasks__task_id__put)
    - [`PATCH: .../tasks/elements/{task_element_id}`](http://40.67.229.195/docs#/Tasks/patch_task_tasks__task_id__patch)
- получить список всех элементов
    - [`GET: .../tasks/elements`](http://40.67.229.195/docs#/Tasks/get_tasks_tasks_get)
- получить список всех элементов у которых в `value` присутствует указанных текст
    - [`GET: .../tasks/elements?value__contains=hello`](http://40.67.229.195/docs#/Tasks/get_tasks_tasks_get)
- получить список всех элементов связанных с Задачей с указанным `id`
    - [`GET: .../tasks/{task_id}/elements`](http://40.67.229.195/docs#/Tasks/get_task_tasks__task_id__get)

_Реализацию получения списков желательно сделать одним методом, подумайте как это можно сделать. Если не получится — то
можно сделать отдельными методами._

**Отчет**:

- Отдельный REST интерфейс, который выгружает в формате XLSX список всех задач с их элементами, первая строка XLSX -
  название полей, вторая и последующие строки XLSX - значения полей задач и элементов
    - [`GET: .../report`](http://40.67.229.195/docs#/Report/get_report_report_get)

### 3. Код и сборка

* Код необходимо загрузить на GitHub и прислать ссылку.
* Если база данных не генерируется кодом, то на GitHub также необходимо загрузить SQL файл со схемой базы данных.
* В случае использования Java - проект должен собираться maven'ом или gradle.



