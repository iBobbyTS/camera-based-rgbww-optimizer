# P7-TD-B Z0-R2-C1R3 lifecycle bootstrap 首失败验收归档

**归档时间：** 2026-07-25 16:39 MDT

**Reference task ID：** REF-P7-01

**Reviewed PLAN contract：** P7-TD-B-Z0-R2-C1R3

**Reviewed PLAN SHA-256：** be6132704eaa85e2c37fc8c40068d7085e4955cf283becda019e4f81ffd726fe

**Planner decision：** `accepted_first_five_matrices_47_of_47; rejected_completion_at_lifecycle_bootstrap; c1r4_required`

**Exact next branch：** P7-TD-B-Z0-R2-C1R4；仅在新 package driver启动前预建空的regular non-symlink顶层 `cases/` directory，frozen lifecycle owner byte/AST-exact不改。

## Reviewed scope 与执行方法

C1R3 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r2-c1r3-offline/20260725T223419Z/`

Executor exact验证 C1R2 artifacts，机械同步 C1R3 contract bookkeeping，保持 frozen PLAN parser和所有核心owner；完成 compile/syntax、source delta与PLAN identity gate后启动driver一次。driver顺序完成前五矩阵，在 lifecycle 首case artifact创建前 fail closed；没有补目录或重跑。

## Evidence 与 validation quality

- `pre-device-failure.json`：bytes `2386`，SHA-256 `c8bff75374f297695f979f395e75b6aaec0ecd98a2e2baf3bc4679c437424739`。
- `validation-summary.json`：bytes `632`，SHA-256 `cc8724da3194b515d9f3ad9b703341b091dff1acc7b2aa554e443df99a98592e`。
- `source/harness.py`：bytes `81654`，SHA-256 `b7162111a9a907fde8cbf10cab01ca4fb64a8ec60430e7cb6f8e8570740d777b`。
- `source/run_wrapper.zsh`：bytes `1671`，SHA-256 `890caf867a4f5630c52bd59b8c7d078daf0f59cd75dfc7b32c79879fe93354e6`。
- `source/real_adapter.py`：bytes `4240`，SHA-256 `c2bc28683a1e789f1945164471f6693f48c79dd3c6dcdb1b7e36d1f0e37fc186`。
- `launcher.zsh`：bytes `289`，SHA-256 `75c589929e08e00043591b683c128e86d30cc60f566caec4a2d5ec5472068dbc`。

有效局部矩阵：evidence tree `6/6`，SHA `f6783173aa8635ee62e7cf9f0e4d1be85ff7b715d150e0c78e858c443d7376d0`；wrapper copy `10/10`，SHA `f7564554054039df98ce230d74436ab9e3a54cd9208783adb9a69ace82b1a946`；secrets identity `7/7`，SHA `cd31d7a66484f0348e5f22fb9c0f14239c4b4174c70ce3d102658a705e8816f2`；source hygiene `10/10`，SHA `da269c0df82b584ea93a4193f6d65654c4f21400195e211732bbf00d5d9a3a68`；PLAN identity `14/14`，SHA `fd979b4c62bc0d3f690ed25540dfaf2e6d768d119844d4a8359978837362f93f`。合计 `47/47`。package现有 `79/79` JSON strict parse通过。

## Finding、decision 与 residual risk

首次失败为 lifecycle owner执行 `case_root.mkdir()` 时 parent `cases/` 不存在，抛出 `FileNotFoundError`。frozen owner故意只创建单case目录而不隐式创建parent；fresh package bootstrap漏建顶层父目录。lifecycle case started=`0`，real-adapter matrix、old-root after replay与terminal seal均未启动。

前五矩阵接受为局部证据，但完整package仍失败，两个既有review findings未关闭。C1R4只补 package bootstrap parent directory；不得给 lifecycle owner增加 `parents=True`、`exist_ok=True`或任何fallback，也不得把47/47当作跳过新package前五矩阵的授权。

PLAN marker/parser、C1R2 artifacts、secrets/launcher、production/scientific owners均通过并冻结。secrets/.env/credentials、production import、hostname、network、device、camera、Ray、strip、Z0、lineage、E2、formal、Git操作均为0；workspace与无关工作保持。
