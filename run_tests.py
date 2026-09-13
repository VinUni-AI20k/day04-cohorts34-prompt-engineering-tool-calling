"""
run_tests.py — Task 4: 5 câu test chứng minh KHI NÀO agent trả lời trực tiếp,
KHI NÀO gọi tool.

Bộ test bám sát "System Prompt Testing Checklist":
  - Happy path (gọi đúng tool)
  - Tool decision (khi nào tool vs khi nào direct)
  - Edge case (thiếu thông tin bắt buộc -> hỏi lại, không tool)
  - Out of scope (từ chối đúng cách, không tool)

Mỗi câu có `expect_tool` (kỳ vọng) để tự động kiểm tra hành vi tool-decision.
"""

from __future__ import annotations

from agent import run_agent
from llm import get_model

# (câu hỏi, tool kỳ vọng hoặc None nếu kỳ vọng trả lời trực tiếp, ghi chú)
TEST_CASES = [
    ("Thời tiết Hà Nội hôm nay thế nào?",
     "get_weather",
     "Happy path — API wrapper: đủ thông tin (thành phố) -> GỌI TOOL."),

    ("Doanh thu miền Bắc tháng này bao nhiêu?",
     "query_sales",
     "Happy path — data query: có khu vực -> GỌI TOOL."),

    ("Xin chào, bạn là ai?",
     None,
     "Conditional/direct: chào hỏi -> TRẢ LỜI TRỰC TIẾP, không tool."),

    ("Cho tôi xem thời tiết đi.",
     None,
     "Edge case: hỏi thời tiết nhưng THIẾU thành phố -> hỏi lại, KHÔNG tool."),

    ("Bạn nghĩ giá bitcoin ngày mai thế nào?",
     None,
     "Out of scope: lời khuyên tài chính -> TỪ CHỐI trực tiếp, không tool."),
]


def main() -> None:
    model = get_model()  # mặc định MockModel; đặt LAB_MODEL=gemini để dùng model thật
    passed = 0
    summary = []

    for i, (question, expected_tool, note) in enumerate(TEST_CASES, 1):
        print(f"\n########## TEST {i}: {note}")
        trace = run_agent(question, model=model)

        actual_tool = trace.tool_calls[0] if trace.called_tool else None
        ok = actual_tool == expected_tool
        passed += ok

        exp = expected_tool or "DIRECT (không tool)"
        act = actual_tool or "DIRECT (không tool)"
        print(f"{'-'*70}")
        print(f"  Kỳ vọng: {exp:32}  Thực tế: {act:32}  {'✅ PASS' if ok else '❌ FAIL'}")
        summary.append((i, exp, act, ok))

    print(f"\n{'='*70}")
    print(f"KẾT QUẢ: {passed}/{len(TEST_CASES)} test PASS")
    print(f"{'='*70}")
    print(f"{'#':<3}{'Kỳ vọng':<34}{'Thực tế':<34}{'':<6}")
    for i, exp, act, ok in summary:
        print(f"{i:<3}{exp:<34}{act:<34}{'PASS' if ok else 'FAIL'}")
    print("\nGhi chú: 2 câu GỌI TOOL (mỗi tool 1 câu), 3 câu TRẢ LỜI TRỰC TIẾP")
    print("(chào hỏi / thiếu thông tin / ngoài phạm vi). Đúng như thiết kế policy.")


if __name__ == "__main__":
    main()
