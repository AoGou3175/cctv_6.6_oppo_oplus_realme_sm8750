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


## 2026-10-11 20:01:02 本轮真实构建失败与管理器安全检查

- 上游同步提交 0a3d8d52a25e6a40c94b73545c5e738c5d6923fb 已推送并核对远程 main；fork 相对上游为 ahead 5 / behind 0。
- 新运行：https://github.com/AoGou3175/cctv_6.6_oppo_oplus_realme_sm8750/actions/runs/38137105017；七个 build job 均编译失败，七个子 Release 与汇总 Release 均跳过，没有发布本轮资产。
- 根因证据：6.6.30 与 6.6.89_mtk 日志都在 KernelSU/kernel/tools/susfs_compat.mk:20 报 Please wait susfs update。BakaSU 提交 48fa4bb7ec8bddb8ea932a8c9be0877f89a1fa73（2026-10-10）主动增加 SUSFS 构建中止；Kbuild 仅在 CONFIG_KSU_SUSFS 模式包含此文件。禁止删除保护来伪造构建成功。
- 管理器进一步核验：2026-10-05 提交 97c102ba05ee2915390cacae6d11e1727d6ca350 更改包名并移除旧管理器支持；旧 CI 最新 APK 是 10 月 4 日源码 8770c7e324a22895703c4916b8a16520e0b81c79 对应的 ReSukiSU_35203，不能当作最新 BakaSU 管理器使用。
- 精准修复：批量发布的 BakaSU APK 筛选要求 BakaSU_ 前缀和 arm64-v8a-release.apk 后缀，不再静默附带旧管理器；AGENTS.md 增加上游保护及管理器兼容性规则。
- 快照：versions/build-test_6.6_kpm-20261011-200102-manager-compat.yml、versions/AGENTS-20261011-200102-susfs-guard.md；本地外层 versions 同步保存。
- 验证：修改前实测旧 CI 仅提供旧管理器；修改后实际运行工作流资产筛选，结果为空，正确拒绝不兼容 APK；源文件 git diff --check 通过。首次结果快照保留源文件原有空白，单独用 SHA-256 验证 20 个快照字节一致，不清理上游无关格式。
- 当前需要用户选择：保留 SUSFS 并固定 10 月 4 日兼容源码（缺少后续更新）、最新 BakaSU 关闭 SUSFS并另配新版管理器，或等待 SUSFS 适配。未擅自改变 susfs 功能、删除上游保护或回退源码。
- GitHub 备份状态：同步代码和首次快照已上传；本条构建失败记录、管理器安全检查和新快照随后提交推送 main。尚无本轮成功构建，不声明任务构建成功。


## 2026-10-11 20:12:43 遵循最新 BakaSU 规则重新构建

- 用户明确选择最新 BakaSU 规则：关闭 SUSFS，不回退源码，不删除 susfs_compat.mk 保护；KPM 和其他参数仍沿用上次实际运行（KPM false、LZ4 true、后缀 AoGou）。
- 修改八个工作流：父入口和七个子入口默认关闭 SUSFS，七个子流程采用 KSU_TRACEPOINT_HOOK；保留 89_mtk、14 个原有用户参数和唯一 ZIP 名称。
- 批量 prepare 记录运行开始时最新 BakaSU main SHA，内部传递 ksu_ref，七版本 checkout 后检查实际 SHA，版本号按 HEAD 计算；汇总校验七份源码 SHA 相同并在 Release 写明来源。
- 官方管理器来自 Baka-SU/BakaSU 的 Build Manager，筛选 main、push、success、同源码 SHA 的 Manager-release 工件。跨仓库下载无权限时仅保留官方来源链接，不用旧/PR/DEV/Spoofed APK；本次若需要，由已授权 gh 登录补齐同提交官方 APK。
- 目前源码 SHA 59afa46b325126b12a48234063cd0c2a6b735b57，官方运行 38134360191；APK BakaSU_v4.2.0-rc3_35226-arm64-v8a-release.apk，大小 9687368，SHA-256 14e03f3bb727352234bceeb9fa72087932e8792f92e7ba6e8de9ee52b222350d。
- 更正前条管理器推断：aapt2 实测此官方新版 APK 包名仍为 com.resukisu.resukisu，显示名 BakaSU；apksigner 验证 v2 签名有效，证书 SHA-256 d3469712b6214462764a1d8d3e5cbe1d6819a0b629791b9f4101867821f1df64 与同提交 manager_sign.h 完全一致。不能仅依据重命名提交推断实际包名或签名兼容性。
- 验证：修改前校验按预期发现默认启用 SUSFS；修改后错误参数返回 1、关闭 SUSFS 返回 0；七版本输入/输出/源码接口、165 段 Bash 语法通过；源码解析及官方同提交运行查询实测通过；git diff --check 和敏感信息模式扫描通过。快照保留源文件已有空白，按 SHA-256 验证一致。
- AGENTS.md 已更新本轮长期规则，tests/validate_workflows.py 补充参数拒绝和内部接口验证。
- 本地结果快照完整路径：
- D:/Codex/构建GKI/CCTV6.6/versions/build-test_6.6_kpm-20261011-201243-bakasu-latest.yml
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.30-20261011-201243-bakasu-latest.yml
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.50-20261011-201243-bakasu-latest.yml
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.56-20261011-201243-bakasu-latest.yml
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.57-20261011-201243-bakasu-latest.yml
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.66-20261011-201243-bakasu-latest.yml
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.89-20261011-201243-bakasu-latest.yml
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.89_mtk-20261011-201243-bakasu-latest.yml
- D:/Codex/构建GKI/CCTV6.6/versions/AGENTS-20261011-201243-bakasu-latest.md
- D:/Codex/构建GKI/CCTV6.6/versions/validate_workflows-20261011-201243-bakasu-latest.py
- 同名快照也保存在 Git 仓库根目录 repo/versions/，本条与代码随提交上传 main；本轮真实 Actions 和 Release 结果待完成后追加，不提前声称构建通过。


