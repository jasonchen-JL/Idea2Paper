from __future__ import annotations

from typing import Any, Dict, List, Optional

CARD_VERSION = "blind_card_v1"


def _stable_string(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        parts = []
        for key in sorted(value.keys()):
            parts.append(f"{key}:{_stable_string(value[key])}")
        return " ".join(parts)
    if isinstance(value, (list, tuple)):
        return " ".join(_stable_string(v) for v in value)
    return str(value)


def _to_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return _stable_string(value)
    return str(value)


def _clean_text(text: str, max_len: int = 800) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = text.strip().replace("\n", " ")
    if len(text) > max_len:
        return text[:max_len].rstrip() + "…"
    return text


def build_story_card(story: Dict[str, Any]) -> Dict[str, Any]:
    problem = story.get("problem_framing") or story.get("problem_definition") or ""
    method = story.get("method_skeleton", "")
    contrib = story.get("innovation_claims", story.get("claims", ""))
    experiments = story.get("experiments_plan", "")
    domain = story.get("domain", "")
    sub_domains = story.get("sub_domains", "")
    application = story.get("application", "")

    notes: List[str] = []
    if not problem:
        notes.append("problem:missing")
    if not method:
        notes.append("method:missing")
    if not contrib:
        notes.append("contrib:missing")
    if not experiments:
        notes.append("experiments_plan:missing")

    return {
        "problem": _clean_text(_to_str(problem)),
        "method": _clean_text(_to_str(method)),
        "contrib": _clean_text(_to_str(contrib)),
        "experiments_plan": _clean_text(_to_str(experiments)),
        "domain": _clean_text(_to_str(domain)),
        "sub_domains": _clean_text(_to_str(sub_domains)),
        "application": _clean_text(_to_str(application)),
        "notes": notes,
        "card_version": CARD_VERSION,
    }


def build_paper_card(paper: Dict[str, Any], review_summary: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    pattern_details = paper.get("pattern_details", {}) or {}
    problem = pattern_details.get("base_problem", "")
    method = pattern_details.get("solution_pattern", "")
    story = pattern_details.get("story", "")
    idea = paper.get("idea", "")
    contrib = ""
    if review_summary:
        contrib = review_summary.get("contribution") or review_summary.get("strengths") or ""
    if not contrib:
        contrib = " ".join([_to_str(idea), _to_str(story)]).strip()
    experiments = review_summary.get("experiments_plan") if review_summary else ""
    experiments = experiments or "unknown"
    domain = paper.get("domain", "")
    sub_domains = paper.get("sub_domains", "")
    application = pattern_details.get("application", "")

    notes: List[str] = []
    if not problem:
        notes.append("problem:missing")
    if not method:
        notes.append("method:missing")
    if not contrib:
        notes.append("contrib:missing")
    if experiments == "unknown":
        notes.append("experiments_plan:unknown")

    return {
        "problem": _clean_text(_to_str(problem)),
        "method": _clean_text(_to_str(method)),
        "contrib": _clean_text(_to_str(contrib)),
        "experiments_plan": _clean_text(_to_str(experiments)),
        "domain": _clean_text(_to_str(domain)),
        "sub_domains": _clean_text(_to_str(sub_domains)),
        "application": _clean_text(_to_str(application)),
        "notes": notes,
        "card_version": CARD_VERSION,
    }
