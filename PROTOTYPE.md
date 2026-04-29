# Prototype assets

## Schemas

- `schemas/ai-plan.schema.json`
- `schemas/execution-result.schema.json`

## Prompts

- `prompts/epic_to_plan.prompt.md`
- `prompts/task_execution.prompt.md`

## Examples

- `examples/sample-ai-plan.json`
- `examples/sample-execution-result.json`
- `examples/sample-jira-comment.md`

## Scripts

- `scripts/orchestrator.py`

## Notes

当前脚本为原型骨架，主要用于固定接口、目录和数据契约。
下一步可以继续补：

- 真实 Jira API client
- 真实 Codex CLI runner
- JSON schema 校验
- `.env` 配置加载
- JQL 模板与 comment 生成器