## 2026-10-11 20:25:00 最新 BakaSU 七版本构建与发布验证完成

- 构建代码提交：49ccdd75374de3a2271b47a8cc2d848f1b4d3257，main 已推送并核对 GitHub 回读。
- 真实运行：https://github.com/AoGou3175/cctv_6.6_oppo_oplus_realme_sm8750/actions/runs/38138527278；16 个 job 全部 success，包括准备、七个 build、七个子 Release 和统一发布。
- 统一 Release：https://github.com/AoGou3175/cctv_6.6_oppo_oplus_realme_sm8750/releases/tag/OPPO-OPlus-Realme-build-all-261011202212-38138527278；7 个唯一命名 ZIP（30、50、56、57、66、89、89_mtk）和 1 个官方 arm64 管理器 APK，未漏传 MTK。
- 汇总日志验证七份 KSU SHA 全部为 59afa46b325126b12a48234063cd0c2a6b735b57；BakaSU 35226，SUSFS false、KPM false、LZ4 true、后缀 AoGou。
- 本次跨仓库 GITHUB_TOKEN 实际下载 Manager-release 成功，官方管理器自动随统一 Release 上传，不需要人工补传。前述 gh 补传仅是权限失败时的备用方法。
- 从 Release 下载到 D:/Personal/Temp/gki-final-38138527278，七 ZIP CRC 全部通过，含 Image、anykernel.sh、tools/ak3-core.sh；Image ARM64 魔数有效（大小约 36.6–37.6 MB），ZIP 注释包含本轮 Run ID、代码提交、35226 及功能开关。
- 8 个资产的本地大小和 SHA-256 全部与 GitHub API digest 一致；APK 与同源码官方工件一致（14e03f3bb727352234bceeb9fa72087932e8792f92e7ba6e8de9ee52b222350d），apksigner 签名验证通过，证书与 manager_sign.h 一致。
- 检查脚本最初误假设 APK 原生库名 libksu.so，实际官方 APK 使用 libkernelsu.so 和 libksud.so；根据真实内容修正临时检查后通过，未改动交付 APK。不能凭经验硬编码不确定的文件名来判定资产损坏。
- 最终静态检查：七版本接口和唯一命名、165 段 Bash 语法通过，git diff --check 通过；Release 中文、标签、源码及资产回读正常。
- 本轮工作流、测试、AGENTS.md 和 10 个结果快照已上传提交 49ccdd7；快照路径见上一条记录。本条仅补充验证结果，不对 CHANGELOG 自身生成递归快照；仓库内记录随后正常提交推送 main，本地外层记录同步保留。
- 未进行手机刷写、开机或 Root/模块实机验证；未发现新的工作流构建故障，没有修改设备分区、仓库可见性或 fork 关系。


## 2026-10-12 08:52:39 修复并行子 Release 标签撞名

- 问题运行 38188659698：七个 build 成功，6.6.57 子 Release 报 HTTP 422 / Release.tag_name already exists，最终汇总跳过；七 ZIP 工件均保留。
- 根因：6.6.50 与 6.6.57 在 08:43:23 同秒生成 OPPO-OPlus-Realme-build-261012084323，标签只包含秒级时间；6.6.50 先占用标签。不是 BakaSU、内核源码或 ZIP 命名问题。
- 修改七个批量子工作流的一行 gh release create 标签表达式，加入完整 KERNEL_VERSION.SUB_VERSION、github.run_id、github.run_attempt，保留原时间、标题、说明及所有构建选项；不修改非本批次 6.6.118。
- 验证器运行真实标签表达式，固定同一秒，覆盖七版本 × 两运行 × 三次尝试 = 42 个标签。修改前按预期失败，修改后全部唯一；七版本接口、唯一 ZIP 和 165 段 Bash 语法通过。
- AGENTS.md 追加并行发布标签唯一性规则，tests/validate_workflows.py 加入回归验证。九个文件的结果快照如下；repo/versions 保存同名副本，快照与当前文件内容一致，工作流原 CRLF 保留且 SHA-256 字节一致。
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.30-20261012-085239-release-tag-unique.yml
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.50-20261012-085239-release-tag-unique.yml
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.56-20261012-085239-release-tag-unique.yml
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.57-20261012-085239-release-tag-unique.yml
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.66-20261012-085239-release-tag-unique.yml
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.89-20261012-085239-release-tag-unique.yml
- D:/Codex/构建GKI/CCTV6.6/versions/fastbuild_6.6.89_mtk-20261012-085239-release-tag-unique.yml
- D:/Codex/构建GKI/CCTV6.6/versions/AGENTS-20261012-085239-release-tag-unique.md
- D:/Codex/构建GKI/CCTV6.6/versions/validate_workflows-20261012-085239-release-tag-unique.py
- git diff --check 与敏感信息模式扫描通过；没有删除或覆盖既有 Release、资产、标签、历史、旧运行或快照。
- GitHub 备份状态：本轮代码、测试、AGENTS、快照与记录随后按用户要求上传已授权的公开 fork main；真实验证从最新 main 新建运行，参数沿用本次失败运行，结果完成后追加。旧运行补跑仍使用旧提交，不能作为新代码验证。
