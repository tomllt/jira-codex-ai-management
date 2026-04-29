[Codex Execution Update]

Status: Human Review

Summary
- 已实现支付回调幂等校验
- 已补充重复回调测试

Files Touched
- src/payment/callback_handler.py
- tests/payment/test_callback_handler.py

Validation
- pytest tests/payment -q ✅

Risks / Notes
- 依赖事件ID唯一性假设

Next Step
- 请人工 review 并决定是否合并
