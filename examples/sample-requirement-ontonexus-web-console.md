目标：为 OntoNexus web-console 增加一轮更明确的导航配置测试治理。

背景：
- 当前 web-console 已有 App.test.tsx 和 shellNavigation.ts
- 我们希望 AI 能先从需求描述生成 Story/Task 草案，再落到 Jira
- 任务需要尽量小，便于后续 prepare-task 和 run-task 消费

约束：
- 优先只针对 apps/web-console
- 不要修改业务页面逻辑
- 优先补测试和配置一致性校验
- 需要给出明确 test command

期望：
- 生成 1 个故事
- 生成 1~2 个小任务
- 任务要包含 repo/workdir/module_scope/test_command
