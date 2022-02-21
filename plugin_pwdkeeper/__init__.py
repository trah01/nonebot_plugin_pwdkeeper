from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, Message
from nonebot.params import CommandArg
from nonebot import on_command
from nonebot.permission import SUPERUSER
from .sqlall import sqlf, word

caxun = on_command("查询", aliases={"查", "cx"}, permission=SUPERUSER, priority=5, block=True)
caru = on_command("插入", aliases={"插入", "增加", "加入", "添加", "保存", "记住", "cr"}, permission=SUPERUSER, priority=5,
                  block=True)
change = on_command("更改", aliases={"修改", "变更", "gg", "xg"}, permission=SUPERUSER, priority=5, block=True)
dele = on_command("删除", aliases={"删掉", "去除", "del", "sc"}, permission=SUPERUSER, priority=5, block=True)
help = on_command("帮助", aliases={"help"}, permission=SUPERUSER, priority=5, block=True)


@caxun.handle()
async def _(bot: Bot, event: PrivateMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split('，')
    for ins in args:
        if 0 < len(ins.split()) < 3:    #检测是否满足语法
            result, status = sqlf.query(ins.split())    #结果和状态
        else:
            await caxun.finish("格式错误")
    if status == 'yes':
        for res in result:
            if len(res) == 1:
                msg = f"{ins}名有: {res[0]}"    #查询单数据
            else:
                msg = f"{word[0]}为：{res[0]}\n{word[1]}为：{res[1]}\n{word[2]}为：{res[2]}"    #查询多数据
            await caxun.send(msg)
    else:
        await caxun.finish(status)
    await caxun.finish("共有%d条数据" % len(result))


@caru.handle()
async def _(bot: Bot, event: PrivateMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split('，')
    result = []
    for ins in args:
        if len(ins.split()) < 3:        #格式检测，并写入操作结果
            result.append("格式错误")
        else:
            result.append(sqlf.insert(ins.split()))
    await caru.finish(','.join(str(x) for x in result))     #对每组结果进行输出


@change.handle()
async def _(bot: Bot, event: PrivateMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split('，')
    result = []
    for ins in args:
        if len(ins.split()) < 3:
            result.append("格式错误")
        else:
            result.append(sqlf.modify(ins.split()))
    await change.finish(','.join(str(x) for x in result))


@dele.handle()
async def _(bot: Bot, event: PrivateMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await dele.finish("请输入值")
    elif len(args) == 2 or args[0] == "allthing":
        result = sqlf.delete(args)
        await dele.finish(result)
    else:
        await dele.finish("格式错误")

@help.handle()
async def _(bot: Bot, event: PrivateMessageEvent, args: Message = CommandArg()):
    info = '使用说明\n所有关键字用空格分开\n\n默认操作如下:\n查询:\n"查询 软件名 用户名"\n比如:查询 QQ 1234321\n\n"查询 类型(软件名，用户名，密码) 软件名/用户名/密码"\n比如 :查询 ' \
       '用户名 QQ，即查询QQ下所有的用户信息\n\n"查询 all"查询所有数据\n\n插入:\n"插入 软件名，用户名，密码"(可插入多数据，注意格式，用中文逗号分割)\n比如:插入 QQ 123456 pw123，QQ ' \
       '123321 pa111\n\n更改:\n"更改 软件名 用户名 新密码"(可插入多数据，注意格式，用中文逗号分割)\n比如:更改 QQ 123456 aaa123，QQ 123321 ' \
       'pa111\n\n删除:\n"删除 软件名 用户名"比如:删除 QQ 123456\n\n"删除 allthing"删除所用数据，慎用\n '
    await help.finish(info)