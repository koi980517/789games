# 789games · 次日返水活动（Daily Cashback）

玩家前一天在 Slot / Casino / Arcade / Poker / Fishing / Bingo 的有效投注，次日按比例返还为 Cashback。普通玩家按档位（T1–T10），VIP 固定比例，另有 Selected Games 组（后台可开关）。

## 地址
| 资料 | 链接 |
|---|---|
| **在线原型 v1.4（对外可访问）** | https://koi980517.github.io/789games/daily-cashback/ |
| PRD v1.4（Claude Doc） | https://claude.ai/artifact/526VHHDfeci3Nkq8GicCcP |
| PRD 正文（Markdown 副本） | [docs/PRD.md](docs/PRD.md) |
| 原型画布（设计稿，内部） | https://claude.ai/artifact/2aWDMpb9urK3BLnwaYkJrV |
| Jira | [GAM-589](https://jira.bbops.ph/browse/GAM-589) |
| Wiki | [Wiki 页面](https://wiki.bbops.ph/pages/viewpage.action?pageId=49578533) |

## 在线原型说明（index.html，单文件，无外部依赖）
- 顶部切换「前台 H5 / APP」与「运营后台」。
- 首页按现网 QA 首页结构；打开 APP：活动弹窗（整图）→ 活动奖励弹窗；首页右侧独立挂件「1.5%+2%」；首页 Banner 首张 SLOTS CASHBACK（视觉参考返水充返转盘 PRD 3.0）。
- 图片素材在 assets/：banner.webp（首页 Banner）、popup.webp（活动弹窗）、model.webp（奖励弹窗人物）、gift.webp（挂件）。
- 前台：左侧切换身份（普通玩家 / VIP / 新玩家）与领取方式（手动 / 自动）；可演示开屏弹窗 → 领取弹窗、活动页 Today / Yesterday、Selected Games、Category 档位进度、Cashback History（单笔 / 一键领取）、规则页。
- 后台（v1.3，参考返水充返转盘 PRD 3.0）：页签 活动列表（第一个，点「编辑」进活动配置）/ 活动配置 / 费用配置 / 返点核对 / 返水发放 / Push · 短信 / 返水记录 / 活动统计 / 操作日志。活动配置为单页编号区块（① 基本信息 ② Category ③ Selected Games ④ 返水等级 ⑤ 手动指定档位 ⑥ 页面素材 ⑦ 活动规则页）+ 右侧前台实时预览，底部「提交发布」需谷歌验证码（原型 000000）。
- Selected Games：后台整体开关；每组选类型，再从该类型下勾选游戏，比例须高于该类型普通最高档；关闭后组内游戏按所属 Category 计算。Category：后台可设前台显示 / 隐藏，每个分类可启用 / 停用。
- 金额：当日返水向下取整到 ₱1（₱123.99 → ₱123），低于 ₱1 不发放；前台不显示领取时间 / 倒计时（写在规则页）；活动页无顶部 Banner。
- 后台「Category」可新增 / 改名 / 排序 / 删除分类，并从游戏库给每个分类加游戏（一个游戏只属于一个分类）；「返水等级」「Selected Games」修改后，前台同页即时更新；校验 >1% 蓝色、>5% 不可发布、门槛递增、比例逐档不降。
- Bet Bonus（活动 2，v1.4）：后台「⑦ 活动 2 · Bet Bonus」分「档位配置」「发放与流水」两块；参与活动游戏整个活动统一一组（已选择 N 个厂商 / M 个游戏），只有勾选游戏的有效投注计入本活动和奖励流水；档位表 投注额 ≥ / 返 / 删除；计算方式单选（默认不累加）；结算置灰；试算随配置即时重算。
- 数据均为示例，刷新页面即恢复默认。

## 变更记录
| 日期 | 变更 |
|---|---|
| 2026-11-18 | v1.4 同日补充：后台「Push · 短信」移到二期制作，页签标「二期」，页面置灰仅作二期设计参考；一期结算后不发送 Push / 短信 |
| 2026-11-18 | v1.4：后台 Bet Bonus「档位配置」改版（参考每日投注奖后台）：参与活动游戏从逐档配置改为整个活动统一配置（按钮 + 已选择 N 个厂商 / M 个游戏）；档位表改为 投注额 ≥ / 返 / 删除；计算方式改为单选；结算置灰展示；新增试算；前台 Daily Bet Bonus 有效投注只统计参与活动游戏 |
| 2026-11-18 | v1.3：后台按返水充返转盘 PRD 3.0 改版（页签、编号区块、实时预览、提交发布、费用配置、操作日志）；Featured Picks → Selected Games（可开关，按类型配游戏）；Game Types → Category（可配置） |
| 2026-11-18 | v1.2：新增活动弹窗、活动奖励弹窗、独立挂件「1.5%+2%」；首页按 QA 现网重做；首页 Banner 换 SLOTS CASHBACK |
| 2026-11-18 | v1.1：返水向下取整到 ₱1、低于 ₱1 不发；领取时间移入规则页；活动页去掉顶部 Banner；后台返水分类与游戏可配置 |
| 2026-11-18 | 新增在线原型 index.html（按 PRD v1.0 生成，前台 + 后台） |
| 2026-11-18 | 任务迁入 789games 项目；PRD 转为 Claude Doc；建本目录 |
| 2026-10-03 | PRD v1.0 初稿 |
