# 【789games】提现前须通过 KYC 身份核验 PRD v1.0

2026-11-27 · Koi

> 需求原文（第 5 条）：**KYC Verification Required Before Withdrawal | 提现前须通过 KYC 身份核验** —— Players must complete and pass KYC verification before they can withdraw funds. 玩家必须完成并通过 KYC 身份核验后，方可提现。

| 资料 | 链接 |
|---|---|
| 可交互原型 | https://koi980517.github.io/789games/789games-kyc-withdrawal-v1.0.html |
| PRD（本文件） | GitHub `kyc-withdrawal/PRD.md` |
| Wiki | PD › 2026-11 › 提现前须通过 KYC 身份核验（待建） |
| Jira | 故事单（待建）；子任务：后端 / 后台前端 / H5 / App / QA |
| 参考 | Jira 单共享知识库-产品侧（KYC 开关体系 -1213/-1460/PD/1158635、强制 KYC 触发点 -1343、3 天未 KYC 临时冻结 PD/1157182、提款前置 PD/1154492）；firebase-tracking-spec 5.4 / 5.6 |

---

## 1. 背景与范围

合规要求：玩家**完成并通过** KYC 后才能提现。现网已经在提现、绑卡时触发强制 KYC，但存在放行口子（「部分认证用户可提款」开关、审核中状态、仅前端拦截等），不能保证"未通过 KYC 的人一笔也提不出去"。本次把规则收紧为：**只有 KYC 状态 = 审核通过的玩家才能创建提现单，服务端兜底校验，出款前再校验一次。**

### 1.1 现状（As-Is，来自知识库，未在 QA 后台逐项复核）

| # | 现状 | 问题 / 影响 |
|---|---|---|
| P1 | 前台 KYC 状态 4 种：Unverified / Verified / Fully Verified / Rejected，另有审核中（-6306 提到"审核中重复弹窗"） | 「Verified（部分认证）」是否算"通过"没有统一口径 |
| P2 | 后台有「部分认证用户可提款」开关（PD/1158635） | 打开时未完整认证也能提现，与合规原文冲突 |
| P3 | 强制 KYC 在绑卡、提现时触发，弹窗不可关闭（-1343） | 主要是前端拦截；老包 / 直调接口是否被服务端拦截未确认 |
| P4 | 「3 天未 KYC 临时冻结」现在只在点提款时弹窗（PD/1157182） | 与 KYC 拦截弹窗可能叠加、文案不一致 |
| P5 | 已提交待审核的提现单，后台把 KYC 改为 Rejected 后仍可能出款 | 出款前没有二次校验 |
| P6 | KYC 供应商 Zoloz / Paddle 可切换；绿色通道（PAGCOR 手机号）自动通过；789games 继承老站 KYC（GAM-2） | 不同来源的"通过"状态要统一落到同一字段 |

### 1.2 包含 / 不包含

| 包含 | 不包含 |
|---|---|
| 提现入口、提现提交、绑定提款账户三处的 KYC 状态拦截（前端 + 服务端） | KYC 认证流程本身（证件、人脸、补充信息页面不改） |
| 出款前（审核通过 → 代付下单）KYC 二次校验 | 充值、游戏、红包、活动的 KYC 规则 |
| 不同 KYC 状态的拦截弹窗与英文文案 | KYC 供应商切换、NDRP 逻辑 |
| 后台：提现设置新增开关、提现审核列表加 KYC 状态列、拦截日志 | 存量已出款订单回溯 |
| 埋点 withdraw_block / kyc_prompt_view 补参数 | |

### 1.3 目标
1. 上线后，KYC 未通过的账号新建提现单数 = 0（服务端日志可查）。
2. 已提交但 KYC 后来被驳回的提现单，出款前 100% 被拦下转人工。
3. 被拦玩家 1 步即可进入 KYC / 查看审核进度，不出现"白屏 / 无提示"。

### 1.4 适用范围
- 站点：**仅 789games**（与主站共用后端，开关按站点 siteId 隔离；789bingo 是否同步见待确认 1）
- 币种 PHP；语言 English；端：H5 / Android / iOS（含 Flutter 包）/ PC
- 时间：GMT+8

---

