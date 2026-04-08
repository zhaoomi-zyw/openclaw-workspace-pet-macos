# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### Browser
- **ALWAYS use Chrome by default**: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` (v136)
- Always `agent-browser close` first before switching executables
- Or set env: `export AGENT_BROWSER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`

## 网络搜索工作流（必读）

信息来源优先级：**Tavily → CDP → 放弃/替代**

| 情况 | 用什么 | 原因 |
|------|--------|------|
| **Tavily 搜得到的信息** | ✅ **Tavily** | 返回摘要snippet，Token消耗低，速度快 |
| **Tavily 搜不到、但页面里有** | ✅ **CDP**（agent-browser/web-access） | 必须用浏览器打开才能看到JS渲染后的内容 |
| **Tavily搜不到、页面也进不去** | ❌ **放弃或找替代源** | 如需登录的小红书帖子详情，直接放弃 |

**典型场景判断：**
- 查新闻/行业报告 → Tavily
- 官网是JS渲染 → CDP
- 小红书/抖音详情页 → 放弃（Tavily搜摘要即可）
- 需要登录的个人内容 → 放弃
- 微博/贴吧公开内容 → Tavily（通常有搜索索引）

---

Add whatever helps you do your job. This is your cheat sheet.
