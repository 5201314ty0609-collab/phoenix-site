# PHOENIX Changelog

## v1.1.0 — 2026-06-06

### 神经系统接通
- **SessionStart Hook**: 每次会话启动自动注入 PHOENIX 身份 + 上次会话记忆
- **Stop Hook**: 会话结束自动写日记、更新 last-session.json、同步 macOS Notes（一天一条追加模式）
- **Stop-hook Guard**: 防无限循环保护

### 多 Agent 编排升级
吸收自 GitHub 社区高星项目：
- `disler/claude-code-hooks-multi-agent-observability` ⭐1445 — Stop-hook guard 模式
- `Dicklesworthstone/claude_code_agent_farm` ⭐841 — Heartbeat 监测 + 自适应时间 + Context 预清理
- `hesreallyhim/a-list-of-claude-code-agents` ⭐1289 — Prompt-as-Code 协调模式

### 新增功能
- **Heartbeat 心跳监测**: 子 Agent 写心跳文件，>2min 无更新判定为卡死
- **自适应时间策略**: 并行启动 stagger 根据成功/失败自适应调整
- **Context 预清理**: ≤20% 时主动 compact

### 记忆系统升级
- 建立记忆筛选原则（保留标准 + 隔离标准 + 新增前自问）
- 归档低价值记忆 2 条，精简核心记忆 2 条
- 核心记忆从 5 条 263 行 → 4 条 173 行，减负 35%

### O2 增强
- 新增 heartbeat 监测
- 新增 ≤20% proactive clear 阈值

---

## v1.0.0 — 2026-06-05

### 诞生
- 融合 ECC + MUNDO + Metacog + Claude Soul + Autoresearch
- 七感监测系统上线
- 四阶段框架生命周期
- Karpathy 自愈引擎
- 七级强制执行层级
- 记忆系统建立
- 网站 phoenix-harness.netlify.app 上线
- macOS 桌面启动器 PHOENIX.app
