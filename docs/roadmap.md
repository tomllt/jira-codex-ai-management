# 路线图

## 第一阶段：分析沉淀

目标：把 Jira + Codex 协同方案沉淀为文档与结构化规范。

输出：

- 整体定位
- 工作流设计
- MVP 规格
- 数据模型
- Skill 与架构草图

## 第二阶段：最小自动化

目标：实现最基本的自动建单与 Sprint 消费能力。

建议范围：

- 从 Epic 生成 Story / Task 的结构化结果
- 自动创建 Jira Story / Task
- 按 JQL 拉取 Sprint 中 `Ready for Codex` 的任务
- 回写执行 comment 和状态

## 第三阶段：工程化接入

目标：将文档规格转成可运行系统。

建议范围：

- 增加 `schemas/` 管理 JSON Schema
- 增加 `prompts/` 管理需求分析和任务执行模板
- 增加 `scripts/` 实现 Jira API 与 Orchestrator
- 增加示例输入输出与测试样例

## 第四阶段：治理增强

目标：提升可靠性、可审计性与管理赋能深度。

建议范围：

- 增加权限分层
- 增加任务领取锁机制
- 增加阻塞分类统计
- 增加 Sprint 健康检查
- 增加 AI 建议采纳率和执行成功率指标
