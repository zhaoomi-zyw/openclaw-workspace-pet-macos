# Skills 共享目录

此目录包含可复用的 OpenClaw Skills，适合迁移到新 OpenClaw 环境。

## 目录结构

```
skills-for-share/
├── web-access/              # CDP 浏览器自动化（网页抓取/JS渲染页面）
├── memory-setup/            # 记忆系统配置
├── agent-browser-clawdbot/ # Agent 浏览器自动化
├── minimax-mcp-call/       # MiniMax MCP 工具（搜索+图片理解）
├── minimax-multimodal/     # MiniMax 多模态（语音/音乐/视频/图片生成）
├── openclaw-tavily-search/ # Tavily 网络搜索
└── self-improving-agent/   # 自我改进代理
```

## 安装方式

在新机器的 OpenClaw 中，将这些文件夹复制到 `~/.openclaw/skills/` 即可：

```bash
# 方式：将 skills-for-share 下的各 skill 复制到 ~/.openclaw/skills/
cp -r skills-for-share/web-access ~/.openclaw/skills/
cp -r skills-for-share/memory-setup ~/.openclaw/skills/
# ...以此类推
```

或者使用 OpenClaw 内置命令：
```bash
openclaw skills install https://clawhub.ai/<skill-url>
```

## 各 Skill 说明

| Skill | 用途 | 安装优先级 |
|-------|------|----------|
| **web-access** | CDP 浏览器自动化，适合抓取 JS 渲染页面 | ⭐⭐⭐⭐⭐ 必装 |
| **openclaw-tavily-search** | Tavily 搜索，快速获取网络摘要 | ⭐⭐⭐⭐⭐ 必装 |
| **memory-setup** | 配置长期记忆系统 | ⭐⭐⭐⭐ 建议 |
| **agent-browser-clawdbot** | 浏览器自动化基础工具 | ⭐⭐⭐⭐ 建议 |
| **minimax-mcp-call** | MiniMax 搜索+图片理解（需 API Key） | ⭐⭐⭐ 可选 |
| **minimax-multimodal** | 语音/音乐/视频/图片生成（需 API Key） | ⭐⭐⭐ 可选 |
| **self-improving-agent** | 自我学习和错误纠正 | ⭐⭐⭐ 建议（用clawhub安装） |

## ⚠️ 未包含的 Skills

- **`self-improving-agent/`** 未包含（本身是 git clone，含子模块，不适合直接打包）
  → 在目标机器使用 `clawhub install sundial-org/self-improving-agent` 安装

- **`last30days/`** 未包含（35MB，含 ML 模型，不适合 git 管理）
  → 在目标机器重新安装

## 安装检查清单

```bash
# 1. 克隆仓库
git clone https://github.com/zhaoomi-zyw/openclaw-workspace-pet-macos.git ~/.openclaw/workspace

# 2. 复制 skills
cp -r skills-for-share/web-access ~/.openclaw/skills/
cp -r skills-for-share/openclaw-tavily-search ~/.openclaw/skills/
cp -r skills-for-share/memory-setup ~/.openclaw/skills/
cp -r skills-for-share/agent-browser-clawdbot ~/.openclaw/skills/
cp -r skills-for-share/minimax-mcp-call ~/.openclaw/skills/

# 3. 安装 self-improving-agent（clawhub）
clawhub install sundial-org/self-improving-agent

# 4. 安装 minimax-multimodal（按需）
clawhub install minimax-multimodal
```

## Skills 配置注意事项

详见各 skill 目录下的 `SKILL.md` 文件。
