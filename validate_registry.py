#!/usr/bin/env python3
"""Structural validation for the normalized fNIRS dataset registry."""

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent

registry_fields = [
    "dataset_key",
    "source",
    "source_version",
    "title",
    "description",
    "population",
    "n_subjects",
    "modalities",
    "paradigm",
    "format",
    "size",
    "license",
    "access_url",
    "access_method",
    "metadata_status",
    "notes",
    "evidence_url",
    "task_description",
    "n_recordings",
    "recording_count_basis",
    "fnirs_format",
    "count_status",
    "fnirs_duration_min_s",
    "fnirs_duration_max_s",
    "duration_basis",
    "duration_status",
    "features_labels_events",
    "features_behavior",
    "features_demographics",
    "features_clinical",
    "features_questionnaires",
    "features_physiology",
    "features_motion",
    "features_spatial_optode_metadata",
    "features_stimuli",
    "features_other_modalities",
    "features_other",
]
count_statuses = {"verified", "partial", "metadata-warning", "unavailable"}
duration_statuses = {"verified", "partial", "unavailable"}
feature_statuses = {"verified", "partial", "metadata-warning"}
feature_columns = [field for field in registry_fields if field.startswith("features_")]


def read_csv(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


registry_header, registry = read_csv("public/registry.csv")

assert registry_header == registry_fields, registry_header
assert len(registry) == 48, len(registry)
assert len({row["dataset_key"] for row in registry}) == len(registry)
assert all(None not in row for row in registry)
assert all(value == value.strip() for row in registry for value in row.values())
assert all(row["task_description"] for row in registry)
assert all(row["recording_count_basis"] for row in registry)
assert all(row["fnirs_format"] for row in registry)
assert {row["count_status"] for row in registry} <= count_statuses
assert {row["duration_status"] for row in registry} <= duration_statuses
assert all(row["duration_basis"] for row in registry)
assert all(
    (row["n_recordings"].isdigit() and int(row["n_recordings"]) > 0)
    or (row["n_recordings"] == "0" and row["count_status"] == "metadata-warning")
    or (not row["n_recordings"] and row["count_status"] == "unavailable")
    for row in registry
)
assert all(
    not value or re.fullmatch(r"\d+(?:\.\d+)?", value)
    for row in registry
    for value in (row["fnirs_duration_min_s"], row["fnirs_duration_max_s"])
)
assert all(
    (
        row["duration_status"] == "unavailable"
        and not row["fnirs_duration_min_s"]
        and not row["fnirs_duration_max_s"]
    )
    or (
        row["duration_status"] == "partial"
        and bool(row["fnirs_duration_min_s"] or row["fnirs_duration_max_s"])
    )
    or (
        row["duration_status"] == "verified"
        and bool(row["fnirs_duration_min_s"])
        and bool(row["fnirs_duration_max_s"])
        and float(row["fnirs_duration_min_s"]) <= float(row["fnirs_duration_max_s"])
    )
    for row in registry
)
assert all(
    re.match(r"^https://", row[field])
    for row in registry
    for field in ("access_url", "evidence_url")
)

assert all(
    row["features_labels_events"]
    for row in registry
)
feature_cells = [row[field] for row in registry for field in feature_columns if row[field]]
assert all(
    " || format=" in cell
    and " || level=" in cell
    and " || status=" in cell
    and " || evidence=" in cell
    for cell in feature_cells
)
assert all(
    re.search(r"\|\| status=([^|]+)", cell).group(1).strip() in feature_statuses
    for cell in feature_cells
)

readme = (ROOT / "README.md").read_text(encoding="utf-8").splitlines()
table_start = next(i for i, line in enumerate(readme) if line.startswith("| Dataset |"))
table_end = next(i for i in range(table_start + 2, len(readme)) if not readme[i].startswith("|"))
body = readme[table_start + 2 : table_end]
assert len(body) == len(registry), len(body)
assert all(line.count("|") == 11 for line in body)
for line, row in zip(body, registry):
    symbol = {"verified": "✓", "partial": "~", "metadata-warning": "!", "unavailable": "—"}[
        row["count_status"]
    ]
    expected = f"{row['n_recordings']} {symbol}" if row["n_recordings"] else "—"
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    assert cells[4] == expected, (row["dataset_key"], cells[4], expected)

print(f"registry.csv: {len(registry)} rows, {len(registry_header)} columns")
print("count statuses:", dict(sorted(Counter(row["count_status"] for row in registry).items())))
print("duration statuses:", dict(sorted(Counter(row["duration_status"] for row in registry).items())))
print(
    "feature columns:",
    {field: sum(bool(row[field]) for row in registry) for field in feature_columns},
)
print(f"README: {len(body)} rows aligned with registry.csv")
