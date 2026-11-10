# 接口草案（供前后端对齐，字段名以后端定稿为准）

## 1. 后台接口

建议沿用现网路由风格，前缀为 `/api/admin/activity/whitelistSpin`，activityType 为 `WHITELIST_SPIN`。

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/config/list` | 活动列表 |
| POST | `/create` · `/update` | 保存活动，规则写在 configJson 里 |
| POST | `/delete` | 软删除；只有关闭、且没有未使用次数的活动可以删 |
| POST | `/grant` | 单个发放 |
| GET | `/grant/csvTemplate` | 下载批量导入模板 |
| POST | `/grant/importCsv` | 上传 CSV，返回预览结果和 batchId |
| POST | `/grant/confirm` | 按 batchId 确认批量发放 |
| POST | `/grant/page` | 发放记录列表 |
| GET | `/grant/{grantId}` | 发放记录详情，含每次抽奖明细 |
| POST | `/grant/void` | 作废剩余次数，需填原因 |
| POST | `/query` · `/queryTotalReward` | 统计明细和汇总 |

### configJson

```json
{
  "receiveType": 0,
  "needKyc": false,
  "slots": [
    {"index": 0, "type": "DEPOSIT", "amount": 7890, "probability": 0},
    {"index": 1, "type": "DEPOSIT", "amount": 789,  "probability": 5},
    {"index": 2, "type": "DEPOSIT", "amount": 78.9, "probability": 25},
    {"index": 3, "type": "FREE",    "amount": 2.34, "probability": 30},
    {"index": 4, "type": "FREE",    "amount": 1.23, "probability": 35},
    {"index": 5, "type": "FREE",    "amount": 4.56, "probability": 20},
    {"index": 6, "type": "FREE",    "amount": 12.3, "probability": 5},
    {"index": 7, "type": "DEPOSIT", "amount": 23.4, "probability": 40},
    {"index": 8, "type": "DEPOSIT", "amount": 45.6, "probability": 30},
    {"index": 9, "type": "FREE",    "amount": 7.89, "probability": 10}
  ],
  "freeWithdrawWaterMult": 1,
  "freeNeedBonus": true,
  "depositWithdrawWaterMult": 2,
  "depositNeedBonus": true,
  "rewardPopupText": "Get ₱ {bonus} From Lucky Spin",
  "grantPopupText": "You've got {count} Lucky Spins! Spin now to win up to ₱{max}"
}
```

保存时服务端需要校验：

- `slots` 必须正好 10 个；
- FREE、DEPOSIT 两组的 `probability` 各自之和都等于 100；
- 每组至少有一个格子的 `probability` 大于 0。

### 发放

单个发放的请求：

```json
{"activityId": "1301", "userId": 123456, "spinCount": 2, "spinType": "DEPOSIT", "remark": "11/08 充值掉单补偿"}
```

服务端规则：

- 校验用户是否存在；
- 校验次数上限；
- 按“次数 × 该类型最高奖”预估成本，超过剩余预算则拒绝；
- 写入发放记录和操作日志。

CSV 模板：

```
userId,spinCount,spinType,remark
123456,2,DEPOSIT,补偿
```

### 发放记录 grant

| 字段 | 说明 |
|---|---|
| grantId | 记录ID |
| activityId | 活动 |
| userId | 用户 |
| spinType | FREE / DEPOSIT |
| spinCount | 发放次数 |
| usedCount | 已使用次数 |
| status | UNUSED / IN_USE / USED_UP / VOID / EXPIRED |
| source | SINGLE / BATCH |
| batchId | 批量导入时的批次号 |
| remark | 备注 |
| operator | 操作人 |
| createdAt | 操作时间 |
| voidReason | 作废原因 |
| voidBy | 作废操作人 |
| voidAt | 作废时间 |

## 2. 前台接口

| 方法 | 路径 | 返回 |
|---|---|---|
| GET | `/api/activity/whitelistSpin/info` | `slots[10]`（只含 index、amount，不返回概率和类型）、`remaining`、`currentSpinType`、`expireTime`、`jackpot`、`showGrantPopup` |
| POST | `/api/activity/whitelistSpin/draw` | `slotIndex`、`amount`、`remaining`、`grantId`、`drawId` |

draw 的处理流程：

1. 校验以下条件，任一不满足则返回“活动已结束”：
   - 活动开启且在有效期内；
   - 预算充足；
   - 用户还有剩余次数。
2. 加锁，取最早发放、仍有剩余次数的那条记录，先扣减它的 `usedCount`。
3. 按这条记录的 `spinType`，在同类型的格子里按概率抽出一格。
4. 写入抽奖明细和稽核：稽核金额 = amount × 该类型流水倍数。
5. 返回结果，前端转到 `slotIndex` 对应的格子后停下。

draw 需要支持幂等：前端带上 `requestId`，避免重复点击时重复扣次数。
