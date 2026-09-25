# SPDX-FileCopyrightText: 2026 <ThanlnDat>
#
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

from .loader import SOURCE_URL, nap_vao_db, tai_file, tinh_checksum
from .models import make_session
from .repository import HistoricalRepairRepository

if __name__ == "__main__":
    session = make_session()
    path = tai_file(SOURCE_URL, Path("data/raw/openrepair.csv"))
    checksum = tinh_checksum(path)
    so_ban_ghi = nap_vao_db(session, path, checksum)

    repo = HistoricalRepairRepository(session)
    print(f"Đã nạp {so_ban_ghi} bản ghi")
    print(f"Tổng trong database: {repo.count()}")
    print(f"Checksum: {checksum}")
    print("Đếm theo kết quả sửa chữa:")
    for ket_qua, so_luong in repo.count_by_outcome().items():
        print(f"  {ket_qua}: {so_luong}")