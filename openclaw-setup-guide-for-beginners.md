# OpenClaw 零基础安装配置指南

> 本指南面向完全没有编程背景的用户，每一步都配有截图说明和操作要点。看完就能自己搭起来。

---

## 目录

1. [安装 Node.js（必须先装这个）](#1-安装-nodejs)
2. [安装 OpenClaw](#2-安装-openclaw)
3. [启动 OpenClaw 并注册账号](#3-启动-openclaw-并注册账号)
4. [配置 QQBot（接收 QQ 消息）](#4-配置-qqbot接收-qq-消息)
5. [配置 Web 控制台访问（bind 设置）](#5-配置-web-控制台访问bind-设置)
6. [常见问题](#6-常见问题)

---

## 1. 安装 Node.js

OpenClaw 是基于 Node.js 运行的，必须先装它。

### 第一步：下载 Node.js

1. 打开浏览器，访问：**https://nodejs.org/**
2. 点击左侧绿色大按钮 **"LTS"**（长期支持版，稳定）
3. 下载完成会得到一个 `.pkg` 文件（大约 30MB）

### 第二步：安装 Node.js

1. 双击下载的 `.pkg` 文件
2. 一路点"继续"→"同意"→"安装"
3. 输入你的 Mac 密码
4. 等进度条走完，点"安装完成"

### 第三步：验证安装成功

1. 打开 **终端**（Terminal）：按 `Command + 空格`，搜索"终端"，回车
2. 在终端里输入这两行，每行回车：

```bash
node -v
npm -v
```

**如果看到版本号（比如 `v20.x.x`），就说明安装成功了！** 🎉

---

## 2. 安装 OpenClaw

### 第一步：打开终端

按 `Command + 空格`，搜索"终端"，回车

### 第二步：运行安装命令

在终端里粘贴这行命令，回车：

```bash
npm install -g openclaw
```

**注意：** 粘贴方法：Command + V

### 第三步：等待安装

- 终端会开始下载安装，可能需要 1-3 分钟
- 看到类似 `added xxx packages` 的字样就是装好了
- 中间如果提示输入密码，就输入你的 Mac 登录密码（输入时屏幕不显示字符，正常现象）

### 第四步：验证安装成功

```bash
openclaw --version
```

看到版本号（如 `OpenClaw 2026.4.15`）就说明装好了 ✅

---

## 3. 启动 OpenClaw 并注册账号

### 第一步：启动网关

在终端运行：

```bash
openclaw gateway run
```

### 第二步：看到类似这样的输出

```
🦞 OpenClaw 2026.4.15
Gateway running at http://localhost:18789
```

**保持这个窗口开着！** 关闭窗口 Gateway 就停了。

### 第三步：用浏览器打开控制台

1. 打开 Chrome 或 Safari
2. 地址栏输入：

```
http://localhost:18789
```

3. 第一次打开会让你注册账号、设置密码
4. 按提示完成注册

---

## 4. 配置 QQBot（接收 QQ 消息）

### 前提：需要有一个 QQ 开放平台的开发者账号

如果你没有，需要先到这里申请：
**https://q.qq.com**

申请步骤比较复杂（需要审核），如果没有可以先跳过这步，用网页版和控制台先玩起来。

### 如果你已经有了 QQ 开放平台的 AppID 和 Token：

#### 第一步：安装 QQBot 插件

打开终端，运行：

```bash
openclaw plugins install qqbot
```

#### 第二步：配置 AppID

```bash
openclaw config set plugins.entries.qqbot.config.appId 你的AppID
```

#### 第三步：配置 Token

```bash
openclaw config set plugins.entries.qqbot.config.token 你的Token
```

#### 第四步：重启网关

```bash
openclaw gateway restart
```

#### 第五步：在 QQ 开放平台配置回调地址

在 QQ 开放平台的机器人配置页面，填入：

```
https://你的公网域名/callback/qqbot
```

（域名部分需要先有公网访问能力，新手建议先跳过这个，用网页版即可）

---

## 5. 配置 Web 控制台访问（bind 设置）

### 什么是 bind？

`bind` 决定了谁能访问 OpenClaw 控制台：

| bind 值 | 谁能访问 |
|---------|---------|
| `local` | 只有安装 OpenClaw 的这台电脑能访问 |
| `lan` | 同一个局域网内的所有设备都能访问 ✅ |
| `tailnet` | 通过 Tailscale VPN 访问（需要额外配置）|

### 目标：让局域网其他设备也能访问

#### 第一步：查看当前 bind 模式

打开终端，运行：

```bash
openclaw config get gateway.bind
```

如果显示 `local`，需要改成 `lan`

#### 第二步：修改 bind 为 lan

```bash
openclaw config set gateway.bind lan
```

#### 第三步：重启网关

```bash
openclaw gateway restart
```

#### 第四步：找到你电脑的局域网 IP

```bash
openclaw gateway status
```

在输出里找类似这样的地址：

```
Dashboard: http://192.168.1.112:18789/
```

`192.168.1.112` 就是你这台电脑的局域网 IP

#### 第五步：从另一台设备访问

**在同一局域网的其他电脑/手机上：**

打开浏览器，地址栏输入：

```
http://192.168.1.112:18789
```

把 `192.168.1.112` 换成你上一步查到的 IP

#### 如果浏览器报错：`control ui requires device identity`

这是浏览器的安全限制，用** SSH 隧道**方法解决（见下方）。

---

## SSH 隧道方法（解决浏览器安全限制）

### 适用场景

从局域网另一台电脑（如 192.168.1.109）访问 Mac 上的 OpenClaw 时，浏览器报错"control ui requires device identity"

### 原理

SSH 隧道把远程端口映射到本地 localhost，绕过浏览器安全限制

### 操作步骤

#### 在远程电脑（192.168.1.109）上打开终端，运行：

```bash
ssh -L 18789:localhost:18789 omi@192.168.1.112
```

把 `omi` 换成你 Mac 的用户名，`192.168.1.112` 换成 Mac 的 IP 地址

#### 按回车后，会提示输入密码

输入你的 Mac 登录密码（输入时屏幕不显示字符，正常）

#### 登录成功后，浏览器地址栏输入：

```
http://localhost:18789
```

就能正常访问了 ✅

---

## 6. 常见问题

### Q1：终端提示"Permission denied"

运行命令时加 `sudo`：

```bash
sudo npm install -g openclaw
```

### Q2：openclaw gateway run 报错"port already in use"

18789 端口被其他程序占用了，换一个端口：

```bash
openclaw config set gateway.port 19898
openclaw gateway restart
```

### Q3：重启后 bind 又变回 local 了？

每次重启 gateway 会重新读取配置。如果发现变了，确认你没有误操作 `openclaw config set gateway.bind local`

### Q4：QQBot 收不到消息？

1. 确认 gateway 正在运行（终端没有关闭）
2. 确认 QQBot 插件已安装：`openclaw plugins list`
3. 确认 AppID 和 Token 正确
4. 重启 gateway：`openclaw gateway restart`

### Q5：如何更新 OpenClaw 到最新版？

```bash
npm update -g openclaw
openclaw gateway restart
```

---

## 下一步（可选）

安装完成后，推荐继续配置这些：

| 任务 | 作用 | 难度 |
|------|------|------|
| 配置 Tavily API Key | 开启联网搜索能力 | ⭐ |
| 安装更多 Skill | 扩展 AI 能力 | ⭐ |
| 配置 GitHub 备份 | 自动备份工作文件 | ⭐⭐ |

---

*本指南最后更新：2026-04-18*
