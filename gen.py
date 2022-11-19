# coding: utf-8
from db import Category, Task
from db import get_snips, get_categories, get_task
import xml.etree.ElementTree as ET

file_snips = 'UserSnippets.xml'
xml_start = "<?xml version = '1.0' encoding = 'UTF-8'?>\n"

def get_xml_task_snips(task: Task) -> str:
    root = ET.Element('snippets')
    for cat in get_categories(task = task):
        category = ET.SubElement(root, 'group', {'category': cat.name, 'language': 'PLSQL'})
        for snip in get_snips(cat = cat):
            snippet = ET.SubElement(category, 'snippet', {'name': snip.name, 'description': snip.descript})
            code = ET.SubElement(snippet, 'code')
            code.text = snip.code.replace('\n', '')
    ET.indent(root)
    return ET.tostring(root).decode('utf-8').replace('&lt;', '<').replace('&gt;', '>')

def get_xml_cat_snips(cat: Category) -> str:
    root = ET.Element('snippets')
    category = ET.SubElement(root, 'group', {'category': cat.name, 'language': 'PLSQL'})
    for snip in get_snips(cat = cat):
        snip = ET.SubElement(category, 'snippet', {'name': snip.name, 'description': snip.descript})
        code = ET.SubElement(snip, 'code')
        code.text = snip.code
    ET.indent(root)
    return ET.tostring(root).decode('utf-8').replace('&lt;', '<').replace('&gt;', '>')

def gen_xml_cat_snips(cat: Category) -> None:
    with open(file_snips, 'w') as f: f.write(xml_start + get_xml_cat_snips(cat = cat))

def gen_xml_task_snips(task: Task) -> None:
    with open(file_snips, 'w') as f: f.write(xml_start + get_xml_task_snips(task = task))

def gen_xml_user_snips(id_task: int) -> None:
    gen_xml_task_snips(task = get_task(id = id_task))


if __name__ == "__main__":
    gen_xml_user_snips(1)
