# 789games / 789bingo · KYC 验证状态与后台 Gaming Venue 字段调整

按合规文件第 7 节「KYC Verification and Back-Office Gaming Venue Requirements」调整：

1. 必填 KYC 资料（F1–F11）全部完整、且证件 / 人脸 / 审核通过，才能标记 **Verified**；任一缺失保持 **Pending Verification**。
2. 后台会员详情的「投注站」改为英文 **Gaming Venue**，值只取玩家 KYC 时选择的场所。
3. 所有 KYC 字段必填：「KYC 提交信息配置」中合规字段锁定为显示 + 必填。

| 项 | 内容 |
|---|---|
| 状态 | PRD v1.0 初稿，待评审 |
| 负责人 | Koi（产品） |
| 日期 | 2026-11-27 |
| 需求来源 | 合规文件第 7 节（PAGCOR 合规要求） |
| 关联 Jira | -6448 / -6450（KYC 提交信息配置 + 10 站点选择）、-5603（Venue 清单）、GAM-2 |
| Jira（本需求） | 待建：故事单 + 后端 / 后台前端 / H5 / iOS / Android |
| 站点 | 789games + 789bingo（共用 KYC 库，待确认 Q2） |

## 目录

| 路径 | 说明 |
|---|---|
| [docs/PRD.md](docs/PRD.md) | 需求说明：现状、必填字段、状态判定、Gaming Venue 取值、前后台改动、接口、验收、待确认 |
| [kyc-gaming-venue-prototype-v1.0.html](kyc-gaming-venue-prototype-v1.0.html) | 可交互原型，单文件，下载后浏览器直接打开 |

**怎么用原型**：顶部四个页签。

- **运营后台**：会员详情（可切「现网（截图）/ 调整后」、切 4 个示例会员）；KYC 审核（对缺资料账号点「通过」看结果）；KYC 提交信息配置（合规字段锁定）；KYC 完整性检查（存量迁移）。
- **玩家端**：A1 Account 状态、P1 提款卡点弹窗、K3 首次填写、K4 补充资料。提交后回后台可看到状态同步变化。
- **状态判定**：勾选字段和条件，实时算出状态。
- **改动对照**：现网 vs 调整后。

示例数据，非线上配置；截图中的真实玩家资料已替换为示例值。

## 待确认（摘要）

Q1 现网「投注站」值的来源 · Q2 两站是否同时生效 · Q3 Verified / Fully Verified 映射 · Q4「部分认证用户可提款」开关 · Q5 客服能否代改 Gaming Venue · Q6 存量是否降级 · Q7 在途提款单 · Q8 下拉选项 · Q9 埋点通道
