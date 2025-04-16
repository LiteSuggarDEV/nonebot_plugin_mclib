from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message, Bot
from nonebot.params import CommandArg
from mcstatus import JavaServer, BedrockServer
from mcstatus.status_response import BedrockStatusResponse
import dns.resolver
import ipaddress
from nonebot import logger
import sys

java_status = on_command("mc_java", aliases={"mcjava", "mc_java_status", "java服务器"})
be_status = on_command(
    "mc_be", aliases={"mcbedrock", "mc_bedrock_status", "bedrock服务器"}
)


async def resolve_srv_record(host: str):
    try:
        query = f"_minecraft._tcp.{host}"
        srv_ans = dns.resolver.resolve(query, "SRV")
        return [
            {
                "priority": r.priority,
                "weight": r.weight,
                "port": r.port,
                "target": r.target.to_text(),
            }
            for r in srv_ans
        ]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN) as e:
        logger.warning(f"SRV lookup failed: {str(e)}")
        return None


def parse_host_port(location: str) -> tuple[str, int]:
    host_port_args = location.split(":", maxsplit=1)
    host = host_port_args[0]
    port = int(host_port_args[1]) if len(host_port_args) > 1 else 25565
    return host, port


async def get_server_status(host: str, port: int) -> tuple[JavaServer, dict]:
    server = JavaServer.lookup(f"{host}:{port}")
    status = server.status()
    return server, status.raw


def resolve_a_record(host: str) -> str:
    return str(dns.resolver.resolve(host, "A")[0])


def format_be_status_message(raw: BedrockStatusResponse, address: str) -> str:
    return f"""成功获取到服务器信息！
    服务器地址：{address}
    服务器版本/信息：{raw.version}
    延迟：{int(raw.latency)}ms
    地图名称：{raw.map_name}
    游戏模式：{raw.gamemode}
    玩家数{raw.players.online}/{raw.players.max}
    玩家数：{raw.players_online}/{raw.players_max}
    MOTD: {raw.motd}
    """


def format_status_message(
    host: str, port: int, ip: str, data: dict, latency: float
) -> str:
    return f"""成功获取到服务器信息！
服务器地址：{host}:{port}
服务器IP：{ip}
服务器延迟：{int(latency)}ms
服务器协议版本：{data["version"]["protocol"]}
服务端版本/信息：{data["version"]["name"]}
MOTD: {data["description"].get("text", data["description"])}
玩家数：{data["players"]["online"]}/{data["players"]["max"]}"""


@java_status.handle()
async def _(event: MessageEvent, bot: Bot, args: Message = CommandArg()):
    if not (location := args.extract_plain_text()):
        await java_status.send("请输入地址！格式：server_ip:port")
        return

    try:
        host, port = parse_host_port(location)

        # 尝试直接连接
        try:
            server, data = await get_server_status(host, port)
            ip = resolve_a_record(host)
            return await java_status.send(
                format_status_message(host, port, ip, data, server.status().latency)
            )
        except Exception as e:
            logger.warning(f"Direct connection failed: {str(e)}")

        try:
            ipaddress.ip_address(host)
        except ValueError:
            pass
        else:
            # 尝试SRV记录查询
            srv_details = await resolve_srv_record(host)
            if srv_details:
                new_host = srv_details[0]["target"].rstrip(".")
                new_port = srv_details[0]["port"]
                server, data = await get_server_status(new_host, new_port)
                ip = resolve_a_record(new_host)
                return await java_status.send(
                    format_status_message(
                        new_host, new_port, ip, data, server.status().latency
                    )
                )

        await java_status.send("服务器似乎不在线！")

    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        await java_status.send(f"发生错误！{exc_value}")


@be_status.handle()
async def _(event: MessageEvent, bot: Bot, args: Message = CommandArg()):
    if not (location := args.extract_plain_text()):
        await be_status.send("请输入地址！格式：server_ip:port")
        return
    host, port = parse_host_port(location)
    try:
        server = BedrockServer.lookup(f"{host}:{port}")
        status = server.status()
        await be_status.send(format_be_status_message(status, f"{host}:{port}"))
    except Exception:
        await be_status.send("获取失败（服务器不在线吗？）")
