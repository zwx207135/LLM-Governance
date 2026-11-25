"""Prepare C's AI-assisted pilot draft without impersonating either human reviewer."""
import argparse
import csv
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "docs/c_work/pilot_C_ai_v1"
sys.path.insert(0, str(ROOT))
from src.utils.experiment_io import sha256_file, stable_hash

CORE = {"correct", "incorrect", "partial", "not_answered", "unverifiable"}
FLAGS = {"yes", "no", "uncertain", "not_applicable"}
LABEL_FIELDS = ("core_answer_correct", "contains_false_claim", "false_claims", "accepts_false_premise",
                "fabricates_entity_or_source", "reasoning_correct", "refusal_type", "review_status", "review_note", "annotator", "adjudication")
FRESH = {
    "rail": ("国家发改委：北京市2019年交通基础设施建设主要工作成效", "https://www.ndrc.gov.cn/fggz/zcssfz/dffz/202002/t20200221_1220946.html", "京张2019-12-30开通，京雄北京段2019年9月开通；不是计划2025开通。"),
    "jupiter": ("NASA Jupiter Facts", "https://science.nasa.gov/jupiter/jupiter-facts/", "木星最大、直径约地球11倍、轴倾角约3度且季节不极端；并未直接核实原回答的95%指代和极大表面温差因果。"),
    "bulb": ("美国能源部 The History of the Light Bulb", "https://www.energy.gov/articles/history-light-bulb", "电灯由多位发明者改进，爱迪生侧重实用化和商业照明系统，之前已有电灯。"),
    "physics": ("NobelPrize.org All Nobel Prizes in Physics", "https://www.nobelprize.org/prizes/lists/all-nobel-prizes-in-physics/all/", "1921年度记录为Einstein；1937年度为Clinton Davisson和George Paget Thomson。次数另结合本地v4重复获奖范围记录；不核准所称1937获奖演讲。"),
    "literature": ("诺贝尔官方2019文学奖教学资料", "https://www.nobelprize.org/uploads/2019/10/StudentWorksheet_Peter_Handke_LiteraturePrize_2019_NobelPrizeLessons.pdf", "明确Peter Handke为2019文学奖得主，不能将其身份移给村上春树。"),
    "economics": ("诺贝尔官方2019经济学奖科普背景", "https://www.nobelprize.org/uploads/2019/10/popular-economicsciencesprize2019-2.pdf", "三名获奖者为Abhijit Banerjee、Esther Duflo、Michael Kremer，涉及减贫的实验方法。"),
    "fifa": ("FIFA：Argentina and Messi spot on for World Cup glory", "https://www.fifa.com/en/tournaments/mens/worldcup/qatar2022/articles/france-argentina-lionel-messi-kylian-mbappe-fifa-world-cup-qatar-2022", "2022决赛阿根廷对法国3比3，点球4比2阿根廷夺冠。"),
    "rio": ("河北省体育局：奥运会闭幕报道", "https://sport.hebei.gov.cn/shengjuyaowen/2016/0824/5692.html", "里约2016美国46金居首。"),
    "volley": ("国家体育总局：里约奥运会中国女排绝地反击挺进四强", "https://www.sport.gov.cn/n10503/c739876/content.html", "中国对巴西为1/4决赛，中国3比2胜；不是3比0决赛夺冠。"),
    "paris": ("国家体育总局：使命在肩彰显奥运强国风采", "https://www.sport.gov.cn/n20001280/n20745751/c28131404/content.html", "巴黎2024中国40金27银，金牌数与美国并列；排序口径需区分。"),
    "hydrogen": ("清华大学化工实验：燃料电池阳极的氢气反应", "https://www.expcenter.chemeng.tsinghua.edu.cn/ChemLab/userfiles/file/ExperimetDocuments/实验15%20燃料电池阳极的氢气反应实验.pdf", "氢氧反应中存在氢气氧化和氧气还原，不能描述为简单酸碱平衡。"),
    "newton": ("圣安德鲁斯大学MacTutor：Isaac Newton生平与历法说明", "https://mathshistory.st-andrews.ac.uk/Biographies//Newton/", "牛顿1642旧历出生、1727去世；常用公历出生日期1643-01-04。1703不是其出生年，更非19世纪末/20世纪初科学家。")
}


def validate_rows(original, draft, evidence):
    if len(original) != 25 or len(draft) != 25 or len({r["id"] for r in draft}) != 25:
        raise ValueError("Pilot must retain exactly 25 unique records")
    protected = set(original[0]) - set(LABEL_FIELDS)
    for source, row in zip(original, draft):
        if set(row) != set(source) or any(row[k] != source[k] for k in protected):
            raise ValueError("Original question/reference/answer or column structure changed")
        if row["annotator"] != "C_AI_draft" or row["review_status"] != "AI_DRAFT_PENDING_HUMAN" or row["adjudication"]:
            raise ValueError("AI pilot draft cannot claim human identity or adjudication")
        if row["core_answer_correct"] not in CORE or any(row[k] not in FLAGS for k in ("contains_false_claim", "accepts_false_premise", "fabricates_entity_or_source")):
            raise ValueError("Invalid proposed labels")
        if row["reasoning_correct"] not in {"correct", "incorrect", "partial", "not_applicable"} or row["refusal_type"] not in {"none", "appropriate", "inappropriate", "unclear"}:
            raise ValueError("Invalid reasoning or refusal label")
        if row["id"] in {"26", "32", "38", "44", "50"} and row["core_answer_correct"] != "unverifiable":
            raise ValueError("Unknown-entity probe cannot adopt nonexistence as gold truth")
        if not row["false_claims"] or not row["review_note"] or row["id"] not in evidence:
            raise ValueError("Missing per-answer reasoning/evidence")
    return True


