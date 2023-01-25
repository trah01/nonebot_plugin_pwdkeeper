import os
import yaml
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "bot.db")


def load():
    cur_path = os.path.dirname(os.path.realpath(__file__))
    yaml_path = os.path.join(cur_path, "config.yaml")  # 获取yaml文件路径
    f = open(yaml_path, 'r', encoding='utf-8')  # open方法打开直接读出来
    cfg = f.read()
    return cfg


def db(sql, mes=[]):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # try:
    result = c.execute(sql)
    # except:
    #     return '出错'
    if result:
        mes = list(result)
    conn.commit()
    conn.close()
    return mes


def is_in(message):
    try:
        sql = f'select 1 from {table_user} where {word[0]}="{str(message[0])}" and {word[1]}="{str(message[1])}";'
        res = db(sql)
    except IndexError:
        return '输入有误'
    if not res:
        return 'no'
    return 'in'


def create():
    sql = f"create table userdata(id  INTEGER not null constraint userdata_pk primary key autoincrement,{word[0]} TEXT not null,{word[1]} TEXT not null,{word[2]} TEXT not null);"
    try:
        db(sql)
        return '成功'
    except sqlite3.OperationalError:
        return "失败"


def query(message, res=[]):
    if len(message) == 1:
        if str(message[0]) == 'all':
            sql = f'select {word[0]},{word[1]},{word[2]} from {table_user}'
        elif str(message[0]) in word:
            sql = f'select {message[0]} from {table_user}'
        else:
            sql = f'select {word[0]},{word[1]},{word[2]} from {table_user} where {word[0]}="{str(message[0])}"'
    elif len(message) == 2:
        if message[0] not in word:
            sql = f'select {word[0]},{word[1]},{word[2]} from {table_user} where {word[0]}="{str(message[0])}" and {word[1]}="{str(message[1])}";'
        else:
            sql = f'select {word[0]},{word[1]},{word[2]} from {table_user} where {str(message[0])}="{str(message[1])}";'
    else:
        return '输入有误'
    print(sql)
    res = db(sql)
    if res:
        return res
    return '不存在'


def insert(message):
    res = is_in(message)
    if str(res) == 'no':
        try:
            sql = f'insert into {table_user}({word[0]},{word[1]},{word[2]}) values {message[0], message[1], message[2]}'
        except IndexError:
            return '输入有误'
        res = db(sql)
        if res:
            return '出错'
        return '插入成功'
    return '已存在'


def update(message):
    if str(is_in(message)) == 'in':
        try:
            sql = f'update {table_user} set {word[2]}="{message[2]}" where {word[0]}="{message[0]}" and {word[1]}="{message[1]}" '
        except IndexError:
            return '输入有误'
        res = db(sql)
        if res:
            return '出错'
        return '修改成功'
    return '不存在'


def drop(message):
    if str(is_in(message)) == 'in':
        try:
            sql = f'delete from {table_user} where {word[0]}="{message[0]}" and {word[1]}="{message[1]}"'
        except IndexError:
            return '输入有误'
        res = db(sql)
        if res:
            return '出错'
        return '删除成功'
    return '不存在'


def clean(message, sql=''):
    # message = word,key
    if message[0] in word:
        sql1 = f'select 1 from {table_user} where {message[0]} = "{message[1]}"'
        if db(sql1):
            try:
                sql = f'delete from {table_user} where {message[0]} = "{message[1]}"'
            except IndexError:
                return '输入有误'
    elif str(message[0]) == 'all':
        sql = f'delete from {table_user}'
    res = db(sql)
    if res:
        return '出错'
    return '已清空'


user_ini = yaml.safe_load(load())
word = user_ini["word"]
table_user = user_ini["table"]
