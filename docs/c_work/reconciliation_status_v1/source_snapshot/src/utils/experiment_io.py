"""Immutable run contracts and a durable, resumable result ledger."""
import hashlib
import json
import os
from pathlib import Path


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def atomic_json(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def record_key(row):
    return str(row["id"]), row["mode"]


def read_records(path, repair_tail=False):
    path = Path(path)
    if not path.exists():
        return []
    raw = path.read_bytes()
    lines = raw.splitlines(keepends=True)
    records, valid_bytes = [], 0
    for index, line in enumerate(lines):
        try:
            row = json.loads(line)
            if not isinstance(row, dict) or not {"id", "mode", "status"}.issubset(row):
                raise ValueError("Record fields missing")
        except (ValueError, UnicodeDecodeError) as exc:
            # Recover only a torn final append, never a corrupt complete/interior record.
            torn_tail = index == len(lines) - 1 and not line.endswith(b"\n")
            if not repair_tail or not torn_tail:
                raise ValueError(f"Corrupt record at line {index + 1}") from exc
            backup = path.with_name(path.name + ".torn-" + hashlib.sha256(raw).hexdigest()[:12] + ".bak")
            if not backup.exists():
                backup.write_bytes(raw)
            with path.open("r+b") as stream:
                stream.truncate(valid_bytes)
            return records
        records.append(row)
        valid_bytes += len(line)
    if repair_tail and raw and not raw.endswith(b"\n"):
        with path.open("ab") as stream:
            stream.write(b"\n")
    return records


def latest_records(rows):
    latest = {}
    for row in rows:
        key = record_key(row)
        if key in latest and row.get("attempt", 1) <= latest[key].get("attempt", 1):
            raise ValueError(f"Duplicate/non-increasing attempt: {key}")
        latest[key] = row
    return latest


class RunLedger:
    def __init__(self, directory, contract, planned, resume=False):
        self.directory = Path(directory)
        self.path = self.directory / "records.jsonl"
        self.manifest_path = self.directory / "manifest.json"
        self.planned = planned
        if len(planned) != len(set(planned)):
            raise ValueError("Duplicate planned records")
        if resume:
            self.manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
            if self.manifest["contract_sha256"] != stable_hash(contract):
                raise ValueError("Resume refused: data, corpus, code, configuration or model changed")
            if [tuple(x) for x in self.manifest["planned_records"]] != planned:
                raise ValueError("Resume plan differs")
            self.latest = latest_records(read_records(self.path, repair_tail=True))
            if set(self.latest) - set(planned):
                raise ValueError("Unexpected record identity")
        else:
            self.directory.mkdir(parents=True, exist_ok=False)
            self.latest = {}
            self.manifest = {"schema_version": 2, "stage": "development_only", "contract": contract,
                             "contract_sha256": stable_hash(contract), "planned_records": planned,
                             "status": "created", "segments": []}
        self.save()

    def save(self):
        self.manifest["counts"] = {"planned": len(self.planned),
                                   "ok": sum(r["status"] == "ok" for r in self.latest.values()),
                                   "prepared": sum(r["status"] == "prepared" for r in self.latest.values()),
                                   "errors": sum(r["status"] == "error" for r in self.latest.values()),
                                   "missing": len(self.planned) - len(self.latest)}
        atomic_json(self.manifest_path, self.manifest)

    def pending(self, retry_errors=False):
        return [key for key in self.planned if key not in self.latest or
                (retry_errors and self.latest[key]["status"] == "error")]

    def append(self, row):
        key = record_key(row)
        if key not in set(self.planned):
            raise ValueError("Record not in run plan")
        if row["status"] not in ("ok", "prepared", "error"):
            raise ValueError("Invalid record status")
        row = {**row, "attempt": self.latest.get(key, {}).get("attempt", 0) + 1}
        with self.path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        self.latest[key] = row
        self.save()
