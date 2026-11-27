# 第三方登录入口后台开关 v1.0

后台按站点控制登录 / 注册弹窗的 Google、Facebook、Telegram 按钮显示或隐藏，保存即时生效，H5 与 App 一致。

- PRD：[docs/PRD.md](docs/PRD.md)
- 原型：[third-login-switch-prototype-v1.0.html](https://koi980517.github.io/789games/third-login-switch/third-login-switch-prototype-v1.0.html)（左侧后台改开关 → 保存 → 右侧手机即时刷新；可模拟站点、接口失败）

| 场景 | 表现 |
|---|---|
| L1 三个都开 | 与现网一致 |
| L2 部分关闭 | 只显示开启的，居中 |
| L3 全部关闭 | 「or continue with」整块隐藏 |
| L4 上次登录方式被关 | 不显示 LAST 角标 |

2026-11-27 · Koi
