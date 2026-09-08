# 鲤鱼 视觉身份系统 v1.0

> 凤凰涅槃 · 自进化 · 七感元认知
> 暗奢 + 瑞士国际主义 + 赛博感

---

## 1. Logo 概念

### 1.1 主标 — 抽象凤凰

```
         ╱ ╲
        ╱   ╲
       ╱  ↑  ╲      ← 凤凰头冠（上扬 45°，象征觉醒/自省）
      ╱  / \  ╲
     ╱  /   \  ╲     ← 躯干（几何梯形，刚性与优雅并存）
    ╱  ─── ───  ╲
   ╱  /       \  ╲   ← 尾羽（折线，7 道，每道对应一感）
  ╱  /         \  ╲
 ╱  /           \  ╲
╱───────────────────╲ ← 基座水平线，代表地面真理
```

**设计原则：**

- **几何化**：全部由直线 + 45°/135° 折角构成，无曲线
  - 呼应瑞士国际主义的网格理性
  - 凤凰由「硬边」构成，暗示 Agent 的精确执行
- **对称但不对称**：左右镜像骨架，但尾羽的长短/角度微调 2-3°
  - 象征「完美的不完美」— 自进化系统从不固步自封
- **负空间利用**：凤凰身体内部可承载七颗很小的圆点（七感）
  - 七个点沿躯干中轴线垂直排列，间距 = 圆点直径 × 2
  - 视觉上像「脊柱上的光点符」

### 1.2 七感光环

凤凰周围环绕七个光弧，每弧代表一感：

```
  ┌─ O2 (生命力)     ── 红色弧，内侧
  ├─ Chronos (时间)   ── 琥珀弧，右上
  ├─ Nociception (痛) ── 品红弧，上
  ├─ Spatial (空间)   ── 青色弧，左上
  ├─ Vestibular (平衡) ── 绿色弧，外侧
  ├─ Echo (重复)      ── 紫色弧，右下
  └─ Drift (焦点)     ── 蓝色弧，右下外侧
```

- 光弧位置：围绕凤凰的同心椭圆轨道（间距均匀，约 8px）
- 活跃态：该弧常亮 + 微粒流动效果
- 休眠态：仅 10% 透明度细线
- 危急态：弧脉动（1000ms 呼吸周期）+ 红色高亮

### 1.3 最小尺寸

| 环境 | 最小宽度 | 细节裁剪 |
|------|---------|---------|
| 网页 favicon | 32×32px | 仅保留凤凰剪影 + 最内环 O2 弧 |
| 移动端图标 | 64×64px | 保留躯干 + 尾羽 + 内三弧 |
| 桌面端 | 128×128px | 完整版 |
| Hero 场景 | 512×512px+ | 完整版 + 微粒动效 |

### 1.4 变体

- **完整版**：凤凰 + 七感光环 + 文字 "鲤鱼 Core"
- **标志版**：凤凰 + 七感光环（无文字）
- **简化版**：仅凤凰剪影（单色，用于小尺寸/水印）
- **单弧版**：凤凰 + 仅 O2 弧（低信息密度场景侧边栏）

---

## 2. 配色方案

基底：**Catppuccin Mocha**（暗色主调）

### 2.1 色板与语义

