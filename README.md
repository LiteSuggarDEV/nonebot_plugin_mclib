<div align="center">
  <a href="https://github.com/JohnRichard4096/nonebot_plugin_mclib/">
    <img src="https://github.com/user-attachments/assets/b5162036-5b17-4cf4-b0cb-8ec842a71bc6" width="200" alt="Logo">
  </a>
  <h1>MCLib</h1>
  <h3>我的世界玩家/服务器查询插件～</h3>


[![PyPI Version](https://img.shields.io/pypi/v/nonebot-plugin-mclib?color=blue&style=flat-square)](https://pypi.org/project/nonebot-plugin-mclib/)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue?logo=python&style=flat-square)](https://www.python.org/)
[![NoneBot Version](https://img.shields.io/badge/nonebot2-2.0.0rc4+-blue?style=flat-square)](https://nonebot.dev/)
[![License](https://img.shields.io/github/license/JohnRichard4096/nonebot_plugin_mclib?style=flat-square)](LICENSE)
[![QQ Group](https://img.shields.io/badge/QQ%E7%BE%A4-1002495699-blue?style=flat-square)](https://qm.qq.com/q/PFcfb4296m)

</div>

# 快速开始
1. 使用 pip 安装插件
```bash
pip install nonebot-plugin-mclib
```
并在pyproject.toml中添加插件
```toml
plugins = ["nonebot_plugin_mclib"]
# 添加nonebot_plugin_mclib
```

# 使用方法
## 指令-玩家

- `/mc_uuid <玩家名>` 获取正版玩家的UUID
- `/mc_skin <玩家名>` 获取正版玩家的皮肤
- `/mc_avatar <玩家名>` 获取正版玩家的皮肤大头
- `/mc_body <玩家名>` 获取正版玩家的皮肤渲染图

## 指令-MC服务器
- `/mc_java <服务器地址/服务器地址:端口>` 获取Java版服务器信息（支持SRV解析）
- `/mc_bedrock <服务器地址/服务器地址:端口>` 获取Bedrock版服务器信息