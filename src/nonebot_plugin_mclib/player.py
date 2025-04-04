from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    MessageEvent,
    GroupMessageEvent,
    Message,
    Bot,
    MessageSegment,
)
from nonebot.params import CommandArg
import sys, base64, json
from aiohttp import ClientSession, ClientTimeout

mc_body = on_command("mc-body", aliases={"MC-BODY"}, priority=10, block=True)
mc_uuid = on_command(
    "mc-uuid",
    aliases={"MC-UUID", "mc-UUID", "MC-uuid"},
    priority=10,
    block=True,
)
mc_avatar = on_command("mc-avatar", priority=10, block=True)
mc_skin = on_command("mc-skin", priority=10, block=True)


async def get_uuid(player: str) -> str | None:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"
    }
    async with ClientSession(headers=headers) as session:

        dicts: dict = await (
            await session.get(
                f"https://api.mojang.com/users/profiles/minecraft/{player}",
            )
        ).json()
    return dicts.get("id")


@mc_avatar.handle()
async def _(event: MessageEvent, bot: Bot, args: Message = CommandArg()):
    if location := args.extract_plain_text():
        async with ClientSession(
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"
            }
        ) as session:
            UUID = await get_uuid(player=location)
            message = MessageSegment.image(
                await (
                    await session.get(
                        f"https://crafatar.com/avatars/{UUID}?size=512&overlay",
                        timeout=ClientTimeout(total=5),
                    )
                ).read()
            )
            await mc_avatar.send(message)


@mc_uuid.handle()
async def _(event: MessageEvent, bot: Bot, args: Message = CommandArg()):
    if location := args.extract_plain_text():
        UUID = await get_uuid(player=location)
        if UUID == None:
            await mc_uuid.send(f"没有这个玩家！")
            return
        await mc_uuid.send(f"{location}的UUID是{UUID}")


@mc_skin.handle()
async def _(event: MessageEvent, bot: Bot, args: Message = CommandArg()):
    if location := args.extract_plain_text():
        async with ClientSession() as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"
            }
            UUID = await get_uuid(player=location)
            if UUID == None:
                await mc_skin.send(f"没有这个玩家！")
                return
            try:
                SKIN_dict = await (
                    await session.get(
                        f"https://sessionserver.mojang.com/session/minecraft/profile/{UUID}",
                        headers=headers,
                    )
                ).json()
            except:
                await mc_skin.send(f"查询失败！")
                return
            unbase = base64.b64decode(SKIN_dict["properties"][0]["value"])
            SKIN_LAST = json.loads(unbase)
            message = MessageSegment.image(
                await (await session.get(SKIN_LAST["textures"]["SKIN"]["url"])).read()
            )
            await mc_skin.send(message)

    else:
        await mc_skin.send("请输入玩家ID！")


@mc_body.handle()
async def _(event: MessageEvent, bot: Bot, args: Message = CommandArg()):
    if arg := args.extract_plain_text():
        async with ClientSession(
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"
            }
        ) as session:

            try:
                UUID = await get_uuid(player=arg)
                if UUID == None:
                    await mc_body.send(f"没有这个玩家！")
                    return
                image = await (
                    await session.get(
                        f"https://crafatar.com/renders/body/{UUID}?overlay",
                        timeout=ClientTimeout(total=5),
                    )
                ).read()
                await mc_body.send(MessageSegment.image(image))
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                await mc_body.send(f"过程发生了错误：{str(exc_value)}")

                return
    else:
        await mc_body.send("请输入玩家名！")
