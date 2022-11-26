# coding: utf-8
import xml.etree.ElementTree as ET
from pathlib import Path
from db import Category, Task, Snip
from db import get_snips, get_categories, get_task, get_all_categories

file_snips = str(Path.home()) + r'\AppData\Roaming\SQL Developer\UserSnippets.xml'
xml_start = "<?xml version = '1.0' encoding = 'UTF-8'?>\n"

def get_xml_task_snips(task: Task) -> str:
    root = ET.Element('snippets')
    for cat in task.cats:
        category = ET.SubElement(root, 'group', {'category': cat.name, 'language': 'PLSQL'})
        for snip in cat.snips:
            snippet = ET.SubElement(category, 'snippet', {'name': snip.name, 'description': snip.descript})
            code = ET.SubElement(snippet, 'code')
            code.text = '\n{code}\n'.format(code=snip.code.replace('\r\n', '\n').strip())
    ET.indent(root)
    return ET.tostring(root).decode('utf-8').replace('&lt;', '<').replace('&gt;', '>')

def get_xml_cat_snips(cat: Category) -> str:
    root = ET.Element('snippets')
    category = ET.SubElement(root, 'group', {'category': cat.name, 'language': 'PLSQL'})
    for snip in get_snips(cat = cat):
        snip = ET.SubElement(category, 'snippet', {'name': snip.name, 'description': snip.descript})
        code = ET.SubElement(snip, 'code')
        code.text = '\n' + snip.code
    ET.indent(root)
    return ET.tostring(root).decode('utf-8').replace('&lt;', '<').replace('&gt;', '>')

def gen_xml_cat_snips(cat: Category) -> None:
    with open(file_snips, 'w') as f: f.write(xml_start + get_xml_cat_snips(cat = cat))

def gen_xml_task_snips(task: Task) -> None:
    with open(file_snips, 'w') as f: f.write(xml_start + get_xml_task_snips(task = task))

def gen_xml_user_snips(id_task: int) -> None:
    gen_xml_task_snips(task = get_task(id = id_task))

def get_db_snips() -> ET.Element:
    root = ET.Element('snippets')
    for cat in get_all_categories():
        category = ET.SubElement(root, 'group', {'category': cat.name, 'language': 'PLSQL'})
        for snip in cat.snips:
            snippet = ET.SubElement(category, 'snippet', {'name': snip.name, 'description': snip.descript})
            code = ET.SubElement(snippet, 'code')
            code.text = snip.code.replace('\n', '')
    ET.indent(root)
    return root

def sync_snips() -> None:
    root = ET.Element('snippets')

def get_xml_task_cat_snips(l_cat: list) -> str:
    root = ET.Element('snippets')
    for cat in l_cat:
        category = ET.SubElement(root, 'group', {'category': cat.name, 'language': 'PLSQL'})
        for snip in cat.snips:
            snippet = ET.SubElement(category, 'snippet', {'name': snip.name, 'description': snip.descript})
            code = ET.SubElement(snippet, 'code')
            code.text = '\n{code}\n'.format(code=snip.code.strip())
    ET.indent(root)
    return ET.tostring(root).decode('utf-8').replace('&lt;', '<').replace('&gt;', '>')

def get_xml_cat_tree(file: str) -> str:
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(file, parser=parser)
    root = tree.getroot()
    l_cat = list()
    b_exists = False
    for cat_ in root:
        cat = Category((0, 0, cat_.attrib['category'], '', '', []))
        for i in range(len(l_cat)):
            if cat == l_cat[i]:
                b_exists = True
                break
            else:
                continue
        if not b_exists:
            for sn in cat_:
                for code in sn: cat.snips.append(Snip([0, 0, sn.attrib['name'], 0, 0, code.text, '', '']))
            l_cat.append(cat)
        else:
            b_exists = False
        cat.snips.sort(key=lambda x: x.name, reverse=False)
    l_cat.sort(key=lambda x: x.name, reverse=False)
    return l_cat

def regen_xml_snips(file: str):
    res = get_xml_task_cat_snips(l_cat=get_xml_cat_tree(file=file))
    with open(file_snips, 'w') as f: f.write(xml_start + res)

if __name__ == "__main__":
    gen_xml_user_snips(1)