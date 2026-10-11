# CCTV 6.6 构建维护规则

- 保留七版本批量入口 `.github/workflows/build-test_6.6_kpm.yml`，6.6.89_mtk 是独立的 MT6991 版本，不得漏传或与 6.6.89 合并。
- 6.6.50、6.6.89_mtk 使用 MT6991，其余本批次版本使用 SM8750；保留 Release 中的实际源码/平台对应表、中文安装方法和风险提示。
- 通过普通 merge 同步 `cctv18/oppo_oplus_realme_sm8750` 的 main，禁止强制覆盖历史。同步时必须保留 workflow_call、inputs 上下文、ksuver/ak3name 输出映射和唯一 ZIP 命名。
- 自 2026-10 上游迁移为 BakaSU，6.6 的 ksu_type 使用 bakasu、sukisu、ksunext、ksu、none；父入口、子入口、源码配置和 Release 分支应同时更新。不要因此修改其他项目的 resukisu 参数。
- 新版 BakaSU 管理器优先使用 Baka-SU/BakaSU 官方 Build Manager 的 main 分支 push 成功运行，选择与本次源码 SHA 相同的 Manager-release 中 arm64-v8a-release.apk，不使用 PR、DEV 或 Spoofed 变体。不要假设 cctv18/BakaSU_CI 一定存在，不把旧文件改名伪装新版。
- 名称迁移不能直接证明包名或签名改变。应使用 aapt2 和 apksigner 检查实际 APK，并将证书 SHA-256 与同提交的 kernel/manager/manager_sign.h 核对。当前官方 35226 APK 显示名 BakaSU，包名实际仍为 com.resukisu.resukisu；此前仅据改名提交推断旧管理器必然不兼容的结论不够准确，不沿用该推断。
- 上游若通过 susfs_compat.mk 主动禁止 SUSFS 构建，不删除或绕过保护；说明原因后由用户选择固定兼容源码、关闭 SUSFS 或等待适配。锁定旧源码会缺少后续更新，必须在 Release 明示实际 SHA 和日期，不声称使用最新 KSU。
- 用户已选择遵循最新 BakaSU 规则：批量和七个子入口默认关闭 SUSFS，使用 KSU_TRACEPOINT_HOOK；启用 SUSFS 时尽早拒绝。批量先读取当次最新 main SHA，七版本使用同一 SHA，统计版本号基于 HEAD 并在 Release 明示 SHA。
- 下载跨仓库官方工件需要验证实际权限；若 GITHUB_TOKEN 无法取得 APK，保留官方下载来源并发布完整内核包，不附带不匹配 APK。本次交付由已授权的 gh 登录补充同提交官方 APK，并回读资产哈希。
- 每个子工作流同时支持 workflow_dispatch 和 workflow_call。输入名称、类型与父入口一致，内部使用 inputs.xxx。
- ZIP 名称必须含 KERNEL_VERSION.SUB_VERSION，确保 6.6.89 与 6.6.89_mtk 不重名。汇总 Release 等待全部成功，并校验七个 ZIP 后再发布；none 模式不要求 APK。
- 用户要求重新构建时优先沿用最近一次成功运行的实际参数，而非仅按工作流默认值；需要改变功能开关时明确说明。
- 工作流修改后运行 `python tests/validate_workflows.py`（依赖 PyYAML、Git Bash 或 bash），检查父子接口、输出、版本、ZIP 命名和 Bash 语法，并执行 git diff --check。
- 静态检查不等于构建成功。推送后核对远程 SHA 和关键工作流，再从最新 main 启动新运行，检查构建、工件校验及最终 Release 资产；不要用旧运行的重新运行代替新代码验证。
- 结果快照放在根目录 versions/，CHANGELOG.md 仅追加。UTF-8 Markdown/YAML，Shell 保持 LF；不改无关文件。
- 不提交 Token、密码、私钥或 Cookie；使用 GitHub Secrets。此仓库为用户已授权的 public fork，不改变可见性或 fork 关系。仅在用户明确要求同步/上传时提交推送。
