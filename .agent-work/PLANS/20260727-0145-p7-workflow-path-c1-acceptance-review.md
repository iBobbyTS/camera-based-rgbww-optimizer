# Planner 验收归档：REF-P7-04 WORKFLOW-PATH-C1

**审查日期：** 2026-07-27 01:45

## 证据与决定

- commit `0c878cbf3c7d94dadef2a64446c08ba01931a0d2`，共 5 files；十路径
  manifest SHA `8f9189edfb1520be2e08913678d7e046b93cb0a3c42a0034331e16b39d982e94`。
- isolated cleanup pre/post `5/5`；同根因第六测试在 test scope 使用同一合法 fake key；
  TD-B `72/72`、control/cleanup `59/59`、full `562/562`（新增一个 adversarial test）。
- compileall、wrappers、`git diff --check`、CodeGraph 均通过。
- qualification/replay/candidate/release/device/network/.env/setup/formal/camera/Ray 均为 `0`。

接受十路径 exact manifest、credential test isolation 与 commit。禁止把成功解释为 filename-only
allowlist。当前 commit 另修改两个尚无 exact lineage provenance 的 test paths：
`tests/test_measure_chart_response_basis.py` 与 `tests/test_measure_raw_shutter_response.py`。
它们只包含 test-owned fake Ray key 注入，但仍须先冻结 exact old/current/diff hashes、scope、
commit provenance 与 rollback；在此之前不运行 qualification。

