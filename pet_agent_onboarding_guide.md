# 宠物药市场分析 Agent 完整操作手册

> 本手册面向需要使用 OpenClaw + LLM 进行宠物药市场调研和趋势分析的业务团队成员。通过本手册，你将了解如何从零开始搭建这套系统，并用它来生产专业的市场分析报告。

---

## 一、系统架构概览

```
┌─────────────────────────────────────────────────────┐
│                     用户（QQBot）                    │
└─────────────────────┬───────────────────────────────┘
                      │ 消息
                      ▼
┌─────────────────────────────────────────────────────┐
│         OpenClaw Agent (pet-macos)                  │
│  • 记忆系统 (MEMORY.md / daily memory)              │
│  • 身份配置 (IDENTITY.md / SOUL.md)                 │
│  • 工作规范 (AGENTS.md / TOOLS.md)                 │
└────────┬────────────────────────────────────────────┘
         │
         ├── Tavily Search ──► 行业新闻/报告搜索
         ├── Web-Access (CDP) ──► 需要JS渲染的页面
         ├── MiniMax MCP ──► 图片理解/搜索
         └── MiniMax Multimodal ──► 语音/视频/图片生成
```

**核心能力：**
- 联网搜索（ Tavily + Chrome CDP）
- 社交媒体内容获取（微信/小红书/抖音）
- 图片理解（PDF/截图/图表分析）
- 专业报告生成（PDF/HTML）
- 持久记忆（跨会话积累知识）

---

## 二、Agent 配置（新建 OpenClaw 实例）

### 2.1 安装 OpenClaw

```bash
# macOS/Linux
npm install -g openclaw

# 启动网关
openclaw gateway run

# 查看状态
openclaw gateway status
```

### 2.2 初始化 Agent

```bash
# 创建新 agent（pet-macos 为示例名称）
openclaw agents create pet-macos

# 切换到该 agent
openclaw agents use pet-macos
```

### 2.3 连接 QQBot（消息通道）