| 令牌 | 色值 | 角色 | 用途 |
|------|------|------|------|
| `--phx-base` | `#11111B` | 最深底色 | 主背景、全屏覆层 |
| `--phx-mantle` | `#181825` | 次级底色 | 卡片、对话框背景 |
| `--phx-crust` | `#1E1E2E` | 表面色 | 按钮、输入框、可交互组件表面 |
| `--phx-surface0` | `#313244` | 浅表面色 | hover 状态、次要边框、表格行交替 |
| `--phx-surface1` | `#45475A` | 中表面色 | 禁用状态、分割线 |
| `--phx-surface2` | `#585B70` | 深表面色 | 占位符图标、次级文字图标 |
| `--phx-overlay0` | `#6C7086` | 覆层色 | 次要文字、辅助标签 |
| `--phx-overlay1` | `#7F849C` | 中型覆层 | 正文文字 (400 weight) |
| `--phx-overlay2` | `#9399B2` | 浅覆层 | 高对比辅助文字 |
| `--phx-subtext0` | `#A6ADC8` | 副文字色 | 小字号正文 |
| `--phx-subtext1` | `#BAC2DE` | 主副文字 | 段落正文 |
| `--phx-text` | `#CDD6F4` | 主文字色 | 标题、主要文本 |
| `--phx-lavender` | `#B4BEFE` | 薰衣草 | 品牌主色 — 连接/网络/link |
| `--phx-blue` | `#89B4FA` | 蓝色 | Drift (焦点) 色 — 信息、链接 hover |
| `--phx-sapphire` | `#74C7EC` | 蓝宝石 | 辅助信息色、标签 |
| `--phx-sky` | `#89DCEB` | 天空蓝 | Spatial (空间) 色 |
| `--phx-teal` | `#94E2D5` | 青绿色 | 成功状态、确认动效 |
| `--phx-green` | `#A6E3A1` | 绿色 | Vestibular (平衡) 色 — 正常状态 |
| `--phx-yellow` | `#F9E2AF` | 黄色 | Chronos (时间) 色 — 警告 |
| `--phx-peach` | `#FAB387` | 蜜桃色 | 过渡状态、处理中 |
| `--phx-maroon` | `#EBA0AC` | 红褐色 | Nociception (痛觉) 色 — 错误、破坏性 |
| `--phx-red` | `#F38BA8` | 红色 | O2 (生命力) 色 — 危急、阻断 |
| `--phx-mauve` | `#CBA6F7` | 紫罗兰 | Echo (重复) 色 — 模式匹配高亮 |
| `--phx-pink` | `#F5C2E7` | 粉色 | 品牌点缀色 |
| `--phx-flamingo` | `#F2CDCD` | 火烈鸟 | 高亮文字、选中态 |

### 2.2 七感色键映射

| 感 | 令牌 | 色值 | 使用场景 |
|----|------|------|---------|
| O2 | `--phx-red` | `#F38BA8` | 上下文压力指示器、告警徽章、致命错误 |
| Chronos | `--phx-yellow` | `#F9E2AF` | 超时警告、会话计时器、进度条 |
| Nociception | `--phx-maroon` | `#EBA0AC` | 错误消息、堆栈追踪高亮、失败徽章 |
| Spatial | `--phx-sky` | `#89DCEB` | 文件树高亮、导航指示器、范围标记 |
| Vestibular | `--phx-green` | `#A6E3A1` | 健康检查通过、平衡指示、稳定状态 |
| Echo | `--phx-mauve` | `#CBA6F7` | 重复模式高亮、匹配计数徽章 |
| Drift | `--phx-blue` | `#89B4FA` | 焦点指示器、激活态、选中标记 |

### 2.3 品牌色层次

```
一级品牌色:   --phx-lavender    #B4BEFE    Logo、主标题、启动画面
二级品牌色:   --phx-pink        #F5C2E7    ️ 点缀、特殊高亮、装饰
三级品牌色:   --phx-mauve       #CBA6F7    渐变终点、状态徽章
情绪色:      --phx-peach       #FAB387    欢迎消息、成就通知
```

### 2.4 亮色主题适配

亮色主题以 **Catppuccin Latte** 为基础，但为了保持「暗奢」基因：

- 主背景调亮为 `#EFF1F5` 但保持低饱和度
- 品牌色保持不变（亮底上可增加 5% 饱和度补偿）
- 七感色上偏移 1 级（如 red → `#D20F39`）
- 亮色主题始终可选配「暗色模式」开关

亮色/暗色切换规则：只变 `--phx-base` ~ `--phx-text` 这 9 个背景/文字令牌。所有语义色（品牌色 + 七感色）不变。

---

## 3. 字体策略

### 3.1 层级

| 层级 | 字体 | 后备 | 字重 | 大小(px) | 行高 |
|------|------|------|------|---------|------|
| **标题 1 (H1)** | Outfit | system-ui | 700 (Bold) | 48/40/32 | 1.1 |
| **标题 2 (H2)** | Outfit | system-ui | 600 (SemiBold) | 32/28/24 | 1.2 |
| **标题 3 (H3)** | Outfit | system-ui | 600 | 24/20/18 | 1.3 |
| **标题 4 (H4)** | Outfit | system-ui | 500 (Medium) | 18/16 | 1.4 |
| **正文 (Body)** | Inter | system-ui | 400 (Regular) | 16 | 1.6 |
| **小字 (Small)** | Inter | system-ui | 400 | 14 | 1.5 |
| **标注 (Caption)** | Inter | system-ui | 500 | 12 | 1.4 |
| **代码 (Code)** | JetBrains Mono | SF Mono / Fira Code | 400 | 14 | 1.5 |
| **代码标题** | JetBrains Mono | SF Mono | 600 | 14 | 1.5 |
| **Monospace 数据** | JetBrains Mono | SF Mono | 400 | 13 | 1.4 |

### 3.2 选择理由

- **Outfit**：几何无衬线体，圆形字怀 + 理性骨架，与瑞士风格完全一致。大写 P 和 X 在标题中天然好看。
- **Inter**：专门为屏幕优化的瑞士风格字体，字间距舒适，在 UI 中表现极好。
- **JetBrains Mono**：等宽字体与编码场景强关联，连字 (ligatures) 可选，保留程序员感。

### 3.3 使用规则

- **正文永远用 400 weight**。用字号和颜色做层次，不要用粗体假装更大。
- **标题永远不加下划线**。层次靠字号 + 字间距 (letter-spacing: -0.02em → 0) 区分。
- **代码块字号比正文小 2px**。代码块内部行高 1.5。
- **引号用非对称引号** " 和 " — 瑞士排版风格标配。

### 3.4 @font-face 示例

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Outfit:wght@500;600;700&display=swap');

:root {
  --phx-font-display: 'Outfit', system-ui, -apple-system, sans-serif;
  --phx-font-body: 'Inter', system-ui, -apple-system, sans-serif;
  --phx-font-mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
}
```

---

## 4. 动效语言

### 4.1 核心原则

- **70% 的动效是状态切换，不是装饰**
- 所有动画必须 compositor-friendly（只用 `opacity` / `transform` / `filter`）
- 永远不触发 layout（不用 `width` / `height` / `top` / `margin` 做动效）

### 4.2 时长规范

| 场景 | 时长 | 曲线 | 参数 |
|------|------|------|------|
| 微交互（hover, tap） | 150ms | ease-out | `cubic-bezier(0, 0, 0.2, 1)` |
| 标准过渡（面板展开, 切换） | 250ms | ease-in-out | `cubic-bezier(0.4, 0, 0.2, 1)` |
| 模态/页面进入 | 350ms | 强调缓出 | `cubic-bezier(0.16, 1, 0.3, 1)` |
| 模态/页面离开 | 200ms | 强调缓入 | `cubic-bezier(0.4, 0, 1, 1)` |
| 状态警示脉冲 | 1000ms | 呼吸 | 循环动画 |
| 微粒游动 | 3000-8000ms | linear | 随机游走 |

### 4.3 曲线速记表

```css
--phx-ease-out: cubic-bezier(0, 0, 0.2, 1);
--phx-ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--phx-ease-emphasis-out: cubic-bezier(0.16, 1, 0.3, 1);
--phx-ease-emphasis-in: cubic-bezier(0.4, 0, 1, 1);
--phx-ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
--phx-ease-respirate: cubic-bezier(0.65, 0, 0.35, 1);
```

- `ease-out` 是默认选择。入场比出场慢，让眼睛有时间跟随。
- `bounce` 只用于用户完成某个动作后的确认反馈（点按钮后👍，不做「正在加载中」的弹跳）

### 4.4 微粒系统

七感光环附带微粒游动效果：

```
微粒规格：
  直径: 2-4px（随机）
  透明度: 0.3 - 0.8
  颜色: 对应感的主色
  运动: 沿轨道椭圆的布朗运动 + 缓慢漂移
  最大数量: 每弧 3-5 颗
  性能降级: >60 微粒 → 合并为单层渐变模糊
