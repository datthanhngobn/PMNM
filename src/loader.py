# SPDX-FileCopyrightText: 2026 <ThanlnDat>
#
# SPDX-License-Identifier: Apache-2.0

import sqlite3
import csv
import hashlib
from pathlib import Path

import httpx

from .models import HistoricalRepairCase

SOURCE_URL = "<https://raw.githubusercontent.com/openrepair/data/refs/heads/master/aggregated/202507/OpenRepairData_v0.3_aggregate_202507.csv>"
LICENSE = "CC-BY-SA-4.0"
DATASET = "open-repair-alliance"
TRANSFORM = "ords-map-v1"

# Tạo database bằng sqlite
database = sqlite3.connect("historical_repair_case.db")
database.execute("""CREATE TABLE history_repair_case(
external_reference TEXT,
asset_category TEXT,
asset_brand TEXT,
asset_age_years FLOAT,
country TEXT,
historical_repair_date TEXT,
historical_case_note TEXT,
historical_outcome TEXT,
repair_barrier TEXT);""")

# Mapping attribute
mapping = {
    "id" : "external_reference",
    "product_category" : "asset_category",
    "brand" : "asset_brand",
    "product_age" : "asset_age_years",
    "country" : "country",
    "event_date" : "historical_repair_date",
    "problem" : "historical_case_note",
    "repair_status" : "historical_outcome",
    "repair_barrier_if_end_of_life" : "repair_barrier"
}

csv_key = list(mapping.keys())
db_attribute = list(mapping.values())

db_attribute = ", ".join(csv_key)
str_values = ""

for i in range(len(csv_key)) :
    str_values += "?, "

query_insert_values = f"INSERT INTO database ({db_attribute} VALUES({str_values}))"



# Chỉ nạp những loại sản phẩm này
TU_KHOA_CAN_LAY = ("aircon", "dehumidifier", "fan")


def tai_file(url: str, dest: Path) -> Path:
    """Tải file về. Nếu đã có sẵn thì không tải lại."""
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    with httpx.stream("GET", url, follow_redirects=True, timeout=300) as r:
        r.raise_for_status()
        with dest.open("wb") as f:
            for chunk in r.iter_bytes(1024 * 1024):
                f.write(chunk)
    return dest


def tinh_checksum(path: Path) -> str:
    """Mã sha256 của file — dùng để chứng minh file không bị đổi."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def nap_vao_db(session, path: Path, checksum: str) -> int:
    """Đọc CSV, lọc, tạo object, lưu vào database. Trả về số bản ghi đã nạp."""

    so_ban_ghi = 0
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        data_add = []
        for row in reader:
            if row["product_category"].lower() in TU_KHOA_CAN_LAY :
                values = tuple(row[key] for key in csv_key)
                data_add.append(values)
                so_ban_ghi += 1

    database.executemany(query_insert_values, data_add)
    session.commit()
    return so_ban_ghi