参考：[OpenClaw QQBot 配置文档](https://docs.openclaw.ai)

```bash
# 安装 QQBot 插件
openclaw plugins install qqbot

# 配置 QQBot（获取 AppID 和 Token）
openclaw config set plugins.entries.qqbot.config.appId YOUR_APP_ID
openclaw config set plugins.entries.qqbot.config.token YOUR_TOKEN
```

### 2.4 基础配置文件（必需）

在 workspace 根目录创建以下文件：

| 文件 | 作用 | 说明 |
|------|------|------|
| `IDENTITY.md` | Agent 身份定义 | 名称、能力、角色定位 |
| `SOUL.md` | Agent 风格定义 | 回复语气、行为准则 |
| `USER.md` | 用户信息 | 了解你在帮助谁 |
| `AGENTS.md` | 工作规范 | 会话启动流程、记忆规范 |
| `TOOLS.md` | 工具笔记 | 本地环境配置、快捷指令 |
| `MEMORY.md` | 长期记忆 | 项目状态、关键决策、教训 |
| `HEARTBEAT.md` | 心跳任务 | 定期检查清单（邮件/日历等） |

---

## 三、Skill 安装（核心能力扩展）

### 3.1 安装来源

**方式 A：从 ClawHub 安装（推荐）**
```bash
clawhub install web-access
clawhub install openclaw-tavily-search
clawhub install minimax-mcp-call
clawhub install minimax-multimodal
clawhub install memory-setup
```

**方式 B：直接从 GitHub 共享目录安装**

本项目的共享 skill 目录已上传至 GitHub：
```
https://github.com/zhaoomi-zyw/openclaw-workspace-pet-macos/tree/main/skills-for-share
```

### 3.2 核心 Skill 说明

| Skill | 用途 | 安装命令 |
|-------|------|---------|
| `web-access` | 所有联网操作的必由之路，支持 CDP 浏览器自动化 | `clawhub install web-access` |
| `openclaw-tavily-search` | Tavily 搜索，Token 消耗低，适合新闻/报告搜索 | `clawhub install openclaw-tavily-search` |
| `minimax-mcp-call` | MiniMax MCP 工具集，包含搜索和图片理解 | 参考 MCP 配置 |
| `minimax-multimodal` | 多模态生成：语音/音乐/视频/图片 | `clawhub install minimax-multimodal` |
| `memory-setup` | 记忆系统配置指南 | `clawhub install memory-setup` |
| `self-improving-agent` | 记录错误和教训，持续自我改进 | 随 OpenClaw 内置 |

### 3.3 Tavily API Key 配置

1. 注册 [tavily.com](https://tavily.com)（开发版免费）
2. 获取 API Key
3. 配置到 `~/.openclaw/.env`：

```bash
echo 'TAVILY_API_KEY=tvly-your-key-here' >> ~/.openclaw/.env
```

4. 验证是否生效：
```bash
source ~/.openclaw/.env
curl -X POST "https://api.tavily.com/search" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{"query":"test","max_results":1}'
```

---

## 四、记忆系统（Memory）

### 4.1 为什么需要记忆

OpenClaw 每个会话都是"全新醒来"的，文件是你唯一的记忆载体。养成写文件的习惯 = 养成永久记忆。

### 4.2 长期记忆：MEMORY.md

核心内容包括：

```markdown
## 当前进行中项目
- [项目名] — [状态] — [最后进展日期]
  - 关键背景和结论

## 关键决策记录
- [日期] [决策内容] — 原因：[...]
  后续影响：[...]

## 用户偏好
- [偏好描述] — 场景：[...]
```

### 4.3 每日日志：memory/YYYY-MM-DD.md

每个会话结束后或每天创建，记录：
- 完成了什么
- 遇到了什么问题
- 教训/错误

**状态标签：**
- `[已完成]` 任务已完成
- `[进行中]` 任务未完成，需延续
- `[待确认]` 等待用户回复/外部结果

### 4.4 会话结束检查清单

每次结束会话前确认：
- [ ] 今天的任务完成了吗？ → 未完成的写入 daily memory
- [ ] 有新结论/决策吗？ → 有则写入 MEMORY.md
- [ ] 有教训/错误吗？ → 有则写入 MEMORY.md
- [ ] 用户有明确偏好/要求吗？ → 有则写入 USER.md
- [ ] commit + git push

---

## 五、网络搜索工作流（必读规范）

信息来源优先级：**Tavily → CDP → 放弃/替代**

| 情况 | 工具 | 原因 |
|------|------|------|
| **Tavily 搜得到的信息** | ✅ Tavily | 返回摘要snippet，Token 消耗低，速度快 |
| **Tavily 搜不到、但页面里有** | ✅ CDP（web-access） | 必须用浏览器打开才能看到 JS 渲染后的内容 |
| **Tavily 搜不到、页面也进不去** | ❌ 放弃或找替代源 | 如需登录的小红书帖子详情，直接放弃 |

### 典型场景判断：

- 查新闻/行业报告 → **Tavily**
- 官网是 JS 渲染 → **CDP（web-access）**
- 小红书/抖音详情页 → **放弃**（Tavily 搜摘要即可）
- 需要登录的个人内容 → **放弃**
- 微博/贴吧公开内容 → **Tavily**（通常有搜索索引）

---

## 六、生产宠物药市场分析报告（完整流程）

### 6.1 竞品研究流程

**Step 1：确定研究目标**
- 确定目标品牌（如：勃林格殷格翰宠物药）
- 确定竞争对手（如：硕腾 Zoetis、礼蓝 Elanco、海正动保）

**Step 2：Tavily 搜索基础信息**
```
搜索：勃林格殷格翰宠物药产品线 2025
搜索：硕腾 Zoetis 中国宠物药 2025
搜索：宠物驱虫药中国市场份额 2025
```

**Step 3：CDP 抓取详细页面**
- 品牌官网产品页
- 行业报告发布页
- 新闻媒体专题页

**Step 4：分析整合**
- 产品线对比（价格/适应证/剂型/用法）
- 竞争格局分析（SWOT）
- 市场策略分析（DTC/医院渠道/电商）

**Step 5：生成 PDF 报告**
```python
# 使用 Playwright 生成 HTML → PDF
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///path/to/report.html")
    page.pdf(path="output.pdf", format="A4")
    browser.close()
```

### 6.2 常用搜索关键词（宠物药方向）

| 类型 | 关键词示例 |
|------|---------|
| 产品线 | 勃林格殷格翰 宠物药 产品线 / Zoetis 大宠爱 欣宠克 |
| 市场格局 | 中国宠物药 市场占有率 / 宠物驱虫药 市场份额 |
| 竞争对手 | 硕腾 Zoetis 中国 / 礼蓝 Elanco 宠物 / 海正动保 |
| 动态新闻 | 宠物药 新品上市 / 动保 收购 合并 |
| 电商数据 | 宠物驱虫药 京东销量 / 宠物药 天猫排行榜 |
| 学术文献 | 宠物寄生虫 流行病学 / 心丝虫 预防 中国 |

### 6.3 报告风格（深绿色主题参考）

| 元素 | 颜色 |
|------|------|
| 主标题 | `#1a3d1a` 深墨绿 |
| 副标题/表头 | `#2d5a2d` 中深绿 |
| 页面背景 | `#f5f5f0` 米白 |
| 表格斑马纹 | `#c8e6c9` 薄荷绿 |
| 引用块背景 | `#e8f5e9` 浅绿 |

---

## 七、GitHub 同步（代码和报告备份）

### 7.1 初始化仓库

```bash
cd /Users/omi/.openclaw/workspace-pet-macos
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/zhaoomi-zyw/openclaw-workspace-pet-macos.git
git push -u origin main
```

### 7.2 每次变更后同步

```bash
git add .
git commit -m "[描述] 完成XXX报告 / 更新MEMORY"
git push
```

**注意：** 仓库建议设为 Private，避免敏感信息泄露。

---

## 八、常见问题处理

### Q1：Tavily 搜索返回 Unauthorized
- API Key 过期或无效
- 解决：到 tavily.com 重新获取 key，更新 `~/.openclaw/.env`

### Q2：SSH 隧道访问 OpenClaw 控制台报错
- 错误：`control ui requires device identity (use HTTPS or localhost secure context)`
- 原因：浏览器安全策略禁止局域网 IP 的不安全上下文
- 解决：在远程电脑执行 `ssh -L 18789:localhost:18789 omi@192.168.1.112`，然后访问 `http://localhost:18789`

### Q3：OpenClaw 节点连接不上
- 错误：`pairing required`
- 解决：在 Mac 上运行 `openclaw devices approve --latest`

### Q4：PDF 颜色/字体没生效
- 原因：Google Fonts 在 PDF 转换环境无法加载
- 解决：使用内嵌样式表，避免外部字体依赖

---

## 九、快速启动检查清单

- [ ] OpenClaw 安装完成，`openclaw gateway status` 运行正常
- [ ] QQBot 已配置，能接收消息
- [ ] 7个基础 MD 文件已创建（IDENTITY/SOUL/USER/AGENTS/TOOLS/MEMORY/HEARTBEAT）
- [ ] 核心 Skill 已安装（web-access / tavily-search / minimax-mcp-call）
- [ ] Tavily API Key 已配置并验证
- [ ] GitHub 仓库已初始化
- [ ] 跑通第一次搜索测试

---

## 十、相关资源

- **OpenClaw 官方文档：** https://docs.openclaw.ai
- **ClawHub（技能市场）：** https://clawhub.ai
- **GitHub 仓库：** https://github.com/zhaoomi-zyw/openclaw-workspace-pet-macos
- **Tavily API：** https://tavily.com

---

*本手册最后更新：2026-04-18*
