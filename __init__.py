from os import path
from nonebot.params import CommandArg, Command
from nonebot import on_command
from nonebot.permission import SUPERUSER
from .sql import *

word = sql.word

caxun = on_command("查询", aliases={"查", "cx"}, permission=SUPERUSER, priority=5, block=True)
init = on_command("初始化", aliases={"创建", "开始", "cj", "csh"}, permission=SUPERUSER, priority=5, block=True)
change = on_command("更改", aliases={"修改", "变更", "gg", "xg"}, permission=SUPERUSER, priority=5, block=True)
dele = on_command("删除", aliases={"删掉", "去除", "del", "sc"}, permission=SUPERUSER, priority=5, block=True)
claer = on_command("清空", aliases={"丢掉", "重置", "qk"}, permission=SUPERUSER, priority=5, block=True)
help = on_command("帮助", aliases={"help"}, permission=SUPERUSER, priority=5, block=True)
all = on_command('列表', aliases={str(word[0]), str(word[1]), str(word[2])}, permission=SUPERUSER, priority=5, block=True)
caru = on_command("插入", aliases={"插入", "增加", "加入", "添加", "保存", "记住", "cr"}, permission=SUPERUSER, priority=5,
                  block=True)


@init.handle()
async def start():
    result = sql.create()
    if result != "成功":
        pas = path.isfile(sql.db_path)
        if pas:
            await init.finish("已经初始化过了")
    await init.finish(result)



@caxun.handle()
async def cx(args=CommandArg(), results=[]):
    messages = args.extract_plain_text().strip().split('，')
    for message in messages:
        keys = message.split(' ')
        result = sql.query(keys)
        if type(result) == str:
            await caxun.send(message + str(result))
            continue
        results.append(result)
    print(results)
    for resa in results:
        for res in resa:
            await caxun.send(f'{word[0]}: {res[0]}\n{word[1]}: {res[1]}\n{word[2]}: {res[2]}')
    try:
        await caxun.finish(f'总共有{len(resa)}条数据')
    except UnboundLocalError:
        await caxun.finish('请重新查询')


@caru.handle()
async def cr(args=CommandArg(), res=[]):
    messages = args.extract_plain_text().strip().split('，')
    for message in messages:
        keys = message.split(' ')
        result = str(sql.insert(keys))
        res.append(f'  {message}{result}  \n')
    await caru.finish(''.join(res).strip('\n'))


@change.handle()
async def xg(args=CommandArg(), res=[]):
    messages = args.extract_plain_text().strip().split('，')
    for message in messages:
        keys = message.split(' ')
        result = str(sql.update(keys))
        res.append(f'  {message}{result}  \n')
    await change.finish(''.join(res).strip('\n'))


@dele.handle()
async def sc(args=CommandArg(), res=[]):
    messages = args.extract_plain_text().strip().split('，')
    for message in messages:
        keys = message.split(' ')
        result = str(sql.drop(keys))
        res.append(f'  {message}{result}  \n')
    await change.finish(''.join(res).strip('\n'))


@claer.handle()
async def qk(args=CommandArg(), res=[]):
    messages = args.extract_plain_text().strip().split('，')
    for message in messages:
        keys = message.split(' ')
        result = str(sql.clean(keys))
        res.append(f'  {message}{result}  \n')
    await change.finish(''.join(res).strip('\n'))


@help.handle()
async def bz():
    await help.finish('''不会用拉倒''')


@all.handle()
async def al(cmd=Command()):
    results = []
    result = query([cmd[0]])
    for res in result:
        results.append(res[0])
    await all.finish(f"{cmd[0]}有如下:{','.join(results)}")
