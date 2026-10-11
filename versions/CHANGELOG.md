# CHANGELOG

## 2026-08-20 01:24:07

- 修改内容：新增 6.6 内核批量 KPM 构建入口，统一传递 KSU、susfs、KPM、LZ4、LZ4KD、BBR、Droidspaces、网络增强、ADIOS、Re-Kernel、基带保护和 ccache 参数。
- 覆盖版本：6.6.30、6.6.50、6.6.56、6.6.57、6.6.66、6.6.89、6.6.89_mtk。
- 版本映射：6.6.50 和 6.6.89_mtk 按远程 fastbuild 实际源码记录为 MT6991/天玑特供，其余版本按 SM8750/骁龙 8 Elite 记录。
- 影响文件：`build-test_6.6_kpm.yml`。
- 结果快照：`versions/build-test_6.6_kpm-20260820-012407-create.yml`。
- 验证：PowerShell 结构检查通过；UTF-8、无行尾空白和无明显明文密钥检查通过；提取的 Bash 发布脚本经 Git Bash `bash -n` 检查通过。
- 问题和坑点：远程 6.6 的七个 fastbuild 工作流当前没有声明 `workflow_call`，因此本批量入口还需要远程子工作流补充 reusable workflow 声明后才能实际运行；本次按用户确认范围只新增批量入口，没有改动远程或单版本工作流。
- AGENTS.md：未修改，沿用 `CCTV6.1/AGENTS.md` 的项目规则。
- GitHub 备份状态：本次修改和快照尚未上传 GitHub。

## 2026-08-20 上传记录

- 上传文件：仓库 `AoGou3175/cctv_6.6_oppo_oplus_realme_sm8750` 的 `.github/workflows/build-test_6.6_kpm.yml`。
- 上传方式：提交到 `main`，提交 SHA：`e819f7025edd29d1cf98355f01c12caac1befefa`。
- 验证：远程 `main` 已指向该提交；GitHub Raw 文件 HTTP 200，远程文件 SHA-256 与本地文件一致。
- 注意：远程七个 fastbuild 子工作流仍需声明 `workflow_call` 后，批量入口才能实际调用。
- GitHub 备份状态：已上传 GitHub。

## 2026-08-20 修复可复用工作流

- 修改内容：为 7 个 6.6 fastbuild 子工作流补充 `on.workflow_call` 参数声明和 `ksuver`、`ak3name` 输出映射。
- 兼容修复：将子工作流中的 `github.event.inputs.*` 全部改为 `inputs.*`，使手动运行和批量复用调用使用同一套输入上下文。
- 影响文件：远程仓库 `.github/workflows/fastbuild_6.6.30.yml`、`fastbuild_6.6.50.yml`、`fastbuild_6.6.56.yml`、`fastbuild_6.6.57.yml`、`fastbuild_6.6.66.yml`、`fastbuild_6.6.89.yml`、`fastbuild_6.6.89_mtk.yml`。
- 验证：7 个远程 Raw 文件 HTTP 200；均存在 `workflow_call`，不再存在 `github.event.inputs.*`；GitHub Actions API 已列出批量工作流且状态为 active；`git diff --check` 通过。
- 遇到的问题和解决办法：推送时远程 `main` 已有新提交，先同步远程的缓存键/CVE 更新，再将本修复变基后推送，未覆盖远程历史。
- 提交：`dbd593ec626967dfeef4e46acfc4832920da0a79`。
- AGENTS.md：未修改。
- GitHub 备份状态：已上传 GitHub。

## 2026-08-20 修复 ZIP 工件重名

- 修改内容：为 7 个 6.6 fastbuild 子工作流生成的 ZIP 文件名加入 `KERNEL_VERSION.SUB_VERSION`，使 6.6.30、6.6.50、6.6.56、6.6.57、6.6.66、6.6.89 和 6.6.89_mtk 的工件名称唯一。
- 问题原因：7 个工件名称都为 `AnyKernel3_ReSukiSU_35081_6.6_AoGou.zip`，汇总任务使用 `download-artifact@v8` 时只找到 1 个，导致“期望 7 个 ZIP，实际找到 1 个”。
- 影响文件：远程仓库 7 个 `.github/workflows/fastbuild_6.6*.yml` 子工作流。
- 验证：修复前回归检查按预期发现 7 个模板缺少 `SUB_VERSION`；修复后 7 个远程 Raw 文件 HTTP 200，每个包含 2 个带 `SUB_VERSION` 的 ZIP 名称模板；`git diff --check` 通过。
- 提交：`789348203a627b3e40ec13b41d25917671e005e0`。
- AGENTS.md：未修改。
- GitHub 备份状态：已上传 GitHub。


## 2026-10-11 19:50:00 同步上游并重新构建

- 上游新增 2 个提交：4eec634（补丁匹配容错）、0d90ea4（ReSukiSU 更名 BakaSU）；使用普通合并保留 fork 历史。
- 影响：18 个上游/批量工作流与 local 构建脚本，新增 AGENTS.md 和 tests/validate_workflows.py。
- 合并七个子工作流冲突时保留 workflow_call、inputs、输出映射及 KERNEL_VERSION.SUB_VERSION 唯一 ZIP 名称；保留 89_mtk 和七版本清单。
- 批量入口改用 bakasu，并兼容 BakaSU_CI 最新 Release 暂不可用时从 ReSukiSU_CI 获取真实管理器 APK。未修改七版本源码/平台映射。
- 构建参数沿用最近成功的运行 32291308644：susfs/LZ4 开启，KPM/LZ4KD/ADIOS/基带保护/Re-Kernel/网络增强关闭，BBR/Droidspaces false，ccache 更新/调试关闭，后缀 AoGou；仅 KSU 分支跟随上游改为 bakasu。
- 结果快照：各改动文件保存为 versions/<文件名>-20261011-195000-upstream-sync.<扩展名>。
- 验证：7 个父子接口、输出、版本/89_mtk 和唯一命名检查通过；163 段 Bash 经 bash -n 通过；git diff --check 通过；当前文件与 Git 历史敏感信息模式扫描通过；管理器回退逻辑实测可用，真实 APK 为 ReSukiSU_v4.2.0-rc3_35203-arm64-v8a-release.apk。
- 坑点：不能只改显示名称而保留旧输入参数；新 CI 地址尚未提供 Release 时不能让内核汇总发布失败。长期规则已写入本仓库 AGENTS.md，不修改 6.1 项目。
- GitHub 备份/构建状态：将随同步提交推送至已授权的公开 fork main；本轮 Actions 的真实构建和发布结果待补充。
