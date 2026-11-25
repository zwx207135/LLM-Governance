"""Verify the delivered pilot, including XLSX/CSV equality, without model inference."""
import csv
import json
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.prepare_c_pilot_review import FOLDER, validate_rows
from src.utils.experiment_io import sha256_file, stable_hash

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def xlsx_rows(archive, name):
    shared = []
    if "xl/sharedStrings.xml" in archive.namelist():
        shared = ["".join(x.itertext()) for x in ET.fromstring(archive.read("xl/sharedStrings.xml")).findall("m:si", NS)]
    rows = []
    for node in ET.fromstring(archive.read(name)).findall(".//m:sheetData/m:row", NS):
        row = [""] * 17
        for cell in node.findall("m:c", NS):
            col = 0
            for char in cell.attrib["r"]:
                if not char.isalpha():
                    break
                col = col * 26 + ord(char) - 64
            value = cell.find("m:v", NS)
            typ = cell.attrib.get("t")
            if typ == "s":
                text = shared[int(value.text)]
            elif typ == "inlineStr":
                text = "".join(t.text or "" for t in cell.findall(".//m:t", NS))
            else:
                text = "" if value is None else value.text or ""
            if col <= 17:
                row[col - 1] = text
        rows.append(row)
    return rows


def check(folder=FOLDER):
    p = json.loads((folder / "draft_payload.json").read_text(encoding="utf-8"))
    with (folder / "pilot_annotations_D_original.csv").open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        original = list(reader)
        fields = reader.fieldnames
    with (folder / "pilot_annotations_C_AI_draft.csv").open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        draft = list(reader)
        if reader.fieldnames != fields:
            raise ValueError("Pilot columns changed")
    if original != p["original"] or draft != p["draft"] or fields != p["fields"]:
        raise ValueError("Delivered CSV differs from authored payload")
    validate_rows(original, draft, p["notes"])
    provenance = p["provenance"]
    if sha256_file(folder / "pilot_annotations_D_original.csv") != provenance["input_sha256"]:
        raise ValueError("Source snapshot hash mismatch")
    if provenance["human_review_completed"] or provenance["label_schema_status"] != "proposed_pending_C_D_confirmation":
        raise ValueError("Draft cannot certify independent human completion")
    ids = {s["id"] for s in p["sources"]}
    evidence = json.loads((folder / "evidence_notes.json").read_text(encoding="utf-8"))
    if evidence != {"provenance": provenance, "by_id": p["notes"], "sources": p["sources"]}:
        raise ValueError("Separate evidence ledger differs")
    for row in original:
        note = p["notes"][row["id"]]
        if not note["human_review_required"] or not set(note["source_ids"]) <= ids:
            raise ValueError("Missing review flag or source ID")
        if stable_hash({"question": row["question"], "answer": row["answer"]}) != note["question_answer_sha256"]:
            raise ValueError("Evidence belongs to a different question/answer")
    with zipfile.ZipFile(folder / "pilot_annotations_C_AI_draft.xlsx") as archive:
        for number, rows in ((1, draft), (3, original)):
            expected = [fields] + [[r[k] for k in fields] for r in rows]
            if xlsx_rows(archive, f"xl/worksheets/sheet{number}.xml") != expected:
                raise ValueError("XLSX values differ from CSV, including source text")
    return {"passed": True, "rows": 25, "columns": 17, "original_bytes_verified": True,
            "xlsx_csv_and_evidence_verified": True, "ai_assisted_judgments": 25,
            "independent_human_judgments": 0, "adjudications": 0, "formal_accuracy": None,
            "unknown_entity_truth_not_assumed": True, "model_inference_calls": 0}


if __name__ == "__main__":
    result = check()
    (FOLDER / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