## 2. 规则

### 2.1 放行判定

| KYC 状态（前台显示） | 后端状态 | 能否进入提现页 | 能否提交提现 | 能否绑定提款账户 | 拦截弹窗 |
|---|---|---|---|---|---|
| Unverified 未认证 | UNVERIFIED | 可进入，显示提示条 | ✗ | ✗ | K1 |
| Pending 审核中 | PENDING / MANUAL_REVIEW | 可进入，显示提示条 | ✗ | ✗ | K2 |
| Verified 部分认证 | PARTIAL | 可进入，显示提示条 | ✗（开关关闭"部分认证可提款"后） | ✗ | K4 |
| **Fully Verified 已通过** | APPROVED | ✓ | **✓** | ✓ | — |
| Rejected 已驳回 | REJECTED | 可进入，显示提示条 | ✗ | ✗ | K3 |

- **唯一放行条件：KYC 状态 = APPROVED**（含绿色通道自动通过、继承老站且状态为通过的账号）。
- 「部分认证用户可提款」开关：本需求上线后在 789games **强制关闭并隐藏**（不可再打开）；789bingo 保持现状（待确认 1）。
- 拦截顺序（沿用 R18，KYC 排第一）：**KYC → 未绑手机号 → 未绑提款账户 → 打码 → 余额 → 限额 → 首提规则**。命中 KYC 即返回，不再提示后面的原因。
- 3 天未 KYC 临时冻结：账号既未通过 KYC 又被临时冻结时，**只弹 KYC 弹窗**（K1），不再叠加冻结弹窗；KYC 通过后临时冻结自动解除（沿用现网逻辑，待后端确认）。
- 冻结 / 停用 / 自我排除账号：沿用现网拦截，优先级高于 KYC（先提示账号受限）。

### 2.2 服务端校验点

| 校验点 | 接口 | 未通过时 |
|---|---|---|
| ① 提现页信息 | `GET /withdraw/info` | 返回 `kycStatus`、`withdrawAllowed=false`、`blockReason=KYC_*` |
| ② 提交提现 | `POST /withdraw/apply` | 拒绝下单，错误码 `4101~4104`（占位），不冻结余额 |
| ③ 绑定提款账户 | `POST /withdraw/account/bind` | 拒绝，错误码同上 |
| ④ 出款前 | 审核通过 → 代付下单前 | KYC ≠ APPROVED：订单转「待人工处理」，不调三方代付，记日志 + 后台告警计数 |

- 状态以 DB 为准，不以 Redis 缓存作为唯一判断依据（知识库风险 #3）。
- 老包（不认识新错误码）：服务端照常拦截，前端走通用错误弹窗显示 `message`（英文文案由服务端下发）。

### 2.3 在途订单（上线时）
- 上线前已创建、尚未出款的提现单：在 ④ 出款前校验，KYC 未通过的转「待人工处理」，由客服联系玩家完成 KYC；**不自动驳回、不自动退款**（待确认 3）。

---

## 3. 前台流程

```
点 Withdraw（钱包 / 首页余额 / 个人中心）
   └─ GET /withdraw/info
        ├─ kycStatus = APPROVED → 正常提现页 → Submit → POST /withdraw/apply → 服务端再校验 → 成功
        └─ 其他 → 提现页顶部提示条 + 自动弹出对应 K 弹窗
               ├─ K1 Unverified / K4 Partial → [Verify Now] 进入 KYC 流程；[Later] 关闭留在提现页（Submit 置灰）
               ├─ K2 Pending → [OK] 关闭；[Contact CS]
               └─ K3 Rejected → [Resubmit] 进入 KYC 重提；[Contact CS]
KYC 完成并通过 → 回到提现页自动刷新 → 可提交
```

### 3.1 页面编号

| 编号 | 页面 | 触发条件 | 页面表现 |
|---|---|---|---|
| W1 | 提现页（已通过） | kycStatus = APPROVED | 与现网一致 |
| W2 | 提现页（未通过） | 其他状态 | 顶部黄色提示条（文案见 3.2），金额可输入，**Submit 置灰**；点 Submit / 绑定账户 → 弹对应 K 弹窗 |
| K1 | 未认证弹窗 | UNVERIFIED，进入提现页自动弹一次；点 Submit 再弹 | 见文案 |
| K2 | 审核中弹窗 | PENDING | 见文案 |
| K3 | 已驳回弹窗 | REJECTED | 显示驳回原因（沿用 E-KYC Rejected 的 4 类原因） |
| K4 | 部分认证弹窗 | PARTIAL | 见文案 |

