# 接口草案（供前后端对齐，字段名以后端定稿为准）

## 1. 后台接口

建议沿用现网路由风格，前缀为 `/api/admin/activity/whitelistSpin`，activityType 为 `WHITELIST_SPIN`。

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/config/list` | 活动列表 |
| POST | `/create` · `/update` | 保存活动，规则写在 configJson 里 |
| POST | `/delete` | 软删除；只有关闭、且没有未使用次数的活动可以删 |
| GET | `/whitelist/csvTemplate` | 下载白名单模板（表头 phone） |
| POST | `/whitelist/importCsv` | FormData(activityId, file)；须先保存活动；返回 totalRows / validRows / invalidRows / duplicateInFile / insertedRows / existedRows / batchId |
| GET | `/whitelist/exportCsv?activityId=` | 已导入文件下载 |
| GET | `/whitelist/summary?activityId=` | 名单状态：总数、未注册、已注册生效、最近更新时间、操作人 |
| POST | `/query` · `/queryTotalReward` | 统计明细和汇总 |

### configJson

```json
{
  "receiveType": 0,
  "needKyc": false,
  "slots": [7890, 789, 78.9, 2.34, 1.23, 4.56, 12.3, 23.4, 45.6, 7.89],
  "wheels": [
    {"wheelId": "W1", "name": "免费转盘1", "probabilities": [0, 0, 0, 30, 35, 20, 5, 0, 0, 10]},
    {"wheelId": "W2", "name": "免费转盘2", "probabilities": [0, 1, 9, 0, 0, 0, 20, 40, 30, 0]}
  ],
  "spins": [{"no": 1, "wheelId": "W1"}, {"no": 2, "wheelId": "W1"}, {"no": 3, "wheelId": "W2"}],
  "withdrawWaterMult": 1,
  "needBonus": true,
  "wagerScope": {"type": "GAMES", "categories": [], "gameIds": ["JL-101", "JL-102", "PG-117"]},
  "rewardPopupText": "Get ₱ {bonus} From Lucky Spin",
  "grantPopupText": "You've got {count} Lucky Spins! Spin now to win up to ₱{max}"
}
```

`wagerScope.type`：`ALL` 全部游戏 / `CATEGORIES`（`categories` 取后端 6 类分类码：SLOT、CASINO、POKER、BINGO、ARCADE、FISHING）/ `GAMES`（`gameIds` 为后端游戏 ID）。游戏树复用返水活动「选择指定游戏」接口（分类 → 厂商 → 游戏 ID）。

保存时服务端需要校验：

- `slots` 正好 10 个，金额 > 0；`wheels` 1–5 个，每个 `probabilities` 10 个整数、合计 100；
- `spins` 1–10 个，`wheelId` 必须存在；每个转盘至少被 1 转使用；
- `wagerScope`：CATEGORIES 至少 1 类，GAMES 至少 1 个游戏 ID。

### 白名单

沿用老用户充值转盘现有导入接口与表结构（按手机号）。名单内用户各获得 1 轮转数（`spins` 全部），以“名单记录”为单位记已用次数：

| 字段 | 说明 |
|---|---|
| activityId / phone / userId | userId 在注册后回填，未注册为空 |
| status | UNREGISTERED / ACTIVE |
| usedCount | 已转次数（≤ spins 数） |
| batchId | 导入批次 |
| createdAt / operator | 导入时间、操作人 |

## 2. 前台接口

| 方法 | 路径 | 返回 |
|---|---|---|
| GET | `/api/activity/whitelistSpin/info` | `slots[10]`（只含 index、amount，不返回概率和类型）、`remaining`、`nextSpinNo`、`expireTime`、`jackpot`、`showGrantPopup`、`winners[]`（本活动最近 30 条真实中奖：`maskedAccount`、`amount`、`drawTime`，按时间倒序） |
| POST | `/api/activity/whitelistSpin/draw` | `slotIndex`、`amount`、`remaining`、`drawId` |

draw 的处理流程：

1. 校验以下条件，任一不满足则返回“活动已结束”：
   - 活动开启且在有效期内；
   - 预算充足；
   - 用户还有剩余次数。
2. 加锁，取该用户名单记录的下一转，先扣减 `usedCount`。
3. 按这一转 `wheelId` 对应转盘的 `probabilities` 抽格。
4. 写入抽奖明细和稽核：稽核金额 = amount × `withdrawWaterMult`，稽核只统计 `wagerScope` 内游戏的有效投注。
5. 返回结果，前端转到 `slotIndex` 对应的格子后停下。

`winners` 也可以单独提供 `GET /api/activity/whitelistSpin/winners` 供前端每 60 秒刷新；账号脱敏在服务端完成，不返回 userId。

draw 需要支持幂等：前端带上 `requestId`，避免重复点击时重复扣次数。
