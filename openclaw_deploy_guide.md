# OpenClaw 部署完整指南
### 通过 macOS + 云端资源搭建 AI Gateway 并配置 GitHub Skills

---

**文档版本：** v1.0  
**更新日期：** 2026-04-13  
**适用平台：** macOS 主控端 + Linux VPS (云端 Gateway)

---

## 📋 目录

1. [什么是 OpenClaw？](#1-什么是-openclaw)
2. [系统架构图](#2-系统架构图)
3. [准备工作](#3-准备工作)
4. [方式一：macOS 本地快速部署](#4-方式一macos-本地快速部署)
5. [方式二：macOS + 云端 VPS 混合架构](#5-方式二macos--云端-vps-混合架构)
6. [远程访问配置（Tailscale / SSH）](#6-远程访问配置tailscale--ssh)
7. [GitHub 仓库同步与 Workspace 管理](#7-github-仓库同步与-workspace-管理)
8. [Skills 安装与配置](#8-skills-安装与配置)
9. [配置示例与常见问题](#9-配置示例与常见问题)

---

## 1. 什么是 OpenClaw？

OpenClaw 是一个**自托管的多渠道 AI Gateway**，它将 WhatsApp、Telegram、Discord、iMessage 等聊天应用连接到 AI 助手。

### 核心特性

- 🌐 **多渠道接入**：同时支持 WhatsApp、Telegram、Discord 等
- 🔐 **自托管**：数据完全在自己掌控中
- 🤖 **Agent 原生**：专为 AI 编码助手设计，支持工具调用、会话、多 Agent 路由
- 📱 **移动节点**：支持 iOS/Android 作为外设节点（摄像头、语音等）
- 🔧 **Skills 系统**：通过 ClawHub 安装扩展技能

### 典型使用场景

| 场景 | 说明 |
|------|------|
| **本地开发** | macOS 本地运行，随时调试 |
| **远程助手** | VPS 运行 Gateway，手机随时访问 |
| **团队共享** | 共享 Agent，通过 Slack/Discord 接入 |
| **技能扩展** | 通过 Skills 添加网页搜索、提醒等功能 |

---

## 2. 系统架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                           用户端                                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│  │  iPhone │  │ Android │  │   Mac   │  │  PC     │              │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘              │
│       │            │            │             │                    │
│       └────────────┴────────────┴─────────────┘                    │
│                          │  消息通道                                 │
│                          ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    Chat Apps                                 │  │
│  │   WhatsApp  Telegram  Discord  iMessage  Signal ...         │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                      │
└──────────────────────────────┼──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     OpenClaw Gateway                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │   Channel    │  │    Agent     │  │    Skills    │            │
│  │   Manager    │  │    Engine    │  │    Loader    │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│         │                  │                  │                    │
│         ▼                  ▼                  ▼                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    Workspace / Memory                        │  │
│  │         ~/.openclaw/workspace-*  /  memory/                │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  端口：18789 (WebSocket)   协议：ws://127.0.0.1:18789              │
└─────────────────────────────────────────────────────────────────────┘
                               │
           ┌───────────────────┴───────────────────┐
           ▼                                       ▼
┌─────────────────────────┐           ┌─────────────────────────┐
│     macOS Host          │           │     Linux VPS (Cloud)    │
│  ┌───────────────────┐  │           │  ┌───────────────────┐  │
│  │  Menu Bar App     │  │           │  │  Systemd Service  │  │
│  │  - Canvas         │  │           │  │  - Gateway        │  │
│  │  - Camera         │  │           │  │  - Channels       │  │
│  │  - Screen Record  │  │           │  │                   │  │
│  │  - system.run     │  │           │  │                   │  │
│  └───────────────────┘  │           │  └───────────────────┘  │
│         Node Mode       │           │         Remote Mode      │
└─────────────────────────┘           └─────────────────────────┘
           │                                       │
           └─────────────────┬─────────────────────┘
                             ▼
                   ┌─────────────────┐
                   │    Tailscale    │
                   │   (VPN Layer)   │
                   │  tailnet-access │
                   └─────────────────┘
```

### 架构说明

```
[移动端] ──消息──▶ [Gateway] ──▶ [Agent] ──▶ [Tools/Skills]
                              │
                              ▼
                    [Workspace Files]
                    [Memory Files]
                    [GitHub Sync]
```

---

## 3. 准备工作

### 3.1 硬件与账号要求

| 项目 | 要求 |
|------|------|
| **Node.js** | Node 24 (推荐) / Node 22.14+ (支持) |
| **macOS** | macOS 12+ |
| **云端 VPS** | 1核 1GB 最低配置，Ubuntu 20.04+ |
| **API Key** | 需要从模型提供商获取 (Anthropic/OpenAI 等) |
| **GitHub 账号** | 用于同步 Workspace |
| **Tailscale** | 免费账号，用于 VPN 访问 |

### 3.2 安装 Node.js

**macOS (通过 Homebrew):**

```bash
# 如果没有 Homebrew，先安装
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Node 24
brew install node@24

# 验证版本
node --version  # 应显示 v24.x.x
```

**Linux VPS (通过 NodeSource):**

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证版本
node --version
```

### 3.3 安装 Git

```bash
# macOS (通常已预装)
git --version

# Linux VPS
sudo apt-get update && sudo apt-get install -y git
```

---

## 4. 方式一：macOS 本地快速部署

### 4.1 安装 OpenClaw

```bash
# 推荐：使用官方安装脚本
curl -fsSL https://openclaw.ai/install.sh | bash
```

> **截图位置 1：终端运行安装脚本**
> ![安装脚本执行截图](images/install-script.png)

### 4.2 运行引导向导

```bash
# 启动完整引导流程
openclaw onboard --install-daemon
```

引导流程会要求你：

1. **选择模型提供商** (Anthropic / OpenAI / Google 等)
2. **输入 API Key**
3. **配置第一个渠道** (Telegram 建议作为第一个)
4. **设置访问控制** (谁可以与 Agent 对话)

> **截图位置 2：onboard 引导界面**
> ![Onboard 引导截图](images/onboard-wizard.png)

### 4.3 验证 Gateway 运行状态

```bash
# 检查 Gateway 状态
openclaw gateway status

# 查看详细健康状态
openclaw health
```

预期输出：

```
✅ Gateway is running
   Port: 18789
   URL: ws://127.0.0.1:18789
```

### 4.4 打开控制面板

```bash
# 在浏览器中打开控制 UI
openclaw dashboard
```

> **截图位置 3：Control UI 界面**
> ![Control UI 截图](images/control-ui.png)

### 4.5 配置 Telegram 渠道（示例）

```bash
# 1. 创建 Telegram Bot
# 在 Telegram 中搜索 @BotFather，发送 /newbot

# 2. 获取 Bot Token (格式: 123456:ABC-DEF...)

# 3. 配置到 openclaw.json
openclaw config set channels.telegram.botToken "你的BotToken"
openclaw config set channels.telegram.enabled true
openclaw config set channels.telegram.dmPolicy "pairing"

# 4. 重启 Gateway
openclaw gateway restart

# 5. 给你的 Bot 发送 /start 进行配对
```

### 4.6 安装 macOS 伴侣应用（可选）

从 [openclaw.ai](https://openclaw.ai) 下载 macOS 应用，可以获得：

- 菜单栏快速控制
- 原生通知
- Canvas / Camera / Screen Recording 集成
- 权限统一管理

> **截图位置 4：macOS Menu Bar App**
> ![Menu Bar App](images/menu-bar-app.png)

---

## 5. 方式二：macOS + 云端 VPS 混合架构

当你想让 Agent **7×24 小时运行**，但 Mac 不方便一直开着时，可以将 Gateway 部署在云端 VPS。

### 5.1 推荐云服务商

| 服务商 | 特点 | 价格 |
|--------|------|------|
| **DigitalOcean** | 简单易用，推荐新手 | ~$4/月 |
| **Oracle Cloud** | 永久免费 ARM 实例 | 免费 |
| **Hetzner** | 性价比最高 | ~€3/月 |
| **Railway** | 一键部署 | 按量计费 |

### 5.2 在 VPS 上安装 OpenClaw

**SSH 连接到你的 VPS：**

```bash
ssh root@你的VPS_IP
```

**安装 OpenClaw：**

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_24.x | bash -
apt-get install -y nodejs git

# 安装 OpenClaw
npm install -g openclaw@latest

# 验证安装
openclaw --version
```

> **截图位置 5：VPS 安装 OpenClaw**
> ![VPS 安装截图](images/vps-install.png)

### 5.3 配置 Systemd 服务（确保开机自启）

创建服务文件：

```bash
sudo nano /etc/systemd/system/openclaw.service
```

内容如下：

```ini
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu
ExecStart=/usr/bin/node /usr/bin/openclaw gateway
Restart=always
RestartSec=2
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache

# 可选：性能优化
Environment=OPENCLAW_NO_RESPAWN=1

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
# 重载 systemd
sudo systemctl daemon-reload

# 启用并启动服务
sudo systemctl enable openclaw
sudo systemctl start openclaw

# 查看状态
sudo systemctl status openclaw
```

> **截图位置 6：Systemd 服务状态**
> ![Systemd Status](images/systemd-status.png)

### 5.4 配置防火墙

```bash
# 开放必要端口 (仅限 SSH 和 Gateway)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 18789/tcp  # Gateway WebSocket
sudo ufw enable
sudo ufw status
```

### 5.5 在 macOS 上配置远程连接

编辑 `~/.openclaw/openclaw.json`：

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://127.0.0.1:18789",
      token: "你的-VPS-gateway-token",
    },
  },
}
```

---

## 6. 远程访问配置（Tailscale / SSH）

### 6.1 Tailscale 安装与配置（推荐）

Tailscale 让你像在局域网一样访问 VPS，且不需要暴露公网端口。

**安装 Tailscale：**

```bash
# macOS
brew install tailscale

# VPS (Ubuntu)
curl -fsSL https://tailscale.com/install.sh | sh
```

**登录并启动：**

```bash
# macOS
tailscale up

# VPS
sudo tailscale up
```

> **截图位置 7：Tailscale 连接**
> ![Tailscale](images/tailscale-up.png)

**获取 MagicDNS 地址：**

```bash
# 查看本机 Tailscale IP
tailscale ip -4

# MagicDNS 格式: username@machine.tailscale.net
# 例如: ubuntu@vps-1234@root@ts.net
```

### 6.2 配置 Tailscale Serve（Control UI 远程访问）

编辑 `~/.openclaw/openclaw.json`：

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" },
    auth: { mode: "password", password: "你的密码" },
  },
}
```

重启 Gateway 后，访问：

```
https://你的机器名.ts.net/
```

### 6.3 SSH 隧道方式（备选）

**创建 SSH 隧道：**

```bash
# 在 macOS 终端执行
ssh -N -L 18789:127.0.0.1:18789 ubuntu@你的-VPS-IP
```

之后在浏览器访问：`http://127.0.0.1:18789`

**持久化 SSH 隧道（LaunchAgent）：**

编辑 `~/Library/LaunchAgents/ai.openclaw.ssh-tunnel.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.openclaw.ssh-tunnel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/ssh</string>
        <string>-N</string>
        <string>-L</string>
        <string>18789:127.0.0.1:18789</string>
        <string>ubuntu@你的-VPS-IP</string>
    </array>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

启动：

```bash
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.openclaw.ssh-tunnel.plist
```

---

## 7. GitHub 仓库同步与 Workspace 管理

### 7.1 Workspace 目录结构

```
~/.openclaw/
├── workspace-pet-macos/          # 你的工作空间 (Git 仓库)
│   ├── SOUL.md                   # Agent 身份定义
│   ├── USER.md                   # 用户信息
│   ├── AGENTS.md                 # 工作准则
│   ├── MEMORY.md                 # 长期记忆
│   ├── memory/                   # 每日日志
│   │   └── 2026-04-13.md
│   ├── TOOLS.md                  # 工具配置
│   └── skills/                   # 本地 Skills
│       └── my-custom-skill/
├── openclaw.json                 # 主配置文件
└── skills/                       # 全局 Skills
```

### 7.2 创建 GitHub 仓库

**在 GitHub 上创建新仓库：**

1. 访问 [github.com/new](https://github.com/new)
2. 仓库名称：`openclaw-workspace-pet-macos`
3. 选择 **Private**（私人仓库）
4. **不要**初始化 README

> **截图位置 8：GitHub 创建仓库**
> ![GitHub New Repo](images/github-new-repo.png)

**本地初始化：**

```bash
cd ~/.openclaw/workspace-pet-macos
git init
git add .
git commit -m "Initial commit: OpenClaw workspace setup"
git branch -M main
git remote add origin https://github.com/你的用户名/openclaw-workspace-pet-macos.git
git push -u origin main
```

### 7.3 同步工作流

```bash
# 每次会话结束后的标准同步流程
cd ~/.openclaw/workspace-pet-macos

# 添加更改
git add .

# 提交 (按照 AGENTS.md 要求)
git commit -m "更新: 2026-04-13 工作总结"

# 推送到 GitHub
git push
```

### 7.4 在新设备恢复 Workspace

```bash
# 克隆仓库
git clone https://github.com/你的用户名/openclaw-workspace-pet-macos.git ~/.openclaw/workspace-pet-macos

# 安装 OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# 运行引导 (使用已有配置)
openclaw onboard
```

### 7.5 GitHub 与 Tailscale 的协同

```
┌─────────────┐     SSH/Git      ┌─────────────┐
│  macOS      │◀───────────────▶│   VPS        │
│             │                 │             │
│ Workspace   │    Tailscale    │   Gateway   │
│ (本地开发)   │◀───────────────▶│ (7×24 运行)  │
│             │                 │             │
└─────────────┘                 └─────────────┘
      │                                │
      └────────── git push ────────────┘
                 GitHub 同步
```

---

## 8. Skills 安装与配置

### 8.1 什么是 Skills？

Skills 是 OpenClaw 的扩展模块，通过 ClawHub 安装，为 Agent 添加特定能力。

**已内置的 Skills：**

| Skill | 功能 |
|-------|------|
| `weather` | 天气预报 |
| `web-access` | 网页搜索与抓取 |
| `tavily-search` | Tavily 搜索 |
| `memory-setup` | 记忆系统配置 |
| `qqbot-*` | QQ 相关功能 |

### 8.2 通过 ClawHub 安装 Skills

```bash
# 搜索 Skills
openclaw skills search "web search"

# 安装指定 Skill
openclaw skills install tavily-search

# 更新所有 Skills
openclaw skills update --all

# 查看已安装 Skills
openclaw skills list
```

> **截图位置 9：Skills 安装**
> ![Skills Install](images/skills-install.png)

### 8.3 通过 clawhub CLI 安装（高级）

```bash
# 安装 clawhub CLI
npm i -g clawhub

# 登录 (可选，用于发布)
clawhub login

# 安装 Skill
clawhub install my-skill-pack

# 更新所有
clawhub update --all
```

### 8.4 配置 Skill API Keys

某些 Skills 需要 API Key，配置方法：

```bash
# 设置 API Key
openclaw config set skills.entries.tavily-search.apiKey "你的-Tavily-API-Key"
```

或在 `openclaw.json` 中：

```json5
{
  skills: {
    entries: {
      "tavily-search": {
        apiKey: "你的-Tavily-API-Key",
      },
    },
  },
}
```

### 8.5 创建自定义 Skill

**Skill 目录结构：**

```
skills/my-custom-skill/
├── SKILL.md          # Skill 定义 (必需)
├── scripts/          # 脚本文件
├── references/       # 参考文档
└── config.json       # 配置
```

**SKILL.md 示例：**

```markdown
# My Custom Skill

_描述这个 Skill 做什么_

## 使用方法

当用户说 ... 时使用此 Skill

## 配置要求

- API Key: 需要从 xxx 获取
```

发布到 ClawHub：

```bash
clawhub skill publish ./skills/my-custom-skill \
  --slug my-custom-skill \
  --name "My Custom Skill" \
  --version 1.0.0 \
  --tags latest
```

---

## 9. 配置示例与常见问题

### 9.1 完整配置示例

`~/.openclaw/openclaw.json`:

```json5
{
  // Gateway 配置
  gateway: {
    port: 18789,
    bind: "loopback",           // 本地: loopback | 远程: tailnet
    tailscale: { mode: "serve" },
    auth: {
      mode: "token",
      token: "你的-gateway-token",
    },
  },

  // Agent 配置
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-6",
      },
      workspace: "~/.openclaw/workspace-pet-macos",
    },
  },

  // 渠道配置
  channels: {
    telegram: {
      enabled: true,
      botToken: "你的-Bot-Token",
      dmPolicy: "pairing",
    },
    whatsapp: {
      enabled: false,
      allowFrom: ["+15551234567"],
    },
  },

  // Skills 配置
  skills: {
    entries: {
      "tavily-search": {
        apiKey: "你的-Tavily-Key",
      },
    },
  },
}
```

### 9.2 常用命令速查

| 命令 | 说明 |
|------|------|
| `openclaw gateway status` | 查看 Gateway 状态 |
| `openclaw gateway restart` | 重启 Gateway |
| `openclaw dashboard` | 打开控制面板 |
| `openclaw health` | 健康检查 |
| `openclaw doctor` | 诊断问题 |
| `openclaw config get <key>` | 获取配置项 |
| `openclaw config set <key> <value>` | 设置配置项 |
| `openclaw skills list` | 列出 Skills |
| `openclaw skills install <name>` | 安装 Skill |

### 9.3 常见问题

**Q: Gateway 无法启动？**

```bash
# 运行诊断
openclaw doctor

# 查看日志
openclaw logs
```

**Q: Telegram Bot 没有响应？**

1. 检查 Bot Token 是否正确
2. 确认 Bot 已发送 `/start`
3. 检查 `dmPolicy` 设置

**Q: 远程连接失败？**

1. 确认 VPS 上的 Gateway 正在运行
2. 检查防火墙设置
3. 验证 Token 是否正确

**Q: Skills 不生效？**

1. 确认 Skill 已正确安装
2. 重启 Gateway：`openclaw gateway restart`
3. 检查 API Key 配置

---

## 📚 附录

### A. 相关文档链接

| 资源 | 链接 |
|------|------|
| OpenClaw 官网 | https://openclaw.ai |
| 官方文档 | https://docs.openclaw.ai |
| ClawHub (Skills 市场) | https://clawhub.ai |
| GitHub 仓库 | https://github.com/openclaw/openclaw |
| Discord 社区 | https://discord.com/invite/clawd |

### B. 推荐阅读

- [Getting Started](https://docs.openclaw.ai/start/getting-started)
- [Gateway 配置](https://docs.openclaw.ai/gateway/configuration)
- [Tailscale 集成](https://docs.openclaw.ai/gateway/tailscale)
- [Channels 接入](https://docs.openclaw.ai/channels)
- [Skills 系统](https://docs.openclaw.ai/tools/skills)

### C. 架构决策记录

| 日期 | 决策 | 原因 |
|------|------|------|
| 2026-04-13 | 采用 Tailscale Serve | 安全且简单的远程访问方案 |
| 2026-04-13 | Workspace GitHub 同步 | 确保跨设备一致性和备份 |
| 2026-04-13 | Skills 通过 ClawHub 管理 | 官方支持的标准化方式 |

---

**文档制作：** pet-competitor  
**最后更新：** 2026-04-13