弹窗规则：
- 页面级弹窗，不进首页弹窗队列；**不与 21+ / 协议弹窗叠加**（提现页本身在登录后，正常不会同时出现）。
- 同一次进入提现页只自动弹 1 次；关闭后点 Submit / 绑卡再弹。
- K1 / K4 可关闭（Later），关闭后仍不可提交——与现网"强制 KYC 弹窗不可关闭"不同，见待确认 2。

### 3.2 文案（English）

| 位置 | 标题 | 正文 | 按钮 |
|---|---|---|---|
| 提示条 W2 | — | KYC verification is required before withdrawal. | Verify › |
| K1 未认证 | Verify Your Identity | Players must complete and pass KYC verification before they can withdraw funds. It only takes a few minutes. | Verify Now / Later |
| K2 审核中 | Verification Under Review | Your KYC is being reviewed. You can withdraw once it is approved. We will notify you when the review is complete. | OK / Contact CS |
| K3 已驳回 | Verification Not Approved | Your KYC verification was rejected. Reason: {reason}. Please resubmit your documents to withdraw. | Resubmit / Contact CS |
| K4 部分认证 | Complete Your Verification | Your verification is not yet complete. Please finish all steps to enable withdrawals. | Continue / Later |
| 服务端兜底 Toast | — | Please complete KYC verification before withdrawing. | — |

### 3.3 交易记录
- 被拦截不生成提现单、不冻结余额，交易记录无新增。
- ④ 出款前被拦的订单：前台提现记录状态显示 **Processing**（不对玩家暴露"KYC 拦截"内部状态），客服联系处理。

---

## 4. 后台配置

### 4.1 提现管理 › 提现设置（现有页，新增 / 调整）

| 字段 | 规则 |
|---|---|
| 提现前须通过 KYC（新增） | 开关，按站点；789games 上线即**开启**（合规要求，见待确认 4）；修改需二次确认 + Google 验证码，写操作日志 |
| 部分认证用户可提款（现有） | 789games：上项开启时强制关闭并置灰，提示"已由『提现前须通过 KYC』接管" |
| 出款前 KYC 复核（新增） | 开关，默认开启；随上项联动，不可单独关闭 |

### 4.2 提现管理 › 提现审核列表
- 新增列「KYC 状态」（Unverified / Pending / Partial / Approved / Rejected），非 Approved 标红。
- 新增筛选「KYC 状态」。
- 新增订单状态「待人工处理（KYC 未通过）」；操作：「重新校验」（KYC 已通过后可继续出款）/「驳回并退回余额」（需原因）。

### 4.3 提现管理 › KYC 拦截日志（新增菜单）
- 筛选：时间（GMT+8）、会员 ID、手机号后 4 位、拦截点（info / apply / bind / payout）、KYC 状态、端。
- 字段：时间、会员 ID、手机号（前 3 后 4）、KYC 状态、拦截点、端 / 版本、IP、订单号（payout 时）。
- 导出：≥1 万条异步。保留 180 天。

### 4.4 权限码（cate=3，号段待后端确认）

| 权限码 | 名称 |
|---|---|
| 待分配 | 提现设置-提现前须通过 KYC 开关 |
| 待分配 | 提现审核-重新校验 KYC |
| 待分配 | 提现审核-驳回并退回余额（KYC） |
| 待分配 | KYC 拦截日志-查看 / 导出 |

顶部状态条新增计数「KYC 拦截待处理」（出款前被拦订单数，红色）。

---

## 5. 统计、日志与埋点

| 事件 | 变更 |
|---|---|
| withdraw_block | `reason=kyc` 时新增参数 `kyc_status`: unverified / pending / partial / rejected，`point`: page / submit / bind |
| kyc_prompt_view | `trigger=withdraw`，新增 `popup`: K1 / K2 / K3 / K4 |
| kyc_start | `trigger=withdraw`（从 K1 / K3 / K4 进入） |
| kyc_result → 回到提现页 | 新增 `withdraw_unlock`（S，KYC 通过后首次成功提交提现） |

- 服务端：拦截日志（4.3）即服务端口径；前端埋点上报通道沿用 firebase-tracking-spec（服务端事件通道待确认）。

---

## 6. 接口（草案）

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | /withdraw/info | 新增 `kycStatus`、`withdrawAllowed`、`blockReason`、`kycRejectReason` |
| POST | /withdraw/apply | 先校验 KYC；未通过返回 4101 未认证 / 4102 审核中 / 4103 驳回 / 4104 部分认证（占位） |
| POST | /withdraw/account/bind | 同上 |
| 内部 | payout.precheck | 代付下单前读 DB 校验 KYC，失败转待人工 + 告警 |

- 不收 userId，从 JWT 取；requestId 幂等（沿用现网）。

---

## 7. 验收要点

1. 5 种 KYC 状态 × 3 个入口（提现页、Submit、绑卡）：只有 Approved 能提交，其余弹对应 K 弹窗且 Submit 置灰。
2. 直接调 `/withdraw/apply`（绕过前端 / 老包）：非 Approved 返回 410x，不冻结余额、不生成订单。
3. 提现单审核中把 KYC 改为 Rejected → 审核通过后不调三方代付，订单进「待人工处理」，状态条计数 +1。
4. KYC 通过后回到提现页自动刷新为 W1，可正常提交；绿色通道账号、继承老站已认证账号直接可提。
5. 789games 开关开启后，「部分认证可提款」置灰不可改；789bingo 不受影响。
6. 3 天临时冻结 + 未认证：只弹 K1 一个弹窗。
7. 多端：H5 / Android / iOS / Flutter 老包逐端；老包显示服务端下发的英文 message。
8. 拦截日志时间 GMT+8，00:00 跨天归日正确；导出与页面一致。

---

## 8. 待确认

1. 是否同步到 789bingo（共用后端，本期默认只开 789games）。— 产品 / 合规
2. K1 / K4 是否沿用现网"强制 KYC 弹窗不可关闭"。本期默认**可关闭但不能提交**，避免玩家卡死在提现页。— 产品
3. 上线时在途提现单 KYC 未通过：默认转人工不自动驳回；是否改为自动驳回并退回余额。— 财务 / 客服
4. 新开关默认值：模版要求新开关默认关闭，但这是合规硬性要求，本期默认 789games **上线即开启**。— 合规确认
5. 「Verified」与「Fully Verified」的后端枚举映射，以及绿色通道跳过姓名校验（-6570）的账号是否算 APPROVED。— 后端
6. 错误码号段、权限码号段。— 后端
7. 无手机号的三方登录账号：先提示绑手机号还是先提示 KYC（当前按 KYC 优先）。— 产品

## 9. 风险与依赖

| 等级 | 类别 | 风险 | 应对 |
|---|---|---|---|
| 高 | 合规 | 仅前端拦截被老包 / 直调绕过 | 服务端 ②③④ 三处校验，拦截日志留痕 |
| 高 | 资金 | 在途订单 KYC 后被驳回仍出款 | 出款前复核，失败转人工不调代付 |
| 中 | 体验 | 审核积压导致大量玩家提不了款、客诉上升 | 上线前清点 Pending 数量；后台"实名认证-待处理"计数监控；K2 给 Contact CS |
| 中 | 多端一致性 | KYC 改版 App 未同步（-5825）、iOS 黑屏（-2122） | 逐端验收，老包走服务端 message |
| 低 | 稳定性 | KYC 状态缓存与 DB 不一致 | 以 DB 为准，缓存 ≤10s |

依赖：后端 KYC 状态枚举统一；权限码分配；埋点通道；客服话术（K2 / K3 Contact CS）。

## 10. 变更记录

| 日期 | 变更 |
|---|---|
| 2026-11-27 | v1.0 初稿：按需求原文第 5 条写放行规则、4 个拦截弹窗、服务端 4 处校验、后台开关 / 列表 / 拦截日志；原型 v1.0 |
