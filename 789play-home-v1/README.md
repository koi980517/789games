# 789Play · 首页 V1 原型（按 Figma 1:1 还原）

| 项 | 内容 |
|---|---|
| 状态 | 原型 v1.0，交给设计 / ChatGPT 继续出稿 |
| 负责人 | Koi（产品） |
| 日期 | 2026-11-25 |
| 来源 | Figma「789Play 设计草稿」→ V1 + V2 : INTERFACE COMPARISON → 789P V1（node `196:42373`，390×3669） |
| 在线原型 | [789Play V1 首页原型](https://claude.ai/artifact/YV9Hsxs5YHr7erppdfMsGj) |
| GitHub Pages | https://koi980517.github.io/789games/789play-home-v1/789play-home-v1-prototype.html |

## 目录

| 路径 | 说明 |
|---|---|
| [789play-home-v1-prototype.html](789play-home-v1-prototype.html) | 可交互原型，单文件，图片已内嵌，下载后用浏览器直接打开 |
| [src/template.html](src/template.html) | 页面模板（HTML / CSS / JS），图片位置写成 `{{name}}` |
| [src/build.py](src/build.py) | 把 `assets/` 里的图片内嵌进模板，重新生成原型：`python3 src/build.py` |
| [assets/](assets/) | 从 Figma 1x 渲染图截下来的图片（Banner、活动卡、游戏卡、厂商 logo、导航图标等） |
| [reference/figma-789P-V1-1x.png](reference/figma-789P-V1-1x.png) | Figma 原稿整页截图，用来对比 |

## 规范
- 颜色：#141115 底色 / #FF6200 主橙 / #FFCA38 金黄 / #FFFFFF
- 字体：Inter；画布宽 390（iPhone 14）
- 写成代码的部分：Header、区块标题、分类 Tab、Game Providers 标题、About / Information Center / Help 文案、版权、底部导航
- 用切图的部分：Banner、3 张活动卡、Popular Games、Spin & Win、Pusoy / Poker / Live / Slots、游戏卡、Recent Big Wins、厂商 logo、社媒图标、监管 logo

## 可交互
顶部 Login / Register & Spin Now、分类 Tab、游戏卡收藏 ♥、Read more、底部导航

## 与设计稿的差异 / 待确认
1. 「Recommended Games」「Slots」「Arcade」三个标题在稿里被 Tab 和游戏卡压住，原型里没显示，需设计确认这三个区块要不要。
2. Live / Slots 下方的灰色占位条视为草稿痕迹，没做。
3. About 文案在稿里只写到「…and PAGCOR-」，完整文案待补充。
4. 图片是 1 倍图，高清屏会略糊；要 2 倍图需设计导出切图。
