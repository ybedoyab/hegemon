from __future__ import annotations


def per_task_seconds(task_count: int, total_seconds: int, reserve_seconds: int, setup_seconds_each: int) -> int:
    """Leave a reserve and a setup allowance, then split the rest across tasks."""
    if task_count < 1:
        raise ValueError("task_count must be positive")
    available = total_seconds - reserve_seconds - (setup_seconds_each * task_count)
    if available <= 0:
        return 30
    return max(30, available // task_count)


def should_stop_early(
    *,
    has_verified_patch: bool,
    attempts: int,
    remaining_tool_calls: int,
    repeated: bool,
) -> bool:
    if remaining_tool_calls <= 1:
        return True
    if has_verified_patch and remaining_tool_calls <= 3:
        return True
    if repeated and attempts >= 2:
        return True
    if attempts >= 3 and not has_verified_patch and remaining_tool_calls <= 4:
        return True
    return False