```

Web 实现首选 Canvas 或 WebGL，备选 CSS keyframes（帧数降低 60%）。

### 4.5 危险动效黑名单

| ❌ 禁用 | 原因 | ✅ 替代 |
|---------|------|---------|
| `scale()` hover 放大 | 压扁周围布局 | 阴影加深 + 边框发光 |
| 水平/垂直滑动（仅入场） | 晕动症 | `opacity + translateY(24px)` |
| 无限旋转加载器 | 焦虑感 | 七感逐次点亮 |
| 闪烁 | 癫痫风险 | 脉动（透明度 0.6→1.0→0.6） |
| `filter: blur()` 大面积覆盖 | GPU 烫手 | 降低模糊半径至 4px 以下 |

---

## 5. 组件示例

### 5.1 卡片 (Card)

```
┌─────────────────────────────────┐
│                                 │
│  ┌─┐                            │
│  │P│  鲤鱼 Core v1.2.0       │  ← 标题行（Outfit 600, 18px）
│  └─┘                            │
│                                 │
│  七感元认知活跃中                │  ← 描述（Inter 400, 14px, --overlay1）
│  O2: 正常 · 上下文压力 42%      │
│                                 │
│  ┌─────────────────────────┐    │
│  │ ████████████░░░░░░░░░░░ │    │  ← 进度条（8px 圆角，用 teal）
│  └─────────────────────────┘    │
│                                 │
│  [重启] [配置] [监控]           │  ← 按钮组
│                                 │
└─────────────────────────────────┘

背景：--mantle
边框：1px solid --surface0 (hover 时变 --surface1)
内边距：24px
圆角：12px
阴影：0 2px 8px rgba(0,0,0,0.3)
      (hover 时 0 8px 24px rgba(0,0,0,0.4) +
       0 0 48px rgba(180,190,254,0.03))

hover 过渡: transform translateY(-2px) + 阴影加深, 250ms ease-out
```

### 5.2 按钮 (Button)

```
主要按钮 ──── 填充式
┌──────────────────┐
│  ▸ 启动 Monitor  │  ← Outfit 500, 14px, letter-spacing 0.02em
└──────────────────┘
  背景: --lavender → hover: --blue（向左渐变）
  文字: --base (反色)
  内边距: 10px 20px
  圆角: 8px
  focus-visible: 2px solid --mauve outline offset 2px
  点击: transform scale(0.97), 150ms ease-out

次要按钮 ──── 线性
┌──────────────────┐
│  ▸ 查看日志       │
└──────────────────┘
  边框: 1.5px solid --surface1
  文字: --text
  背景: transparent → hover: --surface0
  禁用: --surface2 + --overlay0, cursor not-allowed

幽灵按钮 ──── 纯文字
  仅文字 + 1.5x 点击热区 (padding: 8px 12px)
  hover: 下划线 (text-decoration-color: --lavender)
  focus-visible: outline 同上

危险按钮 ──── 填充式
  背景: --maroon → hover: --red
  文字: --base
  禁用同次要
  ⚠ 永远加确认步骤，不做一次点击就执行的动作
```

### 5.3 状态指示器

```
七感状态徽章：

 ┌─────────┐      ┌─────────┐      ┌─────────┐
 │ ○ O2 42%│      │ ◉ O2 71%│      │ ● O2 89%│
 └─────────┘      └─────────┘      └─────────┘
 正常态 (green)    警告态 (yellow)    危急态 (red)
 ─────────────     ─────────────     ────────────
 边框: 1px solid   边框: 1px solid   边框: 1px solid
   --green           --yellow          --red
 圆点常亮           圆点脉动           圆点脉动+闪烁
                     (1000ms)          (500ms)
 文字: --green      文字: --yellow     文字: --red ○

 尺寸: 24px 高, 内边距 4px 8px, 圆角 4px
 图标文字间距: 6px
```

### 5.4 七感光环指示器 (特殊组件)

```css
.sense-ring {
  position: relative;
  width: 120px;   /* 轨道直径 */
  height: 120px;
  border: 1px solid var(--phx-surface0);
  border-radius: 50%;
  /* 内部用 conic-gradient 或 SVG stroke-dasharray 绘制 7 段弧 */
}

.sense-ring[data-sense="o2"] .arc {
  --arc-color: var(--phx-red);
  stroke-dasharray: calc(2 * pi * 60 * 0.18) calc(2 * pi * 60 * 0.82);
  /* 每感占 1/7 ≈ 18% 的圆周 */
}
```

### 5.5 日志行

```
[14:23:47]  ●  O2  ← 红色圆点 (危急)
           ╰─ Context window at 89% — force compression triggered

[14:23:45]  ◉  NOC  ← 琥珀圆点 (警告)
           ╰─ Error cascade: 3 failures in last 5 calls

