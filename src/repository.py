# SPDX-FileCopyrightText: 2026 <ThanlnDat>
#
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import HistoricalRepairCase


class Repository(ABC):
    """Lớp nền. Mọi repository đều nhận session và có ít nhất get() với count()."""

    def __init__(self, session: Session) -> None:
        self.session = session

    @abstractmethod
    def get(self, record_id: int): ...

    @abstractmethod
    def count(self) -> int: ...


class HistoricalRepairRepository(Repository):
    def get(self, record_id: int) -> HistoricalRepairCase | None:
        return self.session.get(HistoricalRepairCase, record_id)

    def count(self) -> int:
        return self.session.scalar(
            select(func.count()).select_from(HistoricalRepairCase)
        ) or 0

    def search_by_note(self, keyword: str, limit: int = 20) -> list[HistoricalRepairCase]:
        """Trả về các bản ghi có mô tả lỗi chứa từ khóa."""
        return self.session.scalar(
            select(HistoricalRepairCase).where(HistoricalRepairCase.c.historical_case_note.icontains(keyword)).limit(limit)
        )

    def count_by_outcome(self) -> dict[str, int]:
        """Đếm số bản ghi theo kết quả sửa chữa.

        Kết quả mong đợi trông giống: {"Fixed": 2030, "End of life": 1261, ...}
        """
        rows = self.session.execute(
            select(HistoricalRepairCase.historical_outcome, func.count())
            .group_by(HistoricalRepairCase.historical_outcome)
        ).all()
        return {str(ket_qua): int(so_luong) for ket_qua, so_luong in rows}