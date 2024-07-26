# -*- coding: utf-8 -*-
import asyncio
import sys, os
import requests

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message

sys.path.append(os.getcwd())

yy_qbot_config = read(os.path.join(os.path.dirname(__file__), ".yy_config.yaml"))

_log = logging.get_logger()

# TINYURL_API_URL = "http://tinyurl.com/api-create.php"

# 配置
GITHUB_API_URL = "https://api.github.com"
OWNER = "Sunrisepeak"  # 替换为你的 GitHub 用户名
REPO = "opensource-community"   # 替换为你的仓库名称
CHECK_INTERVAL = 5  # 检查间隔（秒）

# 请求头
HEADERS = {
    "Authorization": f"token {yy_qbot_config['github-token']}"
}

# 获取最新的问题列表
def get_latest_issues():
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/issues"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

class MyClient(botpy.Client):

    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        issues = get_latest_issues()
        issue_nums = len(issues)
        issue_content = f"\n[Issue Lists | 问题列表] - {issue_nums}"
        for issue in issues:
            issue_nums -= 1
            labels = ", ".join(l['name'] for l in issue['labels'])
            issue_content += f"""
---{issue_nums}---
Title: {issue['title']}
Lables: {labels}
Link:

{issue['html_url']}

"""
        issue_content = issue_content.replace("github.com", "github\n.com")

        messageResult = await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=issue_content
        )
        _log.info(messageResult)

if __name__ == "__main__":
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=yy_qbot_config["appid"], secret=yy_qbot_config["secret"])