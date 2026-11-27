# 【789games / 789bingo】KYC 后台审核显示对齐 + Nature of Work 选项精简 PRD v1.0

2026-11-27 · Koi

| 资料 | 链接 |
| --- | --- |
| 原型 v1.0（玩家端 / 运营后台 / 改动对照） | [koi980517.github.io/789games/kyc-review](https://koi980517.github.io/789games/kyc-review/) |
| GitHub 目录 | [koi980517/789games › kyc-review](https://github.com/koi980517/789games/tree/main/kyc-review) |
| 参考 | 用户端字段顺序：[BB789BINGO-7671](https://jira.bbops.ph/browse/BB789BINGO-7671)；后台 KYC 弹窗现状：[admin/user-management.html](https://koi980517.github.io/789games/admin/user-management.html)（会员 → 更多 → KYC信息） |
| 读者 | 前端、后端、测试 |

## 1. 背景与范围

**现状（后台「会员 → 更多 → KYC信息」）**

- 字段顺序、名称与用户端不一致，缺少「性别 Gender」。
- 「投注站」下拉是另一套名称（LAGUNA、BUENDIA PASAY…），和用户端 Game Venue 对不上。
- 必填项为空时只显示空白，审核员分不清是没填还是没加载出来。
- 中英文混排（按钮英文，其余中文）。

**本期包含**

1. 后台 KYC 审核弹窗：字段、顺序、选项、取值与用户端一致。
2. 用户端必填项缺失时，后台显示「待验证 Pending Verification」。
3. 前台、后台的 Nature of Work（工作性质）选项移除 **Youth Worker**、**Legal Clerk**。

**不包含**：KYC 审核流程、状态流转、eKYC 供应商逻辑、NDRP 名单校验（GAM-649 / GAM-703）。

**站点**：789games、789bingo，规则相同。

## 2. 后台显示规则

### 2.1 字段与顺序（与用户端一致）

后台按用户端 KYC 表单的顺序显示，标签用「中文 + 英文原名」，取值直接显示用户提交的原值（下拉项显示与前台相同的英文选项）。

| # | 用户端字段 | 后台标签 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| 1 | ID Type | 证件类型 ID Type | 是 | 选项与前台一致（8 项，顺序同前台） |
| 2 | （eKYC 识别） | 证件号码 ID Number | 是 | eKYC 识别带出，前台表单不显示 |
| 3 | First Name | 名 First Name | 是 | |
| 4 | Middle Name | 中间名 Middle Name | 条件 | 用户勾选 No middle name → 显示「无 N/A」，不算缺失 |
| 5 | Last Name | 姓 Last Name | 是 | 全名 = 名 + 中间名 + 姓，只读拼接 |
| 6 | Birthday | 生日 Birthday | 是 | 格式 YYYY-MM-DD |
| 7 | Gender | 性别 Gender | 是 | **新增**；Male / Female / Others |
| 8 | Game Venue | 投注站 Game Venue | 是 | **改用前台同一套投注站列表** |
| 9 | Place of Birth | 出生地 Place of Birth | 是 | |
| 10 | Current Home Address | 当前地址 Current Home Address | 是 | |
| 11 | Permanent Home Address | 永久居住地 Permanent Home Address | 是 | 用户勾选 Same as current → 显示「同当前地址」+ 地址原文 |
| 12 | Nationality | 国籍 Nationality | 是 | |
| 13 | Source of Income | 收入来源 Source of Income | 是 | |
| 14 | Nature of Work | 工作性质 Nature of Work | 是 | 见第 3 节 |
| 15 | ID Photo / eKYC | 证件照 / eKYC 截屏 | 是 | 图片可点击放大 |

后台独有内容（备注、证件背面、自拍照、收入证明、NDRP 图片、审核记录）放到弹窗下方「审核附加信息」区，不混入用户资料区。

### 2.2 待验证 Pending Verification

- 判定：用户端**必填**字段为空、null 或全空格；图片字段无文件。
- 显示：该字段值位置显示橙色标签「待验证 Pending Verification」，标签前的字段名标红。
- 汇总：弹窗顶部显示「有 N 项必填信息待验证」，点击定位到第一个缺失字段。
- 非必填字段为空显示「--」，不显示待验证。
- 点「通过 Pass KYC」时若仍有待验证项：弹二次确认，列出缺失字段，确认后才提交。
- 后台补录：审核员在弹窗内补填并保存后，标签消失。

### 2.3 其他

- 按钮改中文：保存 / 通过 KYC / 拒绝 KYC。
- 取值由接口 `GET /api/admin/userKyc/getById/{id}` 返回；如缺 gender、noMiddleName、sameAsCurrent 字段需后端补充。

## 3. Nature of Work 选项精简

- 从工作性质字典（`works/queryAll`）删除 **Youth Worker**、**Legal Clerk**，前台（H5 / APP）和后台下拉同时生效。
- 存量用户已选这两项：后台照原值显示，旁边加灰色标签「已下线选项」，不判为缺失；用户在前台重新编辑 KYC 时需重新选择。
- 删除方式建议「停用」而不是物理删除，保证历史数据可回显。

## 4. 验收要点

1. 同一用户，后台 KYC 弹窗的字段顺序、取值与用户端提交内容逐项一致（含性别、投注站名称）。
2. 用户端任一必填项为空 → 后台对应字段显示「待验证 Pending Verification」，顶部数量正确；补录保存后消失。
3. 勾选 No middle name / Same as current 的用户，不出现待验证。
4. 有待验证项时点「通过 KYC」弹二次确认并列出缺失字段。
5. 前台 H5、APP、后台的 Nature of Work 下拉中都没有 Youth Worker、Legal Clerk；存量用户后台显示原值 +「已下线选项」。
6. 789games、789bingo 两站表现一致。

## 5. 待确认

1. 用户端必填项清单以前台现网为准（BB789BINGO-7671 提到部分必填标记缺失），请前端提供最终必填列表。
2. 有待验证项时，「通过 KYC」是二次确认后放行（本稿方案），还是直接禁止通过？
3. 后台投注站下拉切换为前台列表后，旧名称的存量数据如何映射。
4. 两站是否共用同一份工作性质字典。

## 6. 变更记录

| 版本 | 日期 | 内容 |
| --- | --- | --- |
| v1.0 | 2026-11-27 | 初稿 |
