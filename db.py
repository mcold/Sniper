# coding: utf-8
import sqlite3

db = 'DB.db'

class Task:
    id = 0
    num = 0
    name = ''
    descript = ''

    def __init__(self, t: tuple):
        self.id = t[0]
        self.num = t[1]
        self.name = t[2]
        self.descript = t[3]

class Category:
    id = 0
    id_task = 0
    name = ''
    descript = ''

    def __init__(self, t: tuple):
        self.id = t[0]
        self.id_task = t[1]
        self.name = t[2]
        self.descript = t[3]

class Snip:
    id = 0
    id_cat = 0
    name = ''
    install = 0
    code = ''
    roll_back = ''
    descript = ''

    def __init__(self, t: tuple):
        self.id = t[0]
        self.id_cat = t[1]
        self.name = t[2]
        self.install = t[3]
        self.code = t[4]
        self.roll_back = t[5]
        self.descript = t[6]

def get_tasks() -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                    select id,
                           num,
                           name,
                           descript
                      from task
                      order by num;
                    """)
    return [Task(result) for result in cur.fetchall()]                    

def get_categories(task: Task) -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id,
                               id_task,
                               name,
                               descript
                        from category
                        where id_task = {id_task};
                    """.format(id_task = task.id))

    return [Category(result) for result in cur.fetchall()]

def get_snips(cat: Category) -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id,
                               id_cat,
                               name,
                               install,
                               code,
                               roll_back,
                               descript
                          from snip
                         where id_cat = {id_cat};
                    """.format(id_cat = cat.id))
    
    return [Snip(result) for result in cur.fetchall()]