import pymysql
import os
import yaml


class sqlf:
    curPath = os.path.dirname(os.path.realpath(__file__))
    yamlPath = os.path.join(curPath, "config.yaml")  # 获取yaml文件路径
    f = open(yamlPath, 'r', encoding='utf-8')  # open方法打开直接读出来
    cfg = f.read()

    global word, tableu,user_ini #自定义的关键字和表

    user_ini = yaml.load(cfg)
    word = user_ini["word"]
    tableu = user_ini["table"]

    # db = pymysql.connect(host=user_ini["host"],     #自定义的数据库连接
    #                      port=int(user_ini["port"]),
    #                      user=user_ini["user"],
    #                      password=user_ini["password"],
    #                      database=user_ini["database"]
    #                      )
    # cursor = db.cursor()     # 使用 cursor() 方法创建一个游标对象 cursor

    def query(list):
        db = pymysql.connect(host=user_ini["host"],     #自定义的数据库连接
                            port=int(user_ini["port"]),
                            user=user_ini["user"],
                            password=user_ini["password"],
                            database=user_ini["database"]
                            )
        cursor = db.cursor()     # 使用 cursor() 方法创建一个游标对象 cursor
        b = []
        if len(list) == 1:
            if list[0] in (word):
                sql = f"SELECT DISTINCT {str(list[0])} FROM {tableu};"  #关键字的单独查询
            elif list[0] == "all":
                sql = f"SELECT {word[0]},{word[1]},{word[2]} FROM {tableu};"    #所有数据，除了主键
            else:
                return b, "值错误，请输入正确列名或者all"
        else:
            if list[0] in (word):
                sql = f"SELECT {word[0]},{word[1]},{word[2]} FROM {tableu} WHERE {str(list[0])} = '{str(list[1])}'"     #单软件名下的数据查询
            else:
                sql = f"SELECT {word[0]},{word[1]},{word[2]} FROM {tableu} WHERE  {word[0]} ='{str(list[0])}' AND {word[1]} ='{str(list[1])}' "     #软件名用户名的结合查询
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            db.commit()
            db.close()
            cursor.close()
            if results:
                for row in results:
                    a = []
                    for x in range(0, len(row)):    #将结果加入b列表
                        xx = row[x]
                        a.append(xx)
                    b.append(a)
                return b, "yes"     #返回列表与状态
            else:
                return b, "没有查到"
        except:
            return b, "失败"
        
    def insert(list):
        db = pymysql.connect(host=user_ini["host"],     #自定义的数据库连接
                            port=int(user_ini["port"]),
                            user=user_ini["user"],
                            password=user_ini["password"],
                            database=user_ini["database"]
                            )
        cursor = db.cursor()     # 使用 cursor() 方法创建一个游标对象 cursor
        sql = f"insert into {tableu} ({word[0]},{word[1]},{word[2]}) values ('{str(list[0])}','{str(list[1])}','{str(list[2])}')"
        list_a = []
        list_a.append(str(list[0]))
        list_a.append(str(list[1]))
        _, yz = sqlf.query(list_a)
        if str(yz) != "yes":    #验证是否存在，仅针对软件名和用户名进行重复验证
            try:
                cursor.execute(sql)
                db.commit()
                db.close()
                cursor.close()
                return "插入成功"
            except:
                return "插入失败"
        else:
            return "已经存在"

    def modify(list):
        db = pymysql.connect(host=user_ini["host"],     #自定义的数据库连接
                            port=int(user_ini["port"]),
                            user=user_ini["user"],
                            password=user_ini["password"],
                            database=user_ini["database"]
                            )
        cursor = db.cursor()     # 使用 cursor() 方法创建一个游标对象 cursor
        sql = f"update {tableu} set {word[2]} ='{str(list[2])}' WHERE  {word[0]} ='{str(list[0])}' and  {word[1]} ='{str(list[1])}' "
        list_a = []
        list_a.append(str(list[0]))
        list_a.append(str(list[1]))
        _, yz = sqlf.query(list_a)
        if str(yz) == "yes":        #是否存在该数据查询
            try:
                cursor.execute(sql)
                db.commit()
                db.close()
                cursor.close()
                return "修改成功"
            except:
                return "修改失败"
        else:
            return "没有这个东西"

    def delete(list):
        db = pymysql.connect(host=user_ini["host"],     #自定义的数据库连接
                            port=int(user_ini["port"]),
                            user=user_ini["user"],
                            password=user_ini["password"],
                            database=user_ini["database"]
                            )
        cursor = db.cursor()     # 使用 cursor() 方法创建一个游标对象 cursor
        list_a = []
        if str(list[0]) in (word):
            sql = f"delete from {tableu} WHERE {str(list[0])} ='{str(list[1])}'"        #单数据类型删除，用户名等
        elif str(list[0]) == "allthing":                #使用allthing，稍微复杂一点，避免误操
            sql = cursor.execute(f"delete from {tableu}")
            db.close()
            cursor.close()
            return "数据已经清空"
        else:
            sql = f"delete from {tableu} WHERE {word[0]} ='{str(list[0])}' and  {word[1]} ='{str(list[1])}' "       #软件名用户名组合匹配删除
        list_a.append(str(list[0]))
        list_a.append(str(list[1]))
        _, yz = sqlf.query(list_a)
        if str(yz) == "yes":
            try:
                cursor.execute(sql)
                db.commit()
                db.close()
                cursor.close()
                return "删除成功"
            except:
                return "删除失败"
        else:
            return "没有这个东西"
