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
        if len(t) > 4:
            self.cats = t[4]
        else:
            self.cats = get_categories(task = self)            
    
    def __str__(self) -> str:
        return '{id}: {num}: {name}: {descript}'.format(id = self.id, num = self.num, name = self.name, descript = self.descript)

class Category:
    id = 0
    id_task = 0
    name = ''
    tag = ''
    descript = ''
    snips = []

    def __init__(self, t: tuple):
        self.id = t[0]
        self.id_task = t[1]
        self.name = t[2]
        self.tag = t[3]
        self.descript = t[4]
        if len(t) > 5:
            self.snips = t[5]
        else:
            self.snips = get_snips(cat = self)
    
    def __eq__(self, other):
        return self.name == other.name

    def __import_snips__(self, other):
        s_self_snip = set(x.name for x in self.snips)
        s_other_snip = set(x.name for x in other.snips)
        d_other_snip = dict(zip([snip.name for snip in other.snips], other.snips))
        for snip in set.difference(s_other_snip, s_self_snip): self.snips.append(d_other_snip[snip])
        self.snips.sort(key=lambda x: x.name, reverse=False)
        return self

    def __str__(self) -> str:
        return '{id}: {name} {descript}'.format(id=self.id, name=self.name, descript=self.descript)
        
class Snip:
    id = 0
    id_cat = 0
    name = ''
    install = 0
    seq_order = 0
    code = ''
    roll_back = ''
    descript = ''

    def __init__(self, t: tuple):
        self.id = t[0]
        self.id_cat = t[1]
        self.name = t[2]
        self.install = t[3]
        self.seq_order = t[4]
        self.code = t[5].replace('\r\n', '\n').strip()
        self.roll_back = t[6]
        self.descript = t[7]

    def __eq__(self, other):
            return self.name == other.name

    def __str__(self) -> str:
        return '{id}: {name}'.format(id=self.id, name=self.name)

def get_task(id: int) -> Task:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                    select id,
                           num,
                           name,
                           descript
                      from task
                      where id = {id_task}
                      order by num;
                    """.format(id_task = id))
    return Task(cur.fetchone())

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
                               tag,
                               descript
                        from category
                        where id_task = {id_task};
                    """.format(id_task = task.id))
    return [Category(result) for result in cur.fetchall()]

def get_all_categories() -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id,
                               id_task,
                               name,
                               tag,
                               descript
                        from category;
                    """)

    return [Category(result) for result in cur.fetchall()]

def get_snips(cat: Category) -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id,
                               id_cat,
                               name,
                               install,
                               seq_order,
                               code,
                               roll_back,
                               descript
                          from snip
                         where id_cat = {id_cat}
                         order by seq_order asc;
                    """.format(id_cat = cat.id))
    
    return [Snip(result) for result in cur.fetchall()]

def get_all_snips() -> list:
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""
                        select id,
                               id_cat,
                               name,
                               install,
                               seq_order,
                               code,
                               roll_back,
                               descript
                          from snip
                         order by seq_order asc;
                    """)
    
    return [Snip(result) for result in cur.fetchall()]    