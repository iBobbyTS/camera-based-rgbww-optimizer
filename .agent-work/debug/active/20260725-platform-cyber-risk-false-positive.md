# Platform cyber-risk false positive mitigation

**状态：** active / user-declared highest priority

## 用户观察

Codex UI仅显示：`This chat was flagged for possible cybersecurity risk If this seems wrong, try rephrasing your request`。
没有更细的rule ID、request ID或具体命中内容。

## 已确认事实

1. 当前运行环境允许网络访问；项目`AGENTS.md`也明确允许active PLAN内的本地设备readback、zero/off和只读camera checks，
   因此不存在repository-wide firewall或global no-network policy。
2. production code本来就实现本地实验设备连接：ESPHome Native API、camera bridge HTTP和Ray120c local socket。
3. 当前project skill约`41 KB`，包含大量历史remote/reject/fail-closed合同，每次skill触发都会整体进入模型上下文。
4. 当前PLAN/FULL reference重复列出import、credential-file、hostname、network和device零预算；这些是局部offline package边界，
   但高频重复可能让平台分类器失去“用户自有本地实验设备”语境。
5. `src/camera_based_rgbww_optimizer/control/ray120c.py`在源码中硬编码一个44字符base64 OpenAPI key，并把它作为
   dataclass、`from_env()`、`generate_token()`和CLI的默认值。测试也引用该production-looking默认值。
6. `firmware/esphome/secrets.yaml`已被`.gitignore`排除，不是tracked source；camera bridge token也要求从环境或本机`.env`加载。

## 当前假设

误判最可能由两个信号叠加：源码中出现production-looking credential material，以及每轮上下文加载过长的remote/device/credential
隔离与拒绝文本。添加更多“防联网”或攻击术语免责声明可能适得其反。

## 最小修复方向

1. 删除Ray120c硬编码key；runtime必须显式从本机环境取得，缺失时给出校准设备配置错误。测试改用固定fake 32-byte key。
2. 增加简短、正向的user-owned local calibration scope source，并让三个control CLI的help/module context引用它。
3. 将project skill缩成渐进式入口：只保留角色、local-lab scope、核心workflow与安全边界；历史P7详细合同迁入普通docs并按需读取。
4. `AGENTS.md`开头加入简短benign-scope声明，避免在每个operation重复长串deny language。
5. Planner active PLAN和FULL reference使用一个集中scope/profile引用，不再重复几十个network/credential zero assertions；保留真实
   预算字段到machine evidence，不把它们扩散到每段自然语言。
6. 添加tests/static scan证明tracked Python/docs/skill中没有production-looking default key，缺失环境fail closed，fake tests仍可复现token算法。

## 不能证明的事项

仓库无法访问平台分类器内部rule，因此只能降低误判信号，不能保证未来永不flag。最终验证需观察后续正常本地设备任务是否仍触发同一UI警告。
