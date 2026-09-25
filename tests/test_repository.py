# SPDX-FileCopyrightText: 2026 <ThanlnDat>
#
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

from src.loader import nap_vao_db
from src.models import make_session
from src.repository import HistoricalRepairRepository


def test_chi_nap_dung_loai_san_pham(tmp_path):
    """File mẫu có 6 dòng nhưng chỉ 4 dòng thuộc aircon/fan/dehumidifier."""
    session = make_session(str(tmp_path / "test.db"))
    so_ban_ghi = nap_vao_db(session, Path("tests/mau.csv"), "checksum-test")
    assert so_ban_ghi == 4
    assert HistoricalRepairRepository(session).count() == 4


def test_search_by_note_chi_tra_ban_ghi_khop(tmp_path):
    session = make_session(str(tmp_path / "test.db"))
    nap_vao_db(session, Path("tests/mau.csv"), "checksum-test")
    ket_qua = HistoricalRepairRepository(session).search_by_note("quạt")
    assert len(ket_qua) == 2
    for ban_ghi in ket_qua:
        assert "quạt" in ban_ghi.historical_case_note


def test_count_by_outcome_cong_lai_bang_count(tmp_path):
    session = make_session(str(tmp_path / "test.db"))
    nap_vao_db(session, Path("tests/mau.csv"), "checksum-test")
    repo = HistoricalRepairRepository(session)
    assert sum(repo.count_by_outcome().values()) == repo.count()