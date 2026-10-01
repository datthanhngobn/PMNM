# SPDX-FileCopyrightText: 2026 <ThanlnDat>
#
# SPDX-License-Identifier: Apache-2.0

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class HistoricalRepairCase(Base):
    __tablename__ = "historical_repair_case"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # ----- dữ liệu lấy từ file CSV -----
    external_reference: Mapped[str] = mapped_column(String(120), unique=True)
    asset_category: Mapped[str] = mapped_column(String(80))
    asset_brand: Mapped[str | None] = mapped_column(String(120))
    asset_age_years: Mapped[float | None] = mapped_column(Float)
    country: Mapped[str | None] = mapped_column(String(8))
    historical_repair_date: Mapped[str | None] = mapped_column(String(12))
    historical_case_note: Mapped[str | None] = mapped_column(Text)
    historical_outcome: Mapped[str | None] = mapped_column(String(40))
    repair_barrier: Mapped[str | None] = mapped_column(String(80))

    # ----- 6 cột dưới đây BẮT BUỘC, giữ đúng tên, đừng đổi -----
    source_dataset: Mapped[str] = mapped_column(String(80))
    source_url: Mapped[str] = mapped_column(String(400))
    source_license: Mapped[str] = mapped_column(String(40))
    source_checksum: Mapped[str] = mapped_column(String(80))
    transformation_version: Mapped[str] = mapped_column(String(40))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=UTC)
    )


def make_session(db_path: str = "data.db"):
    engine = create_engine(f"sqlite+pysqlite:///{db_path}")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()