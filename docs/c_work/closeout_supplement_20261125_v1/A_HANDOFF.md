# C交给A的真实检索导出

导出文件[a_evidence_export.json](a_evidence_export.json)对应A当前提交中的12条开发题和36条正常任务，每个UID都有真实检索结果、知识库版本/哈希、参数、问题哈希及无命中状态。输入副本和来源提交见[a_handoff_manifest.json](a_handoff_manifest.json)。

当前固定配置下48条全部无命中，因此chunks均为空。空数组是真实覆盖结果，不代表已完成有效证据注入或证明RAG有收益；不以参考答案填补片段。正式联合实验应先共同确认输入和知识库范围。

A输入快照中的4条旧UID在B数据中已更名，显式映射为age的A-D01→AGE-D01、anchoring的A-D01→AN-D01、occupation的A-D01→OCC-D01、region_culture的A-D01→RC-D01。本导出保留A实际输入的旧UID，避免与现有历史输出错配；后续正式输入切换时另建版本，不能覆盖旧记录。

```powershell
# 在A负责的检出版本中使用；输出目录必须新建
python experiments/run_a.py --input datasets/a/pilot_dev.json --configs configs/a/formal_matrix_TEMPLATE.json --evidence path/to/a_evidence_export.json --output results/a/new_development_run
```

上例只是交接入口，formal_matrix_TEMPLATE仍是模板，不能当作已签收冻结协议；本轮没有执行该生成命令。先核对12条开发输入与导出中的问题哈希，正常任务应使用对应输入文件。

已通过A函数的48条无命中消息传递检查及1条有命中探针检查，生成函数为明确标识的测试夹具，实际模型调用为0。探针验证字段和片段能进入A消息，不属于正式数据、模型回答或联合效果验证。A的联合实现未改动。正式C3交接/联合复核仍等待双方冻结输入和实际生成检查。
