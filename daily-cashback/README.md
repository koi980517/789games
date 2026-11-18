# 789games · 次日返水活动（Daily Cashback）

玩家前一天在 Slot / Casino / Arcade / Poker / Fishing / Bingo 的有效投注，次日按比例返还为 Cashback。普通玩家按档位（T1–T10），VIP 固定比例，另有精选组（Featured Group）。

## 地址
| 资料 | 链接 |
|---|---|
| **在线原型 v1.0（对外可访问）** | https://koi980517.github.io/789games/daily-cashback/ |
| PRD v1.0（Claude Doc） | https://claude.ai/artifact/526VHHDfeci3Nkq8GicCcP |
| PRD 正文（Markdown 副本） | [docs/PRD.md](docs/PRD.md) |
| 原型画布（设计稿，内部） | https://claude.ai/artifact/2aWDMpb9urK3BLnwaYkJrV |
| Jira / Wiki | 未建 |

## 在线原型说明（index.html，单文件，无外部依赖）
- 顶部切换「前台 H5 / APP」与「运营后台」。
- 前台：左侧切换身份（普通玩家 / VIP / 新玩家）与领取方式（手动 / 自动）；可演示开屏弹窗 → 领取弹窗、活动页 Today / Yesterday、Featured Picks、Game Types 档位进度、Cashback History（单笔 / 一键领取）、规则页。
- 后台：活动列表、活动基础设置（基础设置 / 返水等级 / 精选游戏 / 分类与厂商）、手动指定档位、规则页、页面素材、返点核对、返水发放与封控、Push · 短信、返水记录、数据统计。
- 后台「返水等级」「精选游戏」修改后，前台同页即时更新；校验 >1% 蓝色、>5% 不可发布、门槛递增、比例逐档不降。
- 数据均为示例，刷新页面即恢复默认。

## 变更记录
| 日期 | 变更 |
|---|---|
| 2026-11-18 | 新增在线原型 index.html（按 PRD v1.0 生成，前台 + 后台） |
| 2026-11-18 | 任务迁入 789games 项目；PRD 转为 Claude Doc；建本目录 |
| 2026-10-03 | PRD v1.0 初稿 |