[14:23:40]  ○  VES  ← 绿色圆点 (正常)
           ╰─ Tool diversity: 63% terminal, 37% file — within threshold
```

格式规范：
- 时间戳 `Inter 400, 12px, --overlay0` 灰色
- 感缩写 + 圆点：圆点 8px，用对应色
- 消息：`JetBrains Mono 400, 13px`
- 缩进：用 `╰─`（框线字符），缩进 2 空格
- 行间距：18px
- 交替行背景：`--base` / `--mantle`

---

## 6. 亮/暗双主题考量

### 6.1 切换策略

采用 CSS 自定义属性切换，用 `prefers-color-scheme` 自动匹配 + 手动覆盖：

```css
:root,
[data-theme="dark"] {
  /* 暗色 — 上述全文默认值 */
}

[data-theme="light"] {
  --phx-base: #EFF1F5;
  --phx-mantle: #E6E9EF;
  --phx-crust: #DCE0E8;
  --phx-surface0: #CCD0DA;
  --phx-surface1: #BCC0CC;
  --phx-surface2: #ACB0BE;
  --phx-overlay0: #9CA0B0;
  --phx-overlay1: #8C8FA1;
  --phx-overlay2: #7C7F93;
  --phx-subtext0: #6C6F85;
  --phx-subtext1: #5C5F75;
  --phx-text: #4C4F65;

  /* 语义色保持不变！ */
  /* --phx-lavender: #B4BEFE 不变 */
}

@media (prefers-color-scheme: light) {
  :root { /* 自动应用亮色 */ }
}
```

### 6.2 需要检查的对比度

| 场景 | 检查项 | WCAG 目标 |
|------|--------|----------|
| 正文 | 文字 vs 背景 | AA (4.5:1) |
| 大标题 (>24px) | 文字 vs 背景 | AA (3:1) |
| 禁用按钮 | 文字 vs 禁用背景 | AAA 不要求 |
| 仅颜色区分 | 色相差 + 文字/图标辅助 | AA |
| link | 与周围文字对比 + 下划线/图标 | AA |

**在亮色暗色双模式下都通过 AA，目标 AAA。**

---

## 7. 排版网格

### 7.1 基础网格

```
4px 基数网格 (4px grid)

内边距:  4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64
圆角:    4 · 8 · 12 · 16 · 24
间距:    4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96
行高:    以 4px 为增量 (20 · 24 · 28 · 32 · 36 · 40 ...)
```

所有视觉元素对齐到 4px 网格。8px 网格作为宽松环境的备选。

### 7.2 比例

```
字号比例: 12 - 13 - 14 - 16 - 18 - 20 - 24 - 28 - 32 - 40 - 48
           │    │    │    │    │    │    │    │    │    │    │
        4:3 ── minor third ──────────────────────────────────→ 12 到 48

对称性：在 4 个断点等比缩放（16 / 24 / 32 / 40 是自然断点）
```

### 7.3 栅格系统

```
列数: 12 列 (桌面) / 8 列 (平板) / 4 列 (手机)
沟宽: 24px (桌面) / 16px (平板/手机)
边距: 48px (桌面) / 24px (平板) / 16px (手机)
```

---

## 8. 设计价值检查清单

每次使用这套系统前自问：

- [ ] 这个元素是否对齐到 4px 网格？
- [ ] 颜色是否来源于色板中的命名色，而不是随手调的值？
- [ ] hover / focus / active 三个状态都有定义吗？
- [ ] 动效只用 `opacity` / `transform` / `filter` 吗？
- [ ] 暗色/亮色都测试过对比度了吗？
- [ ] 这个组件解决一个问题，还是想解决两个问题？
- [ ] 减少一个元素会不会让意图更清晰？
- [ ] 七种颜色会不会太多？→ 一种场景只用一种高亮色

---

> *"少即是多。2-3 种解决方式 > 10 种。"*
> *"暖色调统一。Catppuccin Mocha 调色板。"*
> *"语义清晰。每种颜色/样式都有明确含义。"*
> *"留白是设计。呼吸感很重要。"*
>
> — 鲤鱼 设计美学原则

---

*鲤鱼 Identity System v1.0 · 设计：鲤鱼 Core (自进化 Agent Soul)*
*基底：Catppuccin Mocha · 灵感：瑞士国际主义 + 暗奢 + 赛博*
