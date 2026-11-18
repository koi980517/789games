# 789games · 次日返水活动（Daily Cashback）

玩家前一天在 Slot / Casino / Arcade / Poker / Fishing / Bingo 的有效投注，次日按比例返还为 Cashback。普通玩家按档位（T1–T10），VIP 固定比例，另有精选组（Featured Group）。

## 地址
| 资料 | 链接 |
|---|---|
| **在线原型 v1.2（对外可访问）** | https://koi980517.github.io/789games/daily-cashback/ |
| PRD v1.2（Claude Doc） | https://claude.ai/artifact/526VHHDfeci3Nkq8GicCcP |
| PRD 正文（Markdown 副本） | [docs/PRD.md](docs/PRD.md) |
| 原型画布（设计稿，内部） | https://claude.ai/artifact/2aWDMpb9urK3BLnwaYkJrV |
| Jira / Wiki | 未建 |

## 在线原型说明（index.html，单文件，无外部依赖）
- 顶部切换「前台 H5 / APP」与「运营后台」。
- 首页按现网 QA 首页结构；打开 APP：活动弹窗（整图）→ 活动奖励弹窗；首页右侧独立挂件「1.5%+2%」；首页 Banner 首张 SLOTS CASHBACK（视觉参考返水充返转盘 PRD 3.0）。
- 图片素材在 assets/：banner.webp（首页 Banner）、popup.webp（活动弹窗）、model.webp（奖励弹窗人物）、gift.webp（挂件）。
- 前台：左侧切换身份（普通玩家 / VIP / 新玩家）与领取方式（手动 / 自动）；可演示开屏弹窗 → 领取弹窗、活动页 Today / Yesterday、Featured Picks、Game Types 档位进度、Cashback History（单笔 / 一键领取）、规则页。
- 后台：活动列表、活动基础设置（基础设置 / 返水等级 / 精选游戏 / 返水分类与游戏）、手动指定档位、规则页、页面素材、返点核对、返水发放与封控、Push · 短信、返水记录、数据统计。
- 金额：当日返水向下取整到 ₱1（₱123.99 → ₱123），低于 ₱1 不发放；前台不显示领取时间 / 倒计时（写在规则页）；活动页无顶部 Banner。
- 后台「返水分类与游戏」可新增 / 改名 / 排序 / 删除分类，并从游戏库给每个分类加游戏（一个游戏只属于一个分类）；「返水等级」「精选游戏」修改后，前台同页即时更新；校验 >1% 蓝色、>5% 不可发布、门槛递增、比例逐档不降。
- 数据均为示例，刷新页面即恢复默认。

## 变更记录
| 日期 | 变更 |
|---|---|
| 2026-11-18 | v1.2：新增活动弹窗、活动奖励弹窗、独立挂件「1.5%+2%」；首页按 QA 现网重做；首页 Banner 换 SLOTS CASHBACK |
| 2026-11-18 | v1.1：返水向下取整到 ₱1、低于 ₱1 不发；领取时间移入规则页；活动页去掉顶部 Banner；后台返水分类与游戏可配置 |
| 2026-11-18 | 新增在线原型 index.html（按 PRD v1.0 生成，前台 + 后台） |
| 2026-11-18 | 任务迁入 789games 项目；PRD 转为 Claude Doc；建本目录 |
| 2026-10-03 | PRD v1.0 初稿 |