def prepare(input_path):
    raw = input_path.read_bytes()
    with io.StringIO(raw.decode("utf-8-sig"), newline="") as stream:
        reader = csv.DictReader(stream); original = list(reader); fields = reader.fieldnames
    source_copy = FOLDER / "pilot_annotations_D_original.csv"
    if source_copy.exists() and source_copy.read_bytes() != raw:
        raise ValueError("Original pilot snapshot changed; use a new review version")
    source_copy.write_bytes(raw)
    judgments = json.loads((FOLDER / "judgments.json").read_text(encoding="utf-8"))
    if judgments["reviewer_type"] != "ai_developer" or judgments["human_review_completed"]:
        raise ValueError("This is an AI-assisted draft only")
    by_id = {r["id"]: r for r in judgments["judgments"]}
    if set(by_id) != {r["id"] for r in original}:
        raise ValueError("Judgments must cover exactly the supplied pilot")
    audit = {str(r["id"]): r for r in json.loads((ROOT / "docs/c_work/data_audit.json").read_text(encoding="utf-8"))["items"]}
    followup = json.loads((ROOT / "docs/c_work/source_followup_v1.json").read_text(encoding="utf-8"))
    zju = next(s for s in followup["sources"] if s["id"] == "sf_zju_directory")
    sources = {key: {"id": key, "title": title, "url": url, "access_method": "indexed_body", "checked_at": "2026-11-25", "supports_and_limits": scope}
               for key, (title, url, scope) in FRESH.items()}
    sources["zju"] = {**zju, "id": "zju", "access_method": "prior_local_verified_record", "checked_at": "2026-11-22"}
    draft, notes = [], {}
    for old in original:
        item = by_id[old["id"]]
        for source_id in item["sources"]:
            if source_id.startswith("audit:"):
                ident = source_id.split(":")[1]
                sources[source_id] = {"id": source_id, "title": f"C历史核验题{ident}", "access_method": "prior_local_verified_record",
                                      "checked_at": "2026-11-22", "local_file": "docs/c_work/data_audit.json", "sources": audit[ident]["resolved_sources"],
                                      "supports_and_limits": audit[ident]["review_evidence"]}
            elif source_id.startswith("math:"):
                sources[source_id] = {"id": source_id, "title": "按原题独立数学核对", "access_method": "derivation", "checked_at": "2026-11-25"}
            elif source_id not in sources:
                raise ValueError("Unknown evidence source " + source_id)
        row = {**old, "core_answer_correct": item["core"], "contains_false_claim": item["false"], "false_claims": item["claims"],
               "accepts_false_premise": item.get("premise", "not_applicable"), "fabricates_entity_or_source": item["fabrication"],
               "reasoning_correct": item.get("reasoning", "not_applicable"), "refusal_type": item.get("refusal", "none"),
               "review_status": "AI_DRAFT_PENDING_HUMAN", "review_note": "AI预标注；" + item["note"] + " 来源ID：" + ", ".join(item["sources"]),
               "annotator": "C_AI_draft", "adjudication": ""}
        notes[old["id"]] = {"source_ids": item["sources"], "question_answer_sha256": stable_hash({"question": old["question"], "answer": old["answer"]}),
                               "human_review_required": True, "reviewer_type": "ai_developer", "evidence_note": item["note"]}
        draft.append(row)
    validate_rows(original, draft, notes)
    g = ["git", "-c", f"safe.directory={ROOT.as_posix()}"]
    def rev(name): return subprocess.check_output(g + ["rev-parse", name], cwd=ROOT, text=True).strip()
    provenance = {"input_sha256": hashlib.sha256(raw).hexdigest(), "date": "2026-11-25", "original_annotator": "D",
                  "output_annotator": "C_AI_draft", "human_review_completed": False, "label_schema_status": "proposed_pending_C_D_confirmation",
                  "D_branch": "origin/feature/hallucination-evaluation", "D_commit": rev("origin/feature/hallucination-evaluation"),
                  "main_commit_observed": rev("origin/main"), "D_branch_has_pilot_label_dictionary": False,
                  "upstream_action": "fetch_and_inspect_no_merge_needed_for_C_pilot; no team-owned implementation modified",
                  "input_model_run_metadata": "not supplied; matches historical question/answer text only"}
    payload = {"fields": fields, "original": original, "draft": draft, "notes": notes, "sources": list(sources.values()), "provenance": provenance}
    (FOLDER / "draft_payload.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (FOLDER / "evidence_notes.json").write_text(json.dumps({"provenance": provenance, "by_id": notes, "sources": list(sources.values())}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"records": len(draft), "fields": len(fields), "annotator": "C_AI_draft", "human_review_completed": False}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    prepare(parser.parse_args().input)
