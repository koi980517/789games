# 789games · 玩家注册与登录调整（合规）

按合规条款「3. Player registration and login」调整：只能用手机号注册；注册时必须提供全名、出生日期、最近的游戏场所、政府签发证件；手机号和基本注册信息在账户页可见；Google / Facebook / Telegram 只做便捷登录，不能注册。

| 项 | 内容 |
|---|---|
| 状态 | v1.0 初稿，待评审 |
| 负责人 | Koi（产品） |
| 日期 | 2026-11-27 |
| 站点 | 789games（主站是否同步待确认） |
| Jira / Wiki | 待建 |

## 目录

| 路径 | 说明 |
|---|---|
| [docs/PRD.md](docs/PRD.md) | PRD v1.0：条款拆解、现状、规则、前台流程、后台配置、接口、验收、待确认、风险 |
| [registration-login-prototype-v1.0.html](registration-login-prototype-v1.0.html) | 可交互原型（玩家端 / 运营后台 / 改动对照） |

在线原型：https://koi980517.github.io/789games/registration-login/registration-login-prototype-v1.0.html

## 原型页面

| 编号 | 页面 |
|---|---|
| L1 | 登录 / 注册页（OTP / 密码 / 三方仅登录） |
| R1–R5 | OTP → 基本信息 → 证件 → 密码与确认 → 注册成功 |
| L2 | 三方未绑定提示（不建号） |
| L3 | 存量账号绑手机号 + 补全 |
| A1 | My Details · Registration Info |
| A2 | Account Security · Linked Accounts |
| 后台 | 用户详情注册信息、用户列表筛选、注册设置、游戏场所清单、补全统计 |

右侧「模拟场景」可切换：新用户注册、三方未绑定、已注册登录、存量三方无手机号、存量 KYC 已过缺场所、未满 21 岁。
