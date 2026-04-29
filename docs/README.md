# 文档索引

## 核心文档

- `overview.md`：项目定位、目标、能力边界
- `workflow.md`：端到端流程与职责划分
- `mvp-spec.md`：MVP 详细规格
- `data-models.md`：字段、模板、JSON 结构
- `skills-architecture.md`：Skill、Orchestrator、Codex CLI 的关系与接口
- `implementation.md`：当前原型实现方式与使用命令
- `roadmap.md`：后续分阶段落地建议
- `2026-04-28-refactor-implementation-plan.md`：原型重构实施计划

## 推荐阅读顺序

1. `overview.md`
2. `workflow.md`
3. `mvp-spec.md`
4. `data-models.md`
5. `skills-architecture.md`
6. `implementation.md`
7. `roadmap.md`

## 已补 Prototype 目录

- `../schemas/`：结构化输出契约
- `../prompts/`：Epic 规划与 Task 执行 prompt
- `../examples/`：示例 JSON 和 Jira comment
- `../scripts/`：原型脚本骨架
- `../PROTOTYPE.md`：原型资产说明

## 目录约定

- 项目根目录是唯一入口，不再保留嵌套的同名历史目录。
- `2026-04-28-refactor-implementation-plan.md` 已归档到 `docs/` 正式文档目录。
- `__pycache__/`、`*.pyc`、`.pytest_cache/`、`.env` 视为运行时或本地文件，由 `.gitignore` 忽略。

## 下一步实现建议

- 增加 Jira API client 的 issue 创建能力扩展
- 增加 Codex CLI runner
- 增加 schema 校验
- 增加配置与环境变量管理细化
