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
  "spins": [{"no": 1, "type": "FREE"}, {"no": 2, "type": "FREE"}, {"no": 3, "type": "PAID"}],
  "slots": [
    {"index": 0, "amount": 7890, "freeProbability": 0},
    {"index": 1, "amount": 789,  "freeProbability": 0},
    {"index": 2, "amount": 78.9, "freeProbability": 0},
    {"index": 3, "amount": 2.34, "freeProbability": 30},
    {"index": 4, "amount": 1.23, "freeProbability": 35},
    {"index": 5, "amount": 4.56, "freeProbability": 20},
    {"index": 6, "amount": 12.3, "freeProbability": 5},
    {"index": 7, "amount": 23.4, "freeProbability": 0},
    {"index": 8, "amount": 45.6, "freeProbability": 0},
    {"index": 9, "amount": 7.89, "freeProbability": 10}
  ],
  "freeWithdrawWaterMult": 1,
  "freeNeedBonus": true,
  "paid": {
    "needRecharge": false,
    "rechargeCountCondition": {"relation": "gte", "count": 1},
    "rechargeChannels": ["PayMongo", "Traxion Pay", "PayCools"],
    "firstTimeRewards": [
      {"minRecharge": 500, "maxRecharge": 1000, "rewardItems": [{"slotIndex": 7, "probability": 80}, {"slotIndex": 8, "probability": 20}]}
    ],
    "nonFirstTimeRewards": [
      {"minRecharge": 500, "maxRecharge": 1000, "rewardItems": [{"slotIndex": 6, "probability": 80}, {"slotIndex": 7, "probability": 20}]}
    ],
    "firstTimeWithdrawWaterMult": 2, "firstTimeNeedPrincipal": false, "firstTimeNeedBonus": true,
    "nonFirstTimeWithdrawWaterMult": 3, "nonFirstTimeNeedPrincipal": false, "nonFirstTimeNeedBonus": true
  },
  "rewardPopupText": "Get ₱ {bonus} From Lucky Spin",
  "grantPopupText": "You've got {count} Lucky Spins! Spin now to win up to ₱{max}"
}
```

`paid` 的档位结构沿用老转盘 `firstTimeRewards` / `nonFirstTimeRewards`，区别是奖励用 `slotIndex` 指向盘面格（金额取 `slots[slotIndex].amount`），保证转盘能停在对应格。

保存时服务端需要校验：

- `spins` 1–10 个，type 为 FREE / PAID；`slots` 正好 10 个，amount > 0；
- 有 FREE 转：`freeProbability` 之和 = 100；
- 有 PAID 转：渠道 ≥ 1；每档 min ≤ max（max 空 = 无穷大）、rewardItems ≤ 2 且概率和 = 100、slotIndex 在 0–9；同类型档位区间不重叠。

### 发放

单个发放的请求：

```json
{"activityId": "1301", "userId": 123456, "spinCount": 1, "spinType": "TEMPLATE", "remark": "按活动转数 1 轮"}
```

服务端规则：

- 校验用户是否存在；
- 校验次数上限；
- 按“次数 × 该类型最高奖”预估成本，超过剩余预算则拒绝；
- 写入发放记录和操作日志。

CSV 模板：

```
userId,spinCount,spinType,remark
123456,1,TEMPLATE,按活动转数 1 轮
208871,2,PAID,补偿
```

### 发放记录 grant

| 字段 | 说明 |
|---|---|
| grantId | 记录ID |
| activityId | 活动 |
| userId | 用户 |
| spinType | TEMPLATE / FREE / PAID（TEMPLATE 按转数设置展开为逐转次数） |
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
| GET | `/api/activity/whitelistSpin/info` | `slots[10]`（只含 index、amount，不返回概率和类型）、`remaining`、`currentSpinType`、`expireTime`、`jackpot`、`showGrantPopup`、`winners[]`（本活动最近 30 条真实中奖：`maskedAccount`、`amount`、`drawTime`，按时间倒序） |
| POST | `/api/activity/whitelistSpin/draw` | `slotIndex`、`amount`、`remaining`、`grantId`、`drawId` |

draw 的处理流程：

1. 校验以下条件，任一不满足则返回“活动已结束”：
   - 活动开启且在有效期内；
   - 预算充足；
   - 用户还有剩余次数。
2. 加锁，取最早发放、仍有剩余次数的那条记录的下一转；若下一转是 PAID 且未解锁（没有满足渠道 / 人群范围、并命中档位的到账充值），返回 `needDeposit=true`，前端引导充值；否则先扣减 `usedCount`。
3. FREE 转按 `freeProbability` 抽格；PAID 转按解锁它的那笔充值匹配档位（首次 / 非首次 + 金额），按档位 rewardItems 抽格。
4. 写入抽奖明细和稽核：稽核金额 = amount × 该类型流水倍数。
5. 返回结果，前端转到 `slotIndex` 对应的格子后停下。

`winners` 也可以单独提供 `GET /api/activity/whitelistSpin/winners` 供前端每 60 秒刷新；账号脱敏在服务端完成，不返回 userId。

draw 需要支持幂等：前端带上 `requestId`，避免重复点击时重复扣次数。
