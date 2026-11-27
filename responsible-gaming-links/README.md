# 【789bingo / 789games】负责任博彩链接可点击（NPGH / RGD）v1.0

- 日期：2026-11-27 · Koi
- PRD（Claude Doc）：https://claude.ai/artifact/2ADbtRR2x2do2Dmu3AWGy9
- 原型：`responsible-gaming-links-prototype-v1.0.html`（页签：玩家端 / 字段示意图 / 改动对照；可切站点、弹窗/页脚、H5/App/PC、现网/调整后）
- 在线版：https://koi980517.github.io/789games/responsible-gaming-links/responsible-gaming-links-prototype-v1.0.html
- 来源：合规通知「2. Responsible gaming links」— NPGH 热线和 RGD 自我排除邮箱在负责任博彩弹窗和网站页脚都必须可点击；使用新版 NPGH 标志，NPGH 官网链接可点击。

## 现状（2026-11-27 读取正式站 H5 首页页脚）

| 元素 | 789games | 789bingo |
|---|---|---|
| NPGH 标志 | 旧图，不可点 | 旧图，不可点 |
| Need Help? (02) 8248 9568 | 图片，不可点 | 图片，不可点 |
| RGD_exclusion@pagcor.ph | mailto，可点 | SVG 图片，不可点 |
| RGD@pagcor.ph | mailto，可点 | SVG 图片，不可点 |
| 21+ 负责任博彩弹窗 | 未触发验证 | 未触发验证（代码显示弹窗内含同一 npgh 区块） |

## 改动（弹窗 R1 与页脚 R2 相同，两站共用一个组件）

| 编号 | 元素 | 链接 | 点击后 |
|---|---|---|---|
| L1 | NPGH 标志（换新版） | `https://npgh.ph` | H5/PC 新标签页；App 系统浏览器 |
| L2 | Need Help? Call us at (02) 8248 9568 | `tel:+63282489568` | 系统拨号盘；PC 复制号码 + Toast |
| L3 | RGD_exclusion@pagcor.ph | `mailto:RGD_exclusion@pagcor.ph` | 系统邮件，收件人已填 |
| L4 | RGD@pagcor.ph | `mailto:RGD@pagcor.ph` | 系统邮件，收件人已填 |

- L2–L4 改为前端文字渲染（蓝色下划线，点击高度 ≥ 32px）；点击弹窗内链接不关弹窗、不计同意；游客可点。
- App WebView 必须拦截 `tel:` / `mailto:` / 外链交给系统。
- 埋点 `rg_link_click`：target（npgh_site / hotline / rgd_exclusion / rgd）、placement（popup / footer）、site。

## 待确认

1. NPGH 官网最终地址（默认 https://npgh.ph）
2. 新版 NPGH 标志原图（原型中为通知截图裁剪的示意图）
3. 21+ 弹窗两站现网表现，需 QA 触发截图
4. 链接写死前端（默认）还是后台配置
5. PC 点热线：复制号码 + Toast（默认）还是直接 tel:
6. iOS / Android App 是否已拦截 tel / mailto
7. 789games 页脚 PAGCOR / OSEA 文字链接是否可见（顺带核对）
8. 合规整改期限、Jira 单号
