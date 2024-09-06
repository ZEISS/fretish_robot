# SPDX-FileCopyrightText: Copyright 2023–2024 Carl Zeiss Meditec AG
# SPDX-License-Identifier: Apache-2.0

import dataclasses
import json


@dataclasses.dataclass
class FRETRequirement:
    req_id: str
    requirement_phrase: str
    scope_mode: str | None
    trigger_event: str | None
    timing: str
    condition_to_check: str
    variables: list[str]


def _transform_to_fret_req(req: dict) -> FRETRequirement:
    req_id = req["reqid"]
    fulltext = req["fulltext"]
    semantics = req["semantics"]

    if scopeTextRange := semantics.get("scopeTextRange", None):
        scope_mode = semantics["scope_mode"]
    else:
        scope_mode = None

    pre_condition = semantics.get("regular_condition_unexp_pt", None)

    timing_start, timing_end = semantics["timingTextRange"]
    timing_end += 1  # for timing, FRET end is inclusive...
    timing = fulltext[timing_start:timing_end]

    condition_to_check = semantics["post_condition_unexp_ft"]

    variables = semantics["variables"]

    fret_req = FRETRequirement(
        req_id=req_id,
        requirement_phrase=fulltext,
        scope_mode=scope_mode,
        trigger_event=pre_condition,
        timing=timing,
        condition_to_check=condition_to_check,
        variables=variables,
    )

    return fret_req


def load_fret_requirements(fret_json_input_filepath: str) -> list[FRETRequirement]:
    with open(fret_json_input_filepath, "r") as fret_json_file:
        requirement_dicts = json.load(fret_json_file)

    result = [
        _transform_to_fret_req(req) for req in requirement_dicts if req["semantics"]
    ]

    return result
