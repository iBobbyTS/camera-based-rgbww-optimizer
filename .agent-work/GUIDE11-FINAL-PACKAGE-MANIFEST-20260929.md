# GUIDE11 最终交付包清单（2026-09-29）

包：`GUIDE11-FINAL-PACKAGE-20260929.zip`（本文件旁，不入 git）。
内容边界：仅处理后数据（结果文档、派生 JSON、分析/构建脚本）。
**不含**原始 CR3/RAW/DNG、NPY/NPZ、TIFF/JPEG/PNG 衍生、解码数组、固件、
构建产物、凭据。原始载荷按运行根保留于 `D:\rgbww-optimizer\` 各实验目录。

## 文件清单（路径 · 字节数 · SHA-256）

见同目录机器可读 `GUIDE11-FINAL-PACKAGE-MANIFEST-20260929.json`
（由打包脚本生成，逐文件含 byte_count 与 sha256）。

## 包内目录结构

- `results/` —— .agent-work 下全部 GUIDE11 结果文档与最终报告
- `derived/` —— 各阶段冻结分析 JSON（repo tmp 副本）
- `scripts/` —— 冻结分析器与覆盖图构建脚本（repo tmp）
