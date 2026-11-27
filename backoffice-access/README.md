# 后台访问合规（PAGCOR / megaXcess）v1.0

- 在线原型：https://koi980517.github.io/789games/backoffice-access/backoffice-access-prototype-v1.0.html
- PRD：[PRD-backoffice-access-v1.0.md](PRD-backoffice-access-v1.0.md)
- 依据：PAGCOR GSA 规定「Back-office access｜后台访问」——一个 GSA 一个后台、一个 URL；PAGCOR 和 megaXcess 随时可访问；后台或访问方式变更须通知 PAGCOR。
- 更新日期：2026-11-27（GMT+8）。示例数据均为虚构，非线上配置。

## 页面

| 编号 | 页面 | 说明 |
|---|---|---|
| A1 | 统一登录页 | 一个 URL，按账号类型（员工 / 代理 / 监管）走不同二次验证；旧入口 301 或下线 |
| A2 | 顶栏站点切换 | 全部 / 789games / 789bingo；监管账号显示「监管只读」标签 |
| A3 | 系统管理 › 监管账号 | 新增 / 停用须关联「已通知 PAGCOR」的变更单；最后一个启用账号不能停用 |
| A4 | 系统管理 › 访问变更登记 | 草稿 → 待合规审核 → 待通知 → 已通知 PAGCOR（上传回执）→ 已生效 |
| A5 | 系统管理 › 监管访问监控 | 可用性探测、账号健康、监管访问日志 |
| A6 | 监管只读视图 | 写操作按钮隐藏，服务端拒绝写接口 |

## 变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-11-27 | v1.0 | 初稿 |
