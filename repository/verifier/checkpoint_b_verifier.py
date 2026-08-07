#!/usr/bin/env python3
"""Exact verifier V3 for the frozen Checkpoint B module and suite evidence package.

This verifier is non-governing. It re-derives every Checkpoint B identity from
governing inputs and rejects any state that does not match exactly. It never
mutates the governed repository, the frozen Checkpoint B source archive, the
accepted Checkpoint A archive, the accepted N1 archive, or the Authorization 003
archive. Mutation experiments belong to the test harness and operate only on
temporary copies.

V2 corrects the five defects raised in independent review of V1:

D1  The round-trip transition is exposed as ordered stages, so corruption
    introduced after the first valid extraction reaches the transition branch
    rather than the earlier extracted-identity branch.
D2  Package accounting is derived entirely from observed archive and manifest
    state. No accounting result is produced from compiled constants alone.
D3  The environment fingerprint checks every recorded comparability field, and
    environment variables distinguish unset from set-empty from set-nonempty.
D4  Module and suite evidence is derived semantically from the raw JUnit XML and
    the parsed JSON summaries are cross-checked against it. Causal assertions
    must be derivable from the failing test case's own failure element.
D5  Every census record's node identifiers are bound to its function locator by
    module path, base function name and parametrized suffix, so swapping node
    identifier arrays between functions fails even when the global identifier
    set, the bucket totals and the function totals are unchanged.

V3 applies two narrow corrections raised in independent review of V2:

F1  Manifest self-inclusion is verified as three independent branches covering
    presence, type and value. An absent, null, string or integer declaration is
    never reduced through bool() into an explicit false, so absence fails closed.
F2  The exported archive stores verification/checkpoint_b_verifier.py as a
    regular file with Unix mode 0755, and the stored entry metadata is verified
    directly rather than inferred from the pre-archive filesystem mode.

Twelve subcommands are implemented. Each emits one deterministic JSON object on
stdout carrying the keys subcommand, decision, checks, errors and exit_code. A
failed check yields a nonzero exit code. An unrecognised subcommand fails closed
with exit code 2 and still emits the same JSON shape.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import types
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

# ---------------------------------------------------------------------------
# Governing constants. Every value below is an exact accepted identity.
# ---------------------------------------------------------------------------

DOWNLOADS = Path("/Users/arkadiymiteiko/Downloads")

# The accepted Checkpoint B, Checkpoint A and N1 archives were relocated by the
# owner into a dated folder after the V2 export. Their identities are unchanged
# and are still asserted below; only the resolved directory differs.
ACCEPTED_ARCHIVE_DIRECTORY = DOWNLOADS / "6:8:26"

DEFAULT_SOURCE_ZIP = ACCEPTED_ARCHIVE_DIRECTORY / (
    "oam-cdc-profile-correction-stage-b0-n2a-1-m1-s0-revision-002-"
    "checkpoint-b-module-suite-001.zip"
)
DEFAULT_CHECKPOINT_A_ZIP = ACCEPTED_ARCHIVE_DIRECTORY / (
    "oam-cdc-profile-correction-stage-b0-n2a-1-m1-s0-revision-002-"
    "checkpoint-a-packaging-revision-002.zip"
)
DEFAULT_N1_ZIP = ACCEPTED_ARCHIVE_DIRECTORY / (
    "oam-cdc-profile-correction-stage-b0-n1-artifact-index-freeze-revision-004.zip"
)
DEFAULT_AUTHORIZATION_ZIP = (
    DOWNLOADS
    / "files"
    / (
        "oam-gate-sar-05-cdc-profile-correction-authorization-003-"
        "owner-review-revision-002.zip"
    )
)
DEFAULT_REPOSITORY = Path("/Users/arkadiymiteiko/oam-cdc-wo007-clean")
DEFAULT_PYTHON = Path(
    "/Users/arkadiymiteiko/oam-cdc-reference-publication-candidate/.venv/bin/python"
)

SOURCE_ZIP_BYTES = 60119
SOURCE_ZIP_SHA256 = "e838e305a1bc2544e065353f128020764f8553330c77a4184a7260986d6d7887"
SOURCE_ZIP_SHA512 = (
    "194606cfba9bcbea3ab96c6975b1a2bd5b40f59680b6a54bd48aafbcc98cbb6a"
    "81e9e5819d5234c1bb0c924a0c4e60cc7849ff04b0c17a63274c848211a99e30"
)

CHECKPOINT_A_ZIP_BYTES = 22412
CHECKPOINT_A_ZIP_SHA256 = (
    "28160a1a17d22bd0e7eef57d73411505d93e4854ffc3cf6cb271e5e09df27014"
)

N1_ZIP_BYTES = 41311
N1_ZIP_SHA256 = "7bd4eec589cf9e81cb347a96fd0d148fa7a5a84cedaeff1e8cc619cd4595b035"

AUTHORIZATION_MEMBER = (
    "OAM-GATE-SAR-05-CDC-PROFILE-CORRECTION-AUTHORIZATION-003-"
    "PREFLIGHT-REVISION-002.json"
)
AUTHORIZATION_MEMBER_BYTES = 21864
AUTHORIZATION_MEMBER_SHA256 = (
    "9b8db6de93093b006e25146427b1291addeec9fbf7a65ee2763baa031e78a746"
)

ACCEPTED_HEAD = "9b1754040c3dafa0123c6b13ea9e5f5eaa2b7bd1"
ACCEPTED_TREE = "8d898a5d69164db1d4d64e08fb7b71facf459e8b"
ACCEPTED_REFS = 1

# Frozen Checkpoint B payload members consumed by this verifier.
DOC_COMPARABILITY = "02-M1-S0-CHECKPOINT-B-COORDINATE-ENVIRONMENT-COMPARABILITY.json"
DOC_MODULE = "03-M1-S0-MODULE-EVIDENCE.json"
DOC_SUITE = "04-M1-S0-SUITE-EVIDENCE.json"
DOC_RECONCILIATION = "05-M1-S0-MODULE-SUITE-RECONCILIATION.json"
DOC_MATRIX = "06-CHECKPOINT-B-VERIFICATION-COMMAND-MATRIX.json"
DOC_MANIFEST = "08-CHECKPOINT-B-PACKAGE-MANIFEST.json"

REQUIRED_SOURCE_MEMBERS = (
    "01-OWNER-ACCEPTANCE-CHECKPOINT-A-AND-CHECKPOINT-B-ORDER-001.md",
    DOC_COMPARABILITY,
    DOC_MODULE,
    DOC_SUITE,
    DOC_RECONCILIATION,
    DOC_MATRIX,
    "07-CHECKPOINT-B-RETURN-FINAL.md",
    DOC_MANIFEST,
    "evidence/module.junit.xml",
    "evidence/module.stdout.txt",
    "evidence/module.stderr.txt",
    "evidence/suite.junit.xml",
    "evidence/suite.stdout.txt",
    "evidence/suite.stderr.txt",
)

CHECKPOINT_A_NODEID_MEMBER = "evidence/authorized-nodeids.txt"

N1_AUDIT_INDEX_MEMBER = "OAM-GATE-SAR-05-CDC-AUDIT-INDEX-CANDIDATE-NON-GOVERNING.json"
N1_INDEX_BYTES_MEMBER = (
    "OAM-CDC-PROFILE-CORRECTION-STAGE-B-AUDIT-INDEX-COMPLETE-BYTES-AND-"
    "FIELD-DELTA-001.json"
)

# Exact S0 reconstruction identities.
DELIVERABLE_PROFILE_BYTES = 1454
DELIVERABLE_PROFILE_SHA256 = (
    "7c843beb65dcea78baac3699944d26b0ea3aa064da80157e48b4e2fa5fade398"
)
PROFILE_MANIFEST_BYTES = 1248
PROFILE_MANIFEST_SHA256 = (
    "75dd1c94af2687609ed476756db24dccd25fff90b2beac14e2a13ae19151d4cb"
)
MANIFEST_DIGEST_VALUE = (
    "5d9990d1eb38d1a21c985b3f46de35f5c63dceaf2828674ffa4a87f17008bad9"
)
AUDIT_004_BYTES = 13494
AUDIT_004_SHA256 = "0c7143c500d7912dca95cd01301a2d388c3f8c46ffc3427c95e2089e5425e631"
AUDIT_INDEX_BYTES = 4204
AUDIT_INDEX_SHA256 = "20de3c39d714f392d6511efc9aeb2b49a011c9a168baa1a7d683ee8c202bb376"
AUDIT_INDEX_CONTENT_SHA256 = (
    "1d8f7675746f8294c910e4132907e5650cc60af7af86611ed08d899c0da2c960"
)

DELIVERABLE_PROFILE_RELPATH = "profile/deliverable-profile.json"
PROFILE_MANIFEST_RELPATH = "profile/profile-manifest.json"
AUDIT_INDEX_RELPATH = "docs/governance/gates/OAM-GATE-SAR-05-CDC-AUDIT-INDEX.json"
AUDIT_004_RELPATH = "docs/governance/gates/OAM-GATE-SAR-05-CDC-PROFILE-AUDIT-004.json"
AUDIT_003_REPORT_ID = "OAM-GATE-SAR-05-CDC-PROFILE-AUDIT-003"
AUDIT_004_REPORT_ID = "OAM-GATE-SAR-05-CDC-PROFILE-AUDIT-004"
AUDIT_TOOL_RELPATH = "tools/audit_cdc_profile_conformance.py"
GATE_TOOL_RELPATH = "tools/verify_gate_sar_05_contract.py"

AUDIT_003_NOTE = (
    "Superseded by OAM-GATE-SAR-05-CDC-PROFILE-AUDIT-004 after the bounded CDC "
    "profile correction. The AUDIT-003 report bytes and existing historical state "
    "binding remain unchanged; no rebinding was performed."
)
AUDIT_004_NOTE = (
    "Current-state audit of the bounded CDC profile correction candidate. Generated "
    "by the approved production tool and limited to structural pre-core validation; "
    "independent exact-head review and owner acceptance remain pending."
)

# Exact evidence expectations.
MODULE_COLLECTED = 87
MODULE_PASSED = 78
MODULE_FAILED = 9
MODULE_SKIPPED = 0
MODULE_DISTINCT_FUNCTIONS = 7
MODULE_AFFECTED_MODULES = ["tests/test_audit_lineage.py"]

SUITE_TOTAL = 1041
SUITE_PASSED = 1002
SUITE_FAILED = 32
SUITE_SKIPPED = 7
SUITE_DISTINCT_FUNCTIONS = 30
SUITE_AFFECTED_MODULES = 9

BUCKET_N2A_1 = "N2A_1"
BUCKET_N2A_2 = "N2A_2"
BUCKET_N2B = "N2B_ARTIFACT_OR_MIXED"
BUCKET_N2C = "N2C_INVENTORY"
EXPECTED_BUCKETS = {
    BUCKET_N2A_1: 7,
    BUCKET_N2A_2: 9,
    BUCKET_N2B: 13,
    BUCKET_N2C: 1,
}
BUCKET_N2A_1_NODE_IDS = 9

# D3. Every recorded comparability field, including the three environment
# variables whose unset, set-empty and set-nonempty states are distinguished.
FINGERPRINT_ENVIRONMENT_FIELDS = ("PYTHONPATH", "MYPYPATH", "PYTEST_ADDOPTS")
FINGERPRINT_TEST_FILE_RELPATH = "tests/test_audit_lineage.py"

ENVIRONMENT_UNSET = "UNSET"
ENVIRONMENT_SET_EMPTY = "SET_EMPTY"
ENVIRONMENT_SET_NONEMPTY = "SET_NONEMPTY"

DECISION_PASS = "CHECKPOINT_B_VERIFIER_CHECK_PASS"
DECISION_FAIL = "CHECKPOINT_B_VERIFIER_CHECK_FAIL"
DECISION_UNKNOWN = "CHECKPOINT_B_VERIFIER_UNKNOWN_SUBCOMMAND"

SUBCOMMANDS = (
    "verify-source-package",
    "verify-governed-coordinate",
    "reconstruct-and-verify-s0",
    "verify-environment-fingerprint",
    "verify-module-evidence",
    "verify-suite-evidence",
    "verify-checkpoint-a-nine-id-equality",
    "verify-causal-record-completeness",
    "verify-census-reconciliation",
    "verify-nonchange",
    "verify-package",
    "verify-round-trip",
)


class VerifierInputError(Exception):
    """A governing input could not be read in the exact form the verifier requires."""


@dataclass(frozen=True)
class Config:
    """Resolved locations of every governing input."""

    source_zip: Path
    checkpoint_a_zip: Path
    n1_zip: Path
    authorization_zip: Path
    repository: Path
    python_executable: Path


class CheckLog:
    """Ordered accumulator of named equality checks and their failures."""

    def __init__(self) -> None:
        self.checks: list[dict[str, Any]] = []
        self.errors: list[str] = []

    def record(self, name: str, expected: Any, observed: Any) -> bool:
        """Record one equality check and return whether it held."""
        ok: bool = bool(expected == observed)
        self.checks.append(
            {"name": name, "expected": expected, "observed": observed, "ok": ok}
        )
        if not ok:
            self.errors.append(f"{name}: expected {expected!r} observed {observed!r}")
        return ok

    def fail(self, name: str, detail: str) -> None:
        """Record one non-equality failure with an explicit detail string."""
        self.checks.append(
            {"name": name, "expected": "NO_ERROR", "observed": detail, "ok": False}
        )
        self.errors.append(f"{name}: {detail}")

    def failed_names(self) -> list[str]:
        """Names of every check that did not hold, in record order."""
        return [str(check["name"]) for check in self.checks if not check["ok"]]


# ---------------------------------------------------------------------------
# Primitive helpers.
# ---------------------------------------------------------------------------


def sha256_hex(payload: bytes) -> str:
    """Hexadecimal SHA-256 of exact bytes."""
    return hashlib.sha256(payload).hexdigest()


def sha512_hex(payload: bytes) -> str:
    """Hexadecimal SHA-512 of exact bytes."""
    return hashlib.sha512(payload).hexdigest()


def file_bytes(path: Path) -> bytes:
    """Read one file completely, raising a typed error when it is absent."""
    if not path.is_file():
        raise VerifierInputError(f"required file is absent: {path}")
    return path.read_bytes()


def archive_names(archive: Path) -> list[str]:
    """Names of every non-directory member of a ZIP archive, in archive order.

    Duplicate names are preserved so that duplicate-path accounting is observable.
    """
    if not archive.is_file():
        raise VerifierInputError(f"required archive is absent: {archive}")
    with zipfile.ZipFile(archive) as handle:
        return [info.filename for info in handle.infolist() if not info.is_dir()]


def archive_member(archive: Path, member: str) -> bytes:
    """Exact bytes of one archive member, raising a typed error when absent."""
    if not archive.is_file():
        raise VerifierInputError(f"required archive is absent: {archive}")
    with zipfile.ZipFile(archive) as handle:
        if member not in handle.namelist():
            raise VerifierInputError(f"archive {archive.name} omits member {member}")
        return handle.read(member)


def archive_json(archive: Path, member: str) -> dict[str, Any]:
    """Parse one archive member as a JSON object."""
    parsed: Any = json.loads(archive_member(archive, member).decode("utf-8"))
    if not isinstance(parsed, dict):
        raise VerifierInputError(
            f"member {member} of {archive.name} is not a JSON object"
        )
    return parsed


def git_output(repository: Path, arguments: list[str]) -> str:
    """Run one git command as an argument array and return its stripped stdout."""
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise VerifierInputError(
            f"git {' '.join(arguments)} failed with code {completed.returncode}: "
            f"{completed.stderr.decode('utf-8', 'replace').strip()}"
        )
    return completed.stdout.decode("utf-8").strip()


def nonempty_lines(text: str) -> list[str]:
    """Split text into its non-empty, whitespace-stripped lines."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def as_sorted(values: Any) -> list[str]:
    """Render any iterable of identifiers as a sorted, JSON-serialisable list."""
    return sorted(str(value) for value in values)


def duplicates_in(values: list[str]) -> list[str]:
    """Names that occur more than once, sorted and de-duplicated."""
    seen: set[str] = set()
    repeated: set[str] = set()
    for value in values:
        if value in seen:
            repeated.add(value)
        seen.add(value)
    return sorted(repeated)


def emit(subcommand: str, log: CheckLog, decision_on_pass: str = DECISION_PASS) -> int:
    """Write the deterministic result object and return the process exit code."""
    exit_code = 0 if not log.errors else 1
    payload = {
        "subcommand": subcommand,
        "decision": decision_on_pass if exit_code == 0 else DECISION_FAIL,
        "checks": log.checks,
        "errors": log.errors,
        "exit_code": exit_code,
    }
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return exit_code


def emit_unknown(subcommand: str) -> int:
    """Fail closed on an unrecognised subcommand, still emitting the result shape."""
    detail = f"unrecognised subcommand {subcommand!r}; known: {', '.join(SUBCOMMANDS)}"
    payload = {
        "subcommand": subcommand,
        "decision": DECISION_UNKNOWN,
        "checks": [
            {
                "name": "subcommand_is_known",
                "expected": list(SUBCOMMANDS),
                "observed": subcommand,
                "ok": False,
            }
        ],
        "errors": [detail],
        "exit_code": 2,
    }
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 2


# ---------------------------------------------------------------------------
# D4. Semantic JUnit parsing. The raw XML is the primary source of truth and the
# parsed JSON summary is an object cross-checked against it.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class JUnitCase:
    """One test case as recorded by the raw JUnit XML."""

    node_id: str
    classname: str
    name: str
    module_path: str
    base_name: str
    parameter_suffix: str
    outcome: str
    failure_message: str
    failure_text: str
    first_causal_assertion: str
    skip_message: str


@dataclass(frozen=True)
class JUnitReport:
    """Everything derivable from one raw JUnit XML document."""

    cases: tuple[JUnitCase, ...]
    declared_tests: int
    declared_failures: int
    declared_skipped: int
    declared_errors: int

    def with_outcome(self, outcome: str) -> list[JUnitCase]:
        """Cases carrying one outcome, in document order."""
        return [case for case in self.cases if case.outcome == outcome]

    def identifiers(self, outcome: str) -> list[str]:
        """Node identifiers carrying one outcome, in document order."""
        return [case.node_id for case in self.with_outcome(outcome)]

    def by_node_id(self) -> dict[str, JUnitCase]:
        """Cases indexed by node identifier."""
        return {case.node_id: case for case in self.cases}


def classname_to_module_path(classname: str) -> str:
    """Convert a pytest JUnit dotted classname into its repository module path."""
    if not classname:
        raise VerifierInputError("a JUnit testcase carries an empty classname")
    return classname.replace(".", "/") + ".py"


def split_test_name(name: str) -> tuple[str, str]:
    """Split a pytest test name into its base function and parametrized suffix."""
    start = name.find("[")
    if start == -1:
        return name, ""
    if not name.endswith("]"):
        raise VerifierInputError(f"malformed parametrized test name: {name}")
    return name[:start], name[start:]


def first_line(text: str) -> str:
    """The first line of a message, stripped, or the empty string."""
    lines = text.splitlines()
    return lines[0].strip() if lines else ""


def parse_junit(payload: bytes) -> JUnitReport:
    """Derive every test outcome and failure detail from raw JUnit XML."""
    root = ElementTree.fromstring(payload.decode("utf-8"))
    suite = root.find("testsuite") if root.tag == "testsuites" else root
    if suite is None:
        raise VerifierInputError("the JUnit document carries no testsuite element")

    cases: list[JUnitCase] = []
    for element in suite.findall("testcase"):
        classname = element.get("classname", "")
        name = element.get("name", "")
        if not name:
            raise VerifierInputError("a JUnit testcase carries an empty name")
        module_path = classname_to_module_path(classname)
        base_name, parameter_suffix = split_test_name(name)

        failure = element.find("failure")
        error = element.find("error")
        skipped = element.find("skipped")
        if failure is not None:
            outcome = "failed"
            failure_message = failure.get("message", "")
            failure_text = failure.text or ""
        elif error is not None:
            outcome = "errored"
            failure_message = error.get("message", "")
            failure_text = error.text or ""
        elif skipped is not None:
            outcome = "skipped"
            failure_message = ""
            failure_text = ""
        else:
            outcome = "passed"
            failure_message = ""
            failure_text = ""

        cases.append(
            JUnitCase(
                node_id=f"{module_path}::{name}",
                classname=classname,
                name=name,
                module_path=module_path,
                base_name=base_name,
                parameter_suffix=parameter_suffix,
                outcome=outcome,
                failure_message=failure_message,
                failure_text=failure_text,
                first_causal_assertion=first_line(failure_message),
                skip_message=(
                    skipped.get("message", "") if skipped is not None else ""
                ),
            )
        )

    def declared(attribute: str) -> int:
        raw = suite.get(attribute)
        if raw is None:
            raise VerifierInputError(f"the testsuite element omits {attribute}")
        return int(raw)

    return JUnitReport(
        cases=tuple(cases),
        declared_tests=declared("tests"),
        declared_failures=declared("failures"),
        declared_skipped=declared("skipped"),
        declared_errors=declared("errors"),
    )


def load_junit(config: Config, stem: str) -> JUnitReport:
    """Parse one packaged raw JUnit document."""
    return parse_junit(archive_member(config.source_zip, f"evidence/{stem}.junit.xml"))


# ---------------------------------------------------------------------------
# D5. Node identifier and function locator parsing.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NodeIdentifier:
    """A pytest node identifier decomposed into its governed parts."""

    node_id: str
    module_path: str
    function_name: str
    base_name: str
    parameter_suffix: str


def parse_node_id(node_id: str) -> NodeIdentifier:
    """Decompose a node identifier into module path, function and suffix."""
    module_path, separator, function_name = node_id.partition("::")
    if not separator or not module_path or not function_name:
        raise VerifierInputError(f"malformed node identifier: {node_id}")
    base_name, parameter_suffix = split_test_name(function_name)
    return NodeIdentifier(
        node_id=node_id,
        module_path=module_path,
        function_name=function_name,
        base_name=base_name,
        parameter_suffix=parameter_suffix,
    )


def parse_function_locator(locator: str) -> tuple[str, str]:
    """Decompose a census function locator into its module path and function."""
    module_path, separator, function_name = locator.partition("::")
    if not separator or not module_path or not function_name:
        raise VerifierInputError(f"malformed function locator: {locator}")
    if "[" in function_name:
        raise VerifierInputError(
            f"a function locator must name a base function, not a parametrized case: "
            f"{locator}"
        )
    return module_path, function_name


def group_by_base_function(node_ids: list[str]) -> dict[str, list[str]]:
    """Group node identifiers by their module path and base function name."""
    grouped: dict[str, list[str]] = {}
    for node_id in node_ids:
        parsed = parse_node_id(node_id)
        key = f"{parsed.module_path}::{parsed.base_name}"
        grouped.setdefault(key, []).append(node_id)
    return grouped


# ---------------------------------------------------------------------------
# Governing-input readers.
# ---------------------------------------------------------------------------


def preflight_document(config: Config) -> dict[str, Any]:
    """Read the approved Authorization 003 field preflight from its accepted archive."""
    payload = archive_member(config.authorization_zip, AUTHORIZATION_MEMBER)
    if len(payload) != AUTHORIZATION_MEMBER_BYTES:
        raise VerifierInputError(
            f"preflight member byte length {len(payload)} does not equal "
            f"{AUTHORIZATION_MEMBER_BYTES}"
        )
    if sha256_hex(payload) != AUTHORIZATION_MEMBER_SHA256:
        raise VerifierInputError(
            "preflight member sha256 does not equal the accepted digest"
        )
    parsed: Any = json.loads(payload.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise VerifierInputError("preflight member is not a JSON object")
    return parsed


def preflight_rows(preflight: dict[str, Any], key: str) -> dict[str, Any]:
    """Map one preflight field table to a field-name to proposed-value mapping."""
    rows: Any = preflight.get(key)
    if not isinstance(rows, list):
        raise VerifierInputError(f"preflight omits the {key} table")
    mapping: dict[str, Any] = {}
    for row in rows:
        if not isinstance(row, dict) or "field" not in row:
            raise VerifierInputError(f"malformed row in preflight table {key}")
        mapping[str(row["field"])] = row.get("proposed_value")
    return mapping


def load_module_from(name: str, path: Path) -> types.ModuleType:
    """Import one module by explicit file location without touching the import path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise VerifierInputError(f"cannot construct an import spec for {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Subcommand: verify-source-package
# ---------------------------------------------------------------------------


def verify_source_package(config: Config) -> int:
    """Confirm the frozen Checkpoint B archive identity and required membership."""
    log = CheckLog()
    subcommand = "verify-source-package"
    payload = file_bytes(config.source_zip)
    log.record("source_zip_byte_length", SOURCE_ZIP_BYTES, len(payload))
    log.record("source_zip_sha256", SOURCE_ZIP_SHA256, sha256_hex(payload))
    log.record("source_zip_sha512", SOURCE_ZIP_SHA512, sha512_hex(payload))

    with zipfile.ZipFile(config.source_zip) as handle:
        corrupt = handle.testzip()
    log.record("source_zip_first_corrupt_member", None, corrupt)

    names = archive_names(config.source_zip)
    log.record("source_zip_duplicate_members", [], duplicates_in(names))
    log.record(
        "source_zip_member_set", as_sorted(REQUIRED_SOURCE_MEMBERS), as_sorted(names)
    )
    return emit(subcommand, log)


# ---------------------------------------------------------------------------
# Subcommand: verify-governed-coordinate
# ---------------------------------------------------------------------------


def collect_coordinate(repository: Path) -> dict[str, Any]:
    """Read the six governed-coordinate facts from a repository."""
    return {
        "head": git_output(repository, ["rev-parse", "HEAD"]),
        "tree": git_output(repository, ["rev-parse", "HEAD^{tree}"]),
        "status_lines": len(
            nonempty_lines(git_output(repository, ["status", "--porcelain"]))
        ),
        "untracked": len(
            nonempty_lines(
                git_output(repository, ["ls-files", "--others", "--exclude-standard"])
            )
        ),
        "remotes": len(nonempty_lines(git_output(repository, ["remote"]))),
        "refs": len(
            nonempty_lines(
                git_output(repository, ["for-each-ref", "--format=%(refname)"])
            )
        ),
    }


def verify_governed_coordinate(config: Config) -> int:
    """Confirm the governed repository is at the accepted head with a clean tree."""
    log = CheckLog()
    subcommand = "verify-governed-coordinate"
    coordinate = collect_coordinate(config.repository)
    log.record("governed_head", ACCEPTED_HEAD, coordinate["head"])
    log.record("governed_tree", ACCEPTED_TREE, coordinate["tree"])
    log.record("governed_working_tree_dirty_entries", 0, coordinate["status_lines"])
    log.record("governed_untracked_files", 0, coordinate["untracked"])
    log.record("governed_remotes", 0, coordinate["remotes"])
    log.record("governed_refs", ACCEPTED_REFS, coordinate["refs"])
    return emit(subcommand, log)


# ---------------------------------------------------------------------------
# Subcommand: reconstruct-and-verify-s0
# ---------------------------------------------------------------------------


def build_deliverable_profile(
    clone: Path, preflight: dict[str, Any], gate: types.ModuleType
) -> bytes:
    """Construct deliverable-profile bytes from authorized preservation inputs."""
    fields = preflight_rows(preflight, "deliverable_profile_fields")
    declared_artifacts: Any = fields.get("artifacts")
    if not isinstance(declared_artifacts, list) or not declared_artifacts:
        raise VerifierInputError("preflight declares no deliverable-profile artifacts")

    artifacts: list[dict[str, Any]] = []
    for declared in declared_artifacts:
        if not isinstance(declared, dict):
            raise VerifierInputError("malformed artifact row in the preflight")
        relpath = str(declared["path"])
        raw = file_bytes(clone / relpath)
        artifacts.append(
            {
                "byte_length": len(raw),
                "media_type": str(declared["media_type"]),
                "path": relpath,
                "role": str(declared["role"]),
                "sha256": sha256_hex(raw),
                "sha512": sha512_hex(raw),
            }
        )
        if artifacts[-1]["sha256"] != declared["sha256"]:
            raise VerifierInputError(
                f"preservation input {relpath} does not match the approved preflight "
                f"digest"
            )

    profile: dict[str, Any] = {
        "artifacts": artifacts,
        "claims": fields["claims"],
        "contract_version": fields["contract_version"],
        "document_id": fields["document_id"],
        "package_state": fields["package_state"],
        "profile_id": fields["profile_id"],
        "profile_version": fields["profile_version"],
    }
    encoded: bytes = gate.oam_cjson_encode(profile)
    return encoded + b"\n"


def build_profile_manifest(
    clone: Path, preflight: dict[str, Any], gate: types.ModuleType
) -> tuple[bytes, str]:
    """Construct ProfileManifest bytes and recompute gate.manifest_digest."""
    fields = preflight_rows(preflight, "profile_manifest_fields")
    manifest: dict[str, Any] = {}
    for field, proposed in fields.items():
        if field == "benchmark_package":
            if proposed != "OMITTED":
                raise VerifierInputError("preflight no longer omits benchmark_package")
            continue
        if field == "manifest_digest":
            continue
        if field == "declared_extension_points":
            decoded: Any = json.loads(str(proposed))
            manifest[field] = decoded
            continue
        manifest[field] = proposed

    for field in ("deliverable_package", "terminology_package", "workflow_package"):
        reference: Any = manifest.get(field)
        if not isinstance(reference, dict):
            raise VerifierInputError(f"preflight omits the {field} artifact reference")
        relpath = str(reference["path"])
        manifest[field] = {
            "media_type": str(reference["media_type"]),
            "path": relpath,
            "sha256": sha256_hex(file_bytes(clone / relpath)),
        }

    digest: dict[str, str] = gate.manifest_digest(manifest)
    manifest["manifest_digest"] = digest
    encoded: bytes = gate.oam_cjson_encode(manifest)
    return encoded + b"\n", digest["value"]


def build_audit_index(
    clone: Path, artifact_set_sha256: str, audit_module: types.ModuleType
) -> tuple[bytes, str]:
    """Apply the exact four-report audit-index transition and recompute its digest."""
    parent_text = file_bytes(clone / AUDIT_INDEX_RELPATH).decode("utf-8")
    parent: Any = json.loads(parent_text)
    if not isinstance(parent, dict):
        raise VerifierInputError("the parent audit index is not a JSON object")

    index: Any = json.loads(parent_text)
    audit_bytes = file_bytes(clone / AUDIT_004_RELPATH)

    index["current_report_id"] = AUDIT_004_REPORT_ID
    index["index_sequence"] = int(parent["index_sequence"]) + 1
    index["previous_index_sha256"] = str(parent["content_sha256"])

    superseded = 0
    for report in index["reports"]:
        if report["report_id"] == AUDIT_003_REPORT_ID:
            if report["verified_state_artifact_set_sha256"] != artifact_set_sha256:
                raise VerifierInputError(
                    "the parent AUDIT-003 record does not bind the approved artifact set"
                )
            report["note"] = AUDIT_003_NOTE
            report["role"] = "SUPERSEDED_HISTORICAL_AUDIT"
            superseded += 1
    if superseded != 1:
        raise VerifierInputError(
            f"expected exactly one AUDIT-003 record to supersede, found {superseded}"
        )

    index["reports"].append(
        {
            "byte_length": len(audit_bytes),
            "contract_version": "0.5.1",
            "immutable": True,
            "note": AUDIT_004_NOTE,
            "path": AUDIT_004_RELPATH,
            "report_id": AUDIT_004_REPORT_ID,
            "role": "CURRENT_STATE_AUDIT",
            "sha256": sha256_hex(audit_bytes),
            "sha512": sha512_hex(audit_bytes),
            "supersedes_report_id": AUDIT_003_REPORT_ID,
            "verified_state_artifact_set_sha256": artifact_set_sha256,
            "verified_state_head": None,
        }
    )
    if len(index["reports"]) != 4:
        raise VerifierInputError(
            f"the transition must yield four reports, produced {len(index['reports'])}"
        )

    content_digest: str = audit_module.index_content_digest(index)
    index["content_sha256"] = content_digest
    rendered = json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    return rendered.encode("utf-8"), content_digest


def reconstruct_and_verify_s0(config: Config) -> int:
    """Independently rebuild S0 in a disposable clone and verify every identity."""
    log = CheckLog()
    subcommand = "reconstruct-and-verify-s0"
    workspace = Path(tempfile.mkdtemp(prefix="checkpoint-b-s0-"))
    clone = workspace / "reconstruction"
    try:
        preflight = preflight_document(config)
        artifact_set_sha256 = str(preflight["approved_artifact_set_sha256"])

        subprocess.run(
            [
                "git",
                "clone",
                "--no-hardlinks",
                "--quiet",
                str(config.repository),
                str(clone),
            ],
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(clone), "checkout", "--quiet", "--detach", ACCEPTED_HEAD],
            capture_output=True,
            check=True,
        )
        log.record(
            "clone_head", ACCEPTED_HEAD, git_output(clone, ["rev-parse", "HEAD"])
        )
        log.record(
            "clone_tree", ACCEPTED_TREE, git_output(clone, ["rev-parse", "HEAD^{tree}"])
        )
        log.record(
            "clone_working_tree_dirty_entries",
            0,
            len(nonempty_lines(git_output(clone, ["status", "--porcelain"]))),
        )

        gate = load_module_from(
            "verify_gate_sar_05_contract", clone / GATE_TOOL_RELPATH
        )

        profile_payload = build_deliverable_profile(clone, preflight, gate)
        (clone / DELIVERABLE_PROFILE_RELPATH).write_bytes(profile_payload)
        log.record(
            "deliverable_profile_byte_length",
            DELIVERABLE_PROFILE_BYTES,
            len(profile_payload),
        )
        log.record(
            "deliverable_profile_sha256",
            DELIVERABLE_PROFILE_SHA256,
            sha256_hex(profile_payload),
        )

        manifest_payload, digest_value = build_profile_manifest(clone, preflight, gate)
        (clone / PROFILE_MANIFEST_RELPATH).write_bytes(manifest_payload)
        log.record(
            "profile_manifest_byte_length",
            PROFILE_MANIFEST_BYTES,
            len(manifest_payload),
        )
        log.record(
            "profile_manifest_sha256",
            PROFILE_MANIFEST_SHA256,
            sha256_hex(manifest_payload),
        )
        log.record("gate_manifest_digest", MANIFEST_DIGEST_VALUE, digest_value)

        generation = subprocess.run(
            [
                str(config.python_executable),
                AUDIT_TOOL_RELPATH,
                "--write",
                AUDIT_004_RELPATH,
                "--report-id",
                AUDIT_004_REPORT_ID,
            ],
            cwd=clone,
            capture_output=True,
            check=False,
        )
        log.record("audit_004_generation_exit_code", 0, generation.returncode)
        log.record(
            "audit_004_generation_token",
            True,
            b"AUDIT_REPORT_BYTES_VERIFIED" in generation.stdout,
        )
        audit_payload = file_bytes(clone / AUDIT_004_RELPATH)
        log.record("audit_004_byte_length", AUDIT_004_BYTES, len(audit_payload))
        log.record("audit_004_sha256", AUDIT_004_SHA256, sha256_hex(audit_payload))

        audit_module = load_module_from(
            "audit_cdc_profile_conformance", clone / AUDIT_TOOL_RELPATH
        )
        index_payload, content_digest = build_audit_index(
            clone, artifact_set_sha256, audit_module
        )
        log.record(
            "audit_index_content_sha256", AUDIT_INDEX_CONTENT_SHA256, content_digest
        )
        log.record("audit_index_byte_length", AUDIT_INDEX_BYTES, len(index_payload))
        log.record("audit_index_sha256", AUDIT_INDEX_SHA256, sha256_hex(index_payload))
    except VerifierInputError as error:
        log.fail("reconstruction_input", str(error))
    except subprocess.CalledProcessError as error:
        log.fail(
            "reconstruction_subprocess",
            f"{error.cmd} exited {error.returncode}: "
            f"{error.stderr.decode('utf-8', 'replace').strip()}",
        )
    finally:
        shutil.rmtree(workspace, ignore_errors=False)

    log.record("disposable_clone_destroyed", False, workspace.exists())
    return emit(subcommand, log)


# ---------------------------------------------------------------------------
# D3. Subcommand: verify-environment-fingerprint
# ---------------------------------------------------------------------------


def observed_tool_version(python_executable: Path, module: str) -> str:
    """Read the installed version of one tool through the configured interpreter."""
    completed = subprocess.run(
        [str(python_executable), "-m", module, "--version"],
        capture_output=True,
        check=False,
    )
    text = completed.stdout.decode("utf-8", "replace") or completed.stderr.decode(
        "utf-8", "replace"
    )
    for token in text.replace(",", " ").split():
        if token and token[0].isdigit():
            return token
    raise VerifierInputError(f"cannot read a version for {module}")


def interpreter_value(python_executable: Path, expression: str) -> str:
    """Evaluate one expression in the configured interpreter and return its text."""
    completed = subprocess.run(
        [str(python_executable), "-c", expression],
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise VerifierInputError(
            f"the configured interpreter could not evaluate {expression!r}: "
            f"{completed.stderr.decode('utf-8', 'replace').strip()}"
        )
    return completed.stdout.decode("utf-8").strip()


def classify_environment_value(value: str | None) -> str:
    """Distinguish an unset variable from one set empty and one set nonempty."""
    if value is None:
        return ENVIRONMENT_UNSET
    if value == "":
        return ENVIRONMENT_SET_EMPTY
    return ENVIRONMENT_SET_NONEMPTY


def recorded_environment_value(fingerprint: dict[str, Any], name: str) -> str | None:
    """Read one recorded environment field, treating a JSON null as unset."""
    if name not in fingerprint:
        raise VerifierInputError(f"the recorded comparability fingerprint omits {name}")
    value = fingerprint[name]
    if value is None:
        return None
    return str(value)


def verify_environment_fingerprint(config: Config) -> int:
    """Confirm every recorded comparability field against observed state."""
    log = CheckLog()
    subcommand = "verify-environment-fingerprint"
    document = archive_json(config.source_zip, DOC_COMPARABILITY)

    coordinate: Any = document["governed_coordinate"]
    log.record("recorded_head", ACCEPTED_HEAD, coordinate["HEAD"])
    log.record("recorded_tree", ACCEPTED_TREE, coordinate["tree"])
    log.record("recorded_working_tree", "CLEAN", coordinate["working_tree"])
    log.record("recorded_untracked_files", "NONE", coordinate["untracked_files"])
    log.record("recorded_remotes", "NONE", coordinate["remotes"])
    log.record("recorded_refs", ACCEPTED_REFS, coordinate["refs"])
    log.record("recorded_coordinate_result", "ALL MATCH", coordinate["result"])
    log.record("recorded_repository", str(config.repository), coordinate["repository"])

    fingerprint: Any = document["comparability_fingerprint"]

    # Field 1 and 2: accepted head and tree, against the live repository.
    log.record("fingerprint_accepted_head", ACCEPTED_HEAD, fingerprint["accepted_head"])
    log.record("fingerprint_accepted_tree", ACCEPTED_TREE, fingerprint["accepted_tree"])
    live = collect_coordinate(config.repository)
    log.record(
        "fingerprint_accepted_head_matches_repository",
        live["head"],
        fingerprint["accepted_head"],
    )
    log.record(
        "fingerprint_accepted_tree_matches_repository",
        live["tree"],
        fingerprint["accepted_tree"],
    )

    # Field 3: Python executable.
    log.record(
        "fingerprint_python_executable",
        str(config.python_executable),
        fingerprint["python_executable"],
    )

    # Field 4: Python version.
    log.record(
        "fingerprint_python_version",
        fingerprint["python_version"],
        interpreter_value(
            config.python_executable, "import sys;print(sys.version.split()[0])"
        ),
    )

    # Fields 5 and 6: pytest and mypy versions.
    log.record(
        "fingerprint_pytest_version",
        fingerprint["pytest_version"],
        observed_tool_version(config.python_executable, "pytest"),
    )
    log.record(
        "fingerprint_mypy_version",
        fingerprint["mypy_version"],
        observed_tool_version(config.python_executable, "mypy"),
    )

    # Field 7: platform.
    log.record(
        "fingerprint_platform",
        fingerprint["platform"],
        interpreter_value(
            config.python_executable, "import platform;print(platform.platform())"
        ),
    )

    # Fields 8, 9 and 10: environment variables, three-way classified.
    for name in FINGERPRINT_ENVIRONMENT_FIELDS:
        recorded = recorded_environment_value(fingerprint, name)
        observed = os.environ.get(name)
        log.record(
            f"fingerprint_environment_{name}_classification",
            classify_environment_value(recorded),
            classify_environment_value(observed),
        )
        log.record(f"fingerprint_environment_{name}_value", recorded, observed)

    # Fields 11 and 12: the module test file's exact bytes and digest.
    test_file = file_bytes(config.repository / FINGERPRINT_TEST_FILE_RELPATH)
    log.record(
        "fingerprint_test_file_bytes", fingerprint["test_file_bytes"], len(test_file)
    )
    log.record(
        "fingerprint_test_file_sha256",
        fingerprint["test_file_sha256"],
        sha256_hex(test_file),
    )

    log.record(
        "fingerprint_matches_checkpoint_a", True, fingerprint["matches_checkpoint_a"]
    )
    log.record(
        "fingerprint_material_field_differences",
        0,
        fingerprint["material_field_differences"],
    )

    identities: Any = document["accepted_n1_identities"]
    log.record(
        "n1_deliverable_profile",
        f"{DELIVERABLE_PROFILE_BYTES} / {DELIVERABLE_PROFILE_SHA256}",
        identities["deliverable_profile"],
    )
    log.record(
        "n1_profile_manifest",
        f"{PROFILE_MANIFEST_BYTES} / {PROFILE_MANIFEST_SHA256}",
        identities["profile_manifest"],
    )
    log.record(
        "n1_manifest_digest", MANIFEST_DIGEST_VALUE, identities["manifest_digest"]
    )
    log.record(
        "n1_audit_004",
        f"{AUDIT_004_BYTES} / {AUDIT_004_SHA256}",
        identities["audit_004"],
    )
    log.record(
        "n1_audit_index",
        f"{AUDIT_INDEX_BYTES} / {AUDIT_INDEX_SHA256}",
        identities["audit_index"],
    )
    log.record(
        "n1_identity_result", "ALL MATCH", document["accepted_n1_identity_result"]
    )
    log.record(
        "candidate_bytes_copied_from_n1_package",
        False,
        document["candidate_bytes_copied_from_n1_package"],
    )

    n1_payload = file_bytes(config.n1_zip)
    log.record("n1_zip_byte_length", N1_ZIP_BYTES, len(n1_payload))
    log.record("n1_zip_sha256", N1_ZIP_SHA256, sha256_hex(n1_payload))
    n1_index = archive_member(config.n1_zip, N1_AUDIT_INDEX_MEMBER)
    log.record("n1_audit_index_member_byte_length", AUDIT_INDEX_BYTES, len(n1_index))
    log.record("n1_audit_index_member_sha256", AUDIT_INDEX_SHA256, sha256_hex(n1_index))

    n1_notes: Any = archive_json(config.n1_zip, N1_INDEX_BYTES_MEMBER)[
        "owner_note_strings"
    ]
    log.record("n1_audit_003_note", AUDIT_003_NOTE, n1_notes["AUDIT-003"])
    log.record("n1_audit_004_note", AUDIT_004_NOTE, n1_notes["AUDIT-004"])

    checkpoint_a: Any = document["checkpoint_a_source"]
    log.record(
        "checkpoint_a_recorded_byte_length",
        CHECKPOINT_A_ZIP_BYTES,
        checkpoint_a["byte_length"],
    )
    log.record(
        "checkpoint_a_recorded_sha256", CHECKPOINT_A_ZIP_SHA256, checkpoint_a["sha256"]
    )
    log.record(
        "checkpoint_a_treated_read_only", True, checkpoint_a["treated_read_only"]
    )
    return emit(subcommand, log)


# ---------------------------------------------------------------------------
# D4. Subcommands: verify-module-evidence and verify-suite-evidence
# ---------------------------------------------------------------------------


def raw_evidence_checks(
    log: CheckLog, config: Config, document: dict[str, Any], prefix: str, stem: str
) -> None:
    """Confirm the declared raw-evidence identities equal the packaged bytes."""
    raw: Any = document["raw_evidence"]
    for stream, member in (
        ("junit", f"evidence/{stem}.junit.xml"),
        ("stdout", f"evidence/{stem}.stdout.txt"),
        ("stderr", f"evidence/{stem}.stderr.txt"),
    ):
        payload = archive_member(config.source_zip, member)
        log.record(
            f"{prefix}_{stream}_byte_length", raw[stream]["byte_length"], len(payload)
        )
        log.record(
            f"{prefix}_{stream}_sha256", raw[stream]["sha256"], sha256_hex(payload)
        )
        log.record(
            f"{prefix}_{stream}_sha512", raw[stream]["sha512"], sha512_hex(payload)
        )


def junit_semantic_checks(
    log: CheckLog,
    report: JUnitReport,
    prefix: str,
    expected_collected: int,
    expected_passed: int,
    expected_failed: int,
    expected_skipped: int,
) -> None:
    """Derive counts directly from raw JUnit XML and check internal consistency."""
    log.record(f"{prefix}_junit_collected", expected_collected, len(report.cases))
    log.record(
        f"{prefix}_junit_passed", expected_passed, len(report.with_outcome("passed"))
    )
    log.record(
        f"{prefix}_junit_failed", expected_failed, len(report.with_outcome("failed"))
    )
    log.record(
        f"{prefix}_junit_skipped", expected_skipped, len(report.with_outcome("skipped"))
    )
    log.record(f"{prefix}_junit_errored", 0, len(report.with_outcome("errored")))
    log.record(
        f"{prefix}_junit_declared_tests", len(report.cases), report.declared_tests
    )
    log.record(
        f"{prefix}_junit_declared_failures",
        len(report.with_outcome("failed")),
        report.declared_failures,
    )
    log.record(
        f"{prefix}_junit_declared_skipped",
        len(report.with_outcome("skipped")),
        report.declared_skipped,
    )
    log.record(
        f"{prefix}_junit_declared_errors",
        len(report.with_outcome("errored")),
        report.declared_errors,
    )
    log.record(
        f"{prefix}_junit_node_ids_distinct",
        len(report.cases),
        len({case.node_id for case in report.cases}),
    )

    identity_violations = [
        case.node_id
        for case in report.cases
        if case.node_id
        != f"{case.module_path}::{case.base_name}{case.parameter_suffix}"
        or case.module_path != classname_to_module_path(case.classname)
    ]
    log.record(f"{prefix}_junit_case_identity_violations", [], identity_violations)

    unnamed_failures = [
        case.node_id
        for case in report.with_outcome("failed")
        if f"def {case.base_name}(" not in case.failure_text
    ]
    log.record(f"{prefix}_junit_failure_text_names_its_test", [], unnamed_failures)

    empty_messages = [
        case.node_id
        for case in report.with_outcome("failed")
        if not case.failure_message.strip()
    ]
    log.record(f"{prefix}_junit_failure_message_present", [], empty_messages)


def verify_module_evidence(config: Config) -> int:
    """Confirm the frozen module-scoped evidence against raw JUnit semantics."""
    log = CheckLog()
    subcommand = "verify-module-evidence"
    document = archive_json(config.source_zip, DOC_MODULE)
    report = load_junit(config, "module")

    junit_semantic_checks(
        log,
        report,
        "module",
        MODULE_COLLECTED,
        MODULE_PASSED,
        MODULE_FAILED,
        MODULE_SKIPPED,
    )

    log.record("module_collected", MODULE_COLLECTED, document["collected"])
    log.record("module_passed", MODULE_PASSED, document["passed"])
    log.record("module_failed", MODULE_FAILED, document["failed"])
    log.record("module_skipped", MODULE_SKIPPED, document["skipped"])
    log.record("module_exit_code", 1, document["exit_code"])

    equality: Any = document["checkpoint_a_nine_id_equality"]
    json_failing = [str(value) for value in equality["module_failing_ids"]]
    json_collected = [str(value) for value in document["collected_test_ids"]]
    json_passing = [str(value) for value in document["passing_test_ids"]]

    log.record(
        "module_json_collected_matches_junit",
        as_sorted(report.identifiers("passed") + report.identifiers("failed")),
        as_sorted(json_collected),
    )
    log.record(
        "module_json_passing_matches_junit",
        as_sorted(report.identifiers("passed")),
        as_sorted(json_passing),
    )
    log.record(
        "module_json_failing_matches_junit",
        as_sorted(report.identifiers("failed")),
        as_sorted(json_failing),
    )
    log.record(
        "module_json_counts_match_junit",
        [
            len(report.cases),
            len(report.with_outcome("passed")),
            len(report.with_outcome("failed")),
            len(report.with_outcome("skipped")),
        ],
        [
            document["collected"],
            document["passed"],
            document["failed"],
            document["skipped"],
        ],
    )
    log.record(
        "module_pass_fail_overlap", 0, len(set(json_passing) & set(json_failing))
    )
    log.record("module_failing_ids_distinct", MODULE_FAILED, len(set(json_failing)))

    log.record(
        "module_distinct_failing_functions",
        MODULE_DISTINCT_FUNCTIONS,
        len(document["distinct_failing_functions"]),
    )
    log.record(
        "module_distinct_failing_functions_match_junit",
        MODULE_DISTINCT_FUNCTIONS,
        len({case.base_name for case in report.with_outcome("failed")}),
    )
    log.record(
        "module_affected_module_set",
        MODULE_AFFECTED_MODULES,
        [str(value) for value in document["affected_module_set"]],
    )
    log.record(
        "module_affected_module_set_matches_junit",
        as_sorted(MODULE_AFFECTED_MODULES),
        as_sorted({case.module_path for case in report.with_outcome("failed")}),
    )

    reproduction: Any = document["reproduction_check"]
    log.record("module_reproduction_result", "REPRODUCED", reproduction["result"])
    log.record(
        "module_reproduction_agreement",
        reproduction["expected"],
        reproduction["observed"],
    )
    log.record(
        "module_reproduction_expected_text",
        f"collected {MODULE_COLLECTED} / passed {MODULE_PASSED} / "
        f"failed {MODULE_FAILED} / skipped {MODULE_SKIPPED}",
        reproduction["expected"],
    )

    raw_evidence_checks(log, config, document, "module", "module")
    return emit(subcommand, log)


def verify_suite_evidence(config: Config) -> int:
    """Confirm the frozen full-suite evidence against raw JUnit semantics."""
    log = CheckLog()
    subcommand = "verify-suite-evidence"
    document = archive_json(config.source_zip, DOC_SUITE)
    report = load_junit(config, "suite")

    junit_semantic_checks(
        log, report, "suite", SUITE_TOTAL, SUITE_PASSED, SUITE_FAILED, SUITE_SKIPPED
    )

    log.record("suite_total_tests", SUITE_TOTAL, document["total_tests"])
    log.record("suite_passed", SUITE_PASSED, document["passed"])
    log.record("suite_failed", SUITE_FAILED, document["failed"])
    log.record("suite_skipped", SUITE_SKIPPED, document["skipped"])
    log.record("suite_skipped_count", SUITE_SKIPPED, document["skipped_count"])
    log.record("suite_exit_code", 1, document["exit_code"])
    log.record(
        "suite_arithmetic",
        SUITE_TOTAL,
        int(document["passed"]) + int(document["failed"]) + int(document["skipped"]),
    )

    records: Any = document["failing_ids_with_causal_assertion"]
    json_failing = [str(record["test_id"]) for record in records]
    json_skipped = [str(value) for value in document["skipped_test_ids"]]

    log.record(
        "suite_json_failing_matches_junit",
        as_sorted(report.identifiers("failed")),
        as_sorted(json_failing),
    )
    log.record(
        "suite_json_skipped_matches_junit",
        as_sorted(report.identifiers("skipped")),
        as_sorted(json_skipped),
    )
    log.record(
        "suite_json_counts_match_junit",
        [
            len(report.cases),
            len(report.with_outcome("passed")),
            len(report.with_outcome("failed")),
            len(report.with_outcome("skipped")),
        ],
        [
            document["total_tests"],
            document["passed"],
            document["failed"],
            document["skipped"],
        ],
    )
    log.record(
        "suite_failing_id_count_field", SUITE_FAILED, document["failing_id_count"]
    )
    log.record("suite_failing_ids_distinct", SUITE_FAILED, len(set(json_failing)))
    log.record("suite_skipped_ids_distinct", SUITE_SKIPPED, len(set(json_skipped)))

    functions = [str(value) for value in document["distinct_failing_functions"]]
    log.record(
        "suite_distinct_failing_function_field",
        SUITE_DISTINCT_FUNCTIONS,
        document["distinct_failing_function_count"],
    )
    log.record(
        "suite_distinct_failing_functions", SUITE_DISTINCT_FUNCTIONS, len(functions)
    )
    log.record(
        "suite_distinct_failing_functions_match_junit",
        as_sorted(functions),
        as_sorted({case.base_name for case in report.with_outcome("failed")}),
    )

    modules = [str(value) for value in document["affected_modules"]]
    log.record(
        "suite_affected_module_field",
        SUITE_AFFECTED_MODULES,
        document["affected_module_count"],
    )
    log.record(
        "suite_affected_modules_match_junit",
        as_sorted(modules),
        as_sorted({case.module_path for case in report.with_outcome("failed")}),
    )

    reproduction: Any = document["reproduction_check"]
    log.record("suite_reproduction_result", "REPRODUCED", reproduction["result"])
    log.record(
        "suite_reproduction_agreement",
        reproduction["expected"],
        reproduction["observed"],
    )
    log.record(
        "suite_reproduction_expected_text",
        f"total {SUITE_TOTAL} / passed {SUITE_PASSED} / failed {SUITE_FAILED} / "
        f"skipped {SUITE_SKIPPED}; {SUITE_FAILED} IDs, {SUITE_DISTINCT_FUNCTIONS} functions, "
        f"{SUITE_AFFECTED_MODULES} modules",
        reproduction["expected"],
    )

    raw_evidence_checks(log, config, document, "suite", "suite")
    return emit(subcommand, log)


# ---------------------------------------------------------------------------
# Subcommand: verify-checkpoint-a-nine-id-equality
# ---------------------------------------------------------------------------


def verify_checkpoint_a_nine_id_equality(config: Config) -> int:
    """Confirm the module failure set equals the accepted Checkpoint A nine exactly."""
    log = CheckLog()
    subcommand = "verify-checkpoint-a-nine-id-equality"

    checkpoint_a_payload = file_bytes(config.checkpoint_a_zip)
    log.record(
        "checkpoint_a_zip_byte_length",
        CHECKPOINT_A_ZIP_BYTES,
        len(checkpoint_a_payload),
    )
    log.record(
        "checkpoint_a_zip_sha256",
        CHECKPOINT_A_ZIP_SHA256,
        sha256_hex(checkpoint_a_payload),
    )

    authorized = nonempty_lines(
        archive_member(config.checkpoint_a_zip, CHECKPOINT_A_NODEID_MEMBER).decode(
            "utf-8"
        )
    )
    log.record("checkpoint_a_authorized_id_count", MODULE_FAILED, len(authorized))
    log.record(
        "checkpoint_a_authorized_ids_distinct", MODULE_FAILED, len(set(authorized))
    )

    document = archive_json(config.source_zip, DOC_MODULE)
    equality: Any = document["checkpoint_a_nine_id_equality"]
    recorded = [str(value) for value in equality["checkpoint_a_ids"]]
    failing = [str(value) for value in equality["module_failing_ids"]]
    junit_failing = load_junit(config, "module").identifiers("failed")

    log.record(
        "recorded_checkpoint_a_ids_match_archive",
        as_sorted(authorized),
        as_sorted(recorded),
    )
    log.record(
        "module_failure_set_equals_authorized_nine",
        as_sorted(authorized),
        as_sorted(failing),
    )
    log.record(
        "junit_failure_set_equals_authorized_nine",
        as_sorted(authorized),
        as_sorted(junit_failing),
    )
    log.record(
        "missing_authorized_failures_measured", 0, len(set(authorized) - set(failing))
    )
    log.record(
        "additional_module_failures_measured", 0, len(set(failing) - set(authorized))
    )
    log.record(
        "missing_authorized_failures_declared",
        0,
        equality["missing_authorized_failures"],
    )
    log.record(
        "additional_module_failures_declared", 0, equality["additional_module_failures"]
    )
    log.record("byte_identical_set_declared", True, equality["byte_identical_set"])
    return emit(subcommand, log)


# ---------------------------------------------------------------------------
# D4. Subcommand: verify-causal-record-completeness
# ---------------------------------------------------------------------------


def causal_records(document: dict[str, Any]) -> list[dict[str, Any]]:
    """The causal-assertion records carried by one evidence document."""
    records: Any = document["failing_ids_with_causal_assertion"]
    if not isinstance(records, list):
        raise VerifierInputError("failing_ids_with_causal_assertion is not a list")
    return [record for record in records if isinstance(record, dict)]


def causal_checks(
    log: CheckLog,
    prefix: str,
    report: JUnitReport,
    records: list[dict[str, Any]],
    expected: int,
) -> None:
    """Bind every causal record to its own failing test case in the raw JUnit XML."""
    cases = report.by_node_id()
    junit_failing = set(report.identifiers("failed"))

    log.record(f"{prefix}_causal_record_count", expected, len(records))
    identifiers = [str(record.get("test_id", "")) for record in records]
    log.record(f"{prefix}_causal_record_ids_distinct", expected, len(set(identifiers)))
    log.record(
        f"{prefix}_causal_records_cover_junit_failures",
        as_sorted(junit_failing),
        as_sorted(identifiers),
    )

    unknown: list[str] = []
    not_failing: list[str] = []
    empty: list[str] = []
    underivable: list[str] = []
    for record in records:
        node_id = str(record.get("test_id", ""))
        case = cases.get(node_id)
        if case is None:
            unknown.append(node_id)
            continue
        if case.outcome != "failed":
            not_failing.append(node_id)
            continue
        assertion = record.get("first_causal_assertion")
        if not isinstance(assertion, str) or not assertion.strip():
            empty.append(node_id)
            continue
        # The causal text must be derivable from this test case's own failure
        # element. An arbitrary nonempty string, or text copied from another
        # test case, is not derivable and is recorded here.
        if assertion.strip() != case.first_causal_assertion:
            underivable.append(node_id)

    log.record(f"{prefix}_causal_records_absent_from_junit", [], as_sorted(unknown))
    log.record(
        f"{prefix}_causal_records_not_failing_in_junit", [], as_sorted(not_failing)
    )
    log.record(f"{prefix}_causal_assertions_empty", [], as_sorted(empty))
    log.record(
        f"{prefix}_causal_assertions_not_derivable_from_failure_element",
        [],
        as_sorted(underivable),
    )


def verify_causal_record_completeness(config: Config) -> int:
    """Confirm every module and suite failure carries a derivable causal assertion."""
    log = CheckLog()
    subcommand = "verify-causal-record-completeness"

    module_document = archive_json(config.source_zip, DOC_MODULE)
    suite_document = archive_json(config.source_zip, DOC_SUITE)

    causal_checks(
        log,
        "module",
        load_junit(config, "module"),
        causal_records(module_document),
        MODULE_FAILED,
    )
    causal_checks(
        log,
        "suite",
        load_junit(config, "suite"),
        causal_records(suite_document),
        SUITE_FAILED,
    )
    return emit(subcommand, log)


# ---------------------------------------------------------------------------
# D5. Subcommand: verify-census-reconciliation
# ---------------------------------------------------------------------------


def verify_census_reconciliation(config: Config) -> int:
    """Confirm the census partitions all thirty functions and binds every node ID."""
    log = CheckLog()
    subcommand = "verify-census-reconciliation"
    document = archive_json(config.source_zip, DOC_RECONCILIATION)
    report = load_junit(config, "suite")
    junit_failing = report.identifiers("failed")
    derived_groups = group_by_base_function(junit_failing)

    declared: Any = document["measured_bucket_counts"]
    for bucket, expected in EXPECTED_BUCKETS.items():
        log.record(f"declared_bucket_{bucket}", expected, declared[bucket])

    functions: Any = document["functions"]
    log.record("census_function_records", SUITE_DISTINCT_FUNCTIONS, len(functions))

    locators: list[str] = []
    measured: dict[str, int] = {bucket: 0 for bucket in EXPECTED_BUCKETS}
    bucket_node_ids: dict[str, int] = {bucket: 0 for bucket in EXPECTED_BUCKETS}
    all_node_ids: list[str] = []
    unknown_buckets = 0

    module_violations: list[str] = []
    function_violations: list[str] = []
    suffix_violations: list[str] = []
    group_violations: list[str] = []

    for record in functions:
        if not isinstance(record, dict):
            log.fail("census_record_shape", "a census function record is not an object")
            continue
        locator = str(record["function_locator"])
        locators.append(locator)
        locator_module, locator_function = parse_function_locator(locator)
        bucket = str(record["downstream_bucket"])
        identifiers = [str(value) for value in record["failing_node_ids"]]
        all_node_ids.extend(identifiers)

        if bucket in measured:
            measured[bucket] += 1
            bucket_node_ids[bucket] += len(identifiers)
        else:
            unknown_buckets += 1

        for node_id in identifiers:
            parsed = parse_node_id(node_id)
            if parsed.module_path != locator_module:
                module_violations.append(f"{locator} <- {node_id}")
            if parsed.base_name != locator_function:
                function_violations.append(f"{locator} <- {node_id}")
            if parsed.parameter_suffix and parsed.base_name != locator_function:
                suffix_violations.append(f"{locator} <- {node_id}")

        expected_group = sorted(derived_groups.get(locator, []))
        if sorted(identifiers) != expected_group:
            group_violations.append(locator)

    log.record("census_node_id_module_binding", [], as_sorted(module_violations))
    log.record("census_node_id_function_binding", [], as_sorted(function_violations))
    log.record("census_node_id_parametrized_binding", [], as_sorted(suffix_violations))
    log.record("census_node_id_group_assignment", [], as_sorted(group_violations))
    log.record(
        "census_locator_set_matches_junit_groups",
        as_sorted(derived_groups),
        as_sorted(locators),
    )

    log.record("census_unknown_buckets", 0, unknown_buckets)
    log.record("census_duplicate_bucket_assignments", [], duplicates_in(locators))
    log.record(
        "census_distinct_function_locators",
        SUITE_DISTINCT_FUNCTIONS,
        len(set(locators)),
    )
    for bucket, expected in EXPECTED_BUCKETS.items():
        log.record(f"measured_bucket_{bucket}", expected, measured[bucket])
    log.record(
        "measured_bucket_N2A_1_node_ids",
        BUCKET_N2A_1_NODE_IDS,
        bucket_node_ids[BUCKET_N2A_1],
    )

    log.record(
        "census_measured_total_field",
        SUITE_DISTINCT_FUNCTIONS,
        document["measured_total"],
    )
    log.record(
        "census_measured_total_recomputed",
        SUITE_DISTINCT_FUNCTIONS,
        sum(measured.values()),
    )
    log.record("census_arithmetic_holds", True, document["arithmetic_holds"])
    log.record("census_unaccounted_functions", 0, document["unaccounted_functions"])
    log.record(
        "census_duplicate_bucket_assignments_declared",
        0,
        document["duplicate_bucket_assignments"],
    )
    log.record("census_unexpected_failures", 0, document["unexpected_failures"])
    log.record(
        "census_functions_accounted_for",
        SUITE_DISTINCT_FUNCTIONS,
        document["suite_failing_functions_accounted_for"],
    )

    log.record("census_node_ids_distinct", SUITE_FAILED, len(set(all_node_ids)))
    log.record(
        "census_node_ids_cover_junit_failures",
        as_sorted(junit_failing),
        as_sorted(all_node_ids),
    )

    partition: Any = document["accepted_partition"]
    log.record(
        "accepted_partition_N2A_1", "7 functions / 9 IDs", partition[BUCKET_N2A_1]
    )
    log.record("accepted_partition_N2A_2", "9 functions", partition[BUCKET_N2A_2])
    log.record("accepted_partition_N2B", "13 functions", partition[BUCKET_N2B])
    log.record("accepted_partition_N2C", "1 function", partition[BUCKET_N2C])
    return emit(subcommand, log)


# ---------------------------------------------------------------------------
# Subcommand: verify-nonchange
# ---------------------------------------------------------------------------


def verify_nonchange(config: Config) -> int:
    """Confirm the governed repository and frozen sources were not mutated."""
    log = CheckLog()
    subcommand = "verify-nonchange"

    coordinate = collect_coordinate(config.repository)
    log.record("governed_head_unchanged", ACCEPTED_HEAD, coordinate["head"])
    log.record("governed_tree_unchanged", ACCEPTED_TREE, coordinate["tree"])
    log.record("governed_working_tree_clean", 0, coordinate["status_lines"])
    log.record("governed_untracked_files", 0, coordinate["untracked"])
    log.record("governed_refs", ACCEPTED_REFS, coordinate["refs"])
    log.record("governed_remotes", 0, coordinate["remotes"])

    for relpath in (
        DELIVERABLE_PROFILE_RELPATH,
        PROFILE_MANIFEST_RELPATH,
        AUDIT_004_RELPATH,
    ):
        log.record(
            f"governed_absent_{relpath}", False, (config.repository / relpath).exists()
        )

    manifest = archive_json(config.source_zip, DOC_MANIFEST)
    log.record(
        "manifest_governed_repository_mutated",
        False,
        manifest["governed_repository_mutated"],
    )
    log.record("manifest_accepted_head", ACCEPTED_HEAD, manifest["accepted_head"])
    log.record(
        "manifest_governed_repository",
        str(config.repository),
        manifest["governed_repository"],
    )

    comparability = archive_json(config.source_zip, DOC_COMPARABILITY)
    log.record(
        "comparability_s0_test_layer_edits", 0, comparability["s0_test_layer_edits"]
    )
    log.record(
        "comparability_destination_was_empty_before_use",
        True,
        comparability["destination_was_empty_before_use"],
    )

    for member in (DOC_COMPARABILITY, DOC_MODULE, DOC_SUITE, DOC_RECONCILIATION):
        document = archive_json(config.source_zip, member)
        log.record(
            f"classification_{member}",
            "NON_GOVERNING_DRY_RUN_ONLY",
            document["classification"],
        )
        log.record(
            f"handling_{member}", "DO_NOT_COPY_INTO_STAGE_B1", document["handling"]
        )

    payload = file_bytes(config.source_zip)
    log.record("frozen_source_byte_length", SOURCE_ZIP_BYTES, len(payload))
    log.record("frozen_source_sha256", SOURCE_ZIP_SHA256, sha256_hex(payload))
    checkpoint_a_payload = file_bytes(config.checkpoint_a_zip)
    log.record(
        "frozen_checkpoint_a_byte_length",
        CHECKPOINT_A_ZIP_BYTES,
        len(checkpoint_a_payload),
    )
    log.record(
        "frozen_checkpoint_a_sha256",
        CHECKPOINT_A_ZIP_SHA256,
        sha256_hex(checkpoint_a_payload),
    )
    return emit(subcommand, log)


# ---------------------------------------------------------------------------
# D2. Subcommand: verify-package. Every accounting value is observed.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PackageAccounting:
    """Package accounting derived entirely from observed archive and manifest state."""

    physical_names: tuple[str, ...]
    duplicate_paths: tuple[str, ...]
    manifest_member_paths: tuple[str, ...]
    declared_payload_files: int
    self_excluded_names: tuple[str, ...]
    missing_paths: tuple[str, ...]
    undeclared_paths: tuple[str, ...]
    manifest_self_inclusion_present: bool
    manifest_self_inclusion_value: Any
    manifest_path_in_members: bool

    def self_inclusion_is_boolean(self) -> bool:
        """F1. True only when the declaration is present and a real JSON boolean.

        A JSON null, a string and an integer are all rejected here rather than
        being reduced to a boolean, so absence can never read as an explicit
        false declaration.
        """
        return self.manifest_self_inclusion_present and isinstance(
            self.manifest_self_inclusion_value, bool
        )

    def self_inclusion_is_false(self) -> bool:
        """F1. True only when the declaration is present, boolean and exactly false."""
        return self.self_inclusion_is_boolean() and (
            self.manifest_self_inclusion_value is False
        )


def observe_package(archive: Path, manifest_member: str) -> PackageAccounting:
    """Read every accounting quantity from the archive and its manifest."""
    names = archive_names(archive)
    manifest = archive_json(archive, manifest_member)
    members: Any = manifest.get("members")
    if not isinstance(members, list):
        raise VerifierInputError(f"{manifest_member} carries no members list")

    member_paths = tuple(str(member["path"]) for member in members)
    declared_raw: Any = manifest.get("declared_payload_files")
    if not isinstance(declared_raw, int):
        raise VerifierInputError(f"{manifest_member} carries no declared_payload_files")

    # Every physical file that is not a declared payload member is observed here.
    # Exactly one of them is expected to be the self-excluded manifest; any other
    # is an undeclared payload file. Both quantities are observed, never assumed.
    unaccounted = tuple(
        sorted({name for name in names if name not in set(member_paths)})
    )
    self_excluded = tuple(name for name in unaccounted if name == manifest_member)
    missing = tuple(sorted(set(member_paths) - set(names)))
    undeclared = tuple(name for name in unaccounted if name != manifest_member)

    # F1. Presence, type and value are carried separately and are never reduced
    # through bool(). The absence of the declaration is not a false declaration.
    return PackageAccounting(
        physical_names=tuple(names),
        duplicate_paths=tuple(duplicates_in(names)),
        manifest_member_paths=member_paths,
        declared_payload_files=declared_raw,
        self_excluded_names=self_excluded,
        missing_paths=missing,
        undeclared_paths=undeclared,
        manifest_self_inclusion_present="manifest_self_inclusion" in manifest,
        manifest_self_inclusion_value=manifest.get("manifest_self_inclusion"),
        manifest_path_in_members=manifest_member in set(member_paths),
    )


def verify_package(config: Config) -> int:
    """Confirm observed package accounting and every declared member identity."""
    log = CheckLog()
    subcommand = "verify-package"
    accounting = observe_package(config.source_zip, DOC_MANIFEST)

    observed_members = len(accounting.manifest_member_paths)
    observed_physical = len(accounting.physical_names)
    observed_self_excluded = len(accounting.self_excluded_names)

    # Observed against observed. No accounting result is produced from constants.
    log.record(
        "package_declared_payload_files_matches_members",
        observed_members,
        accounting.declared_payload_files,
    )
    log.record("package_self_excluded_manifest_count", 1, observed_self_excluded)
    log.record(
        "package_self_excluded_manifest_is_the_manifest",
        [DOC_MANIFEST],
        list(accounting.self_excluded_names),
    )
    log.record(
        "package_physical_file_count_accounts_for_members",
        observed_physical,
        observed_members + observed_self_excluded,
    )
    log.record("package_missing_payload_paths", [], list(accounting.missing_paths))
    log.record(
        "package_undeclared_payload_paths", [], list(accounting.undeclared_paths)
    )
    log.record("package_duplicate_archive_paths", [], list(accounting.duplicate_paths))
    # F1. Presence, type and value are three independent observed branches.
    log.record(
        "manifest_self_inclusion_present",
        True,
        accounting.manifest_self_inclusion_present,
    )
    log.record(
        "manifest_self_inclusion_is_boolean",
        True,
        accounting.self_inclusion_is_boolean(),
    )
    log.record(
        "manifest_self_inclusion_is_false",
        True,
        accounting.self_inclusion_is_false(),
    )
    log.record(
        "package_manifest_path_excluded_from_members",
        False,
        accounting.manifest_path_in_members,
    )
    log.record(
        "package_member_paths_distinct",
        observed_members,
        len(set(accounting.manifest_member_paths)),
    )

    # F2. Entry types are read from the stored ZIP metadata, not from disk.
    stored_modes = zip_entry_modes(config.source_zip)
    non_regular = [
        name
        for name, mode in sorted(stored_modes.items())
        if mode != 0 and not mode & REGULAR_FILE_TYPE_BITS
    ]
    log.record("package_member_entry_types_regular", [], non_regular)

    manifest = archive_json(config.source_zip, DOC_MANIFEST)
    members: Any = manifest["members"]
    mismatched: list[str] = []
    for member in members:
        path = str(member["path"])
        if path not in set(accounting.physical_names):
            mismatched.append(f"{path}: absent from the archive")
            continue
        payload = archive_member(config.source_zip, path)
        if len(payload) != member["byte_length"]:
            mismatched.append(
                f"{path}: byte length {len(payload)} != {member['byte_length']}"
            )
        if sha256_hex(payload) != member["sha256"]:
            mismatched.append(f"{path}: sha256 mismatch")
        if sha512_hex(payload) != member["sha512"]:
            mismatched.append(f"{path}: sha512 mismatch")
    log.record("package_member_identity_mismatches", [], mismatched)
    return emit(subcommand, log)


# ---------------------------------------------------------------------------
# F2. Exported ZIP entry modes, read from actual archive metadata.
#
# A ZIP entry records its Unix mode in the high sixteen bits of external_attr,
# including the file-type bits. The V2 export wrote 0o644 << 16, which carried
# no S_IFREG type bits and left the verifier non-executable after extraction.
# Everything below is derived from the stored entry, never from the pre-archive
# filesystem mode.
# ---------------------------------------------------------------------------

REGULAR_FILE_TYPE_BITS = 0o100000
PERMISSION_MASK = 0o7777
EXECUTABLE_ZIP_MODE = 0o755
DOCUMENT_ZIP_MODE = 0o644
OWNER_EXECUTE = 0o100
GROUP_EXECUTE = 0o010
OTHER_EXECUTE = 0o001
EXECUTABLE_PACKAGE_MEMBERS = ("verification/checkpoint_b_verifier.py",)


def zip_entry_mode(archive: Path, member: str) -> int:
    """The complete Unix mode stored for one ZIP entry, including type bits."""
    if not archive.is_file():
        raise VerifierInputError(f"required archive is absent: {archive}")
    with zipfile.ZipFile(archive) as handle:
        for info in handle.infolist():
            if info.filename == member:
                return info.external_attr >> 16
    raise VerifierInputError(f"archive {archive.name} omits member {member}")


def zip_entry_modes(archive: Path) -> dict[str, int]:
    """The complete stored Unix mode of every non-directory entry."""
    if not archive.is_file():
        raise VerifierInputError(f"required archive is absent: {archive}")
    with zipfile.ZipFile(archive) as handle:
        return {
            info.filename: info.external_attr >> 16
            for info in handle.infolist()
            if not info.is_dir()
        }


def build_package_archive(
    root: Path,
    member_names: list[str],
    destination: Path,
    executable_members: tuple[str, ...] = EXECUTABLE_PACKAGE_MEMBERS,
) -> Path:
    """Write a package archive, stamping each entry's Unix mode explicitly.

    Members named in executable_members are stored as regular files with mode
    0o755 so that the extracted file is directly executable through its shebang.
    Every other member is stored as a regular file with mode 0o644.
    """
    if destination.exists():
        raise VerifierInputError(
            f"refusing to overwrite an existing archive: {destination}"
        )
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as handle:
        for name in sorted(member_names):
            permission = (
                EXECUTABLE_ZIP_MODE if name in executable_members else DOCUMENT_ZIP_MODE
            )
            info = zipfile.ZipInfo(name, date_time=(2026, 8, 6, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (REGULAR_FILE_TYPE_BITS | permission) << 16
            handle.writestr(info, file_bytes(root / name))
    return destination


def check_exported_verifier_mode(
    log: CheckLog, archive: Path, member: str = EXECUTABLE_PACKAGE_MEMBERS[0]
) -> None:
    """F2. Confirm the exported verifier entry is an executable regular file.

    Read entirely from the stored ZIP entry metadata so that a correct
    pre-archive filesystem mode cannot mask an incorrect stored mode.
    """
    mode = zip_entry_mode(archive, member)
    permission = mode & PERMISSION_MASK
    log.record(
        "exported_verifier_entry_is_regular_file",
        True,
        bool(mode & REGULAR_FILE_TYPE_BITS),
    )
    log.record(
        "exported_verifier_owner_executable", True, bool(permission & OWNER_EXECUTE)
    )
    log.record(
        "exported_verifier_group_executable", True, bool(permission & GROUP_EXECUTE)
    )
    log.record(
        "exported_verifier_other_executable", True, bool(permission & OTHER_EXECUTE)
    )
    log.record(
        "exported_verifier_effective_mode",
        format(EXECUTABLE_ZIP_MODE, "04o"),
        format(permission, "04o"),
    )


# ---------------------------------------------------------------------------
# D1. Subcommand: verify-round-trip, exposed as ordered stages.
# ---------------------------------------------------------------------------


def extract_package(archive: Path, destination: Path) -> list[str]:
    """Stage one. Extract every member and return the extracted names."""
    with zipfile.ZipFile(archive) as handle:
        handle.extractall(destination)
        return [info.filename for info in handle.infolist() if not info.is_dir()]


def check_extracted_identity(
    log: CheckLog, members: list[dict[str, Any]], directory: Path
) -> None:
    """Stage two. Compare the first extraction against the declared manifest."""
    mismatches: list[str] = []
    for member in members:
        path = str(member["path"])
        payload = file_bytes(directory / path)
        if (
            len(payload) != member["byte_length"]
            or sha256_hex(payload) != member["sha256"]
        ):
            mismatches.append(path)
    log.record("round_trip_extracted_identity_mismatches", [], as_sorted(mismatches))


def repack_package(source: Path, names: list[str], destination: Path) -> Path:
    """Stage three. Repack the extracted tree into a new archive."""
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as handle:
        for name in sorted(names):
            handle.write(source / name, name)
    return destination


def check_round_trip_transition(
    log: CheckLog, names: list[str], first: Path, second: Path
) -> None:
    """Stage five. Compare the first and second extractions byte for byte.

    This branch is reached only by corruption introduced after the first valid
    extraction, which is what distinguishes it from the extracted-identity branch.
    """
    mismatches: list[str] = []
    for name in names:
        if file_bytes(first / name) != file_bytes(second / name):
            mismatches.append(name)
    log.record("round_trip_byte_mismatches", [], as_sorted(mismatches))


def verify_round_trip(config: Config) -> int:
    """Confirm extract, repack and re-extract preserve every payload byte exactly."""
    log = CheckLog()
    subcommand = "verify-round-trip"
    manifest = archive_json(config.source_zip, DOC_MANIFEST)
    members: list[dict[str, Any]] = list(manifest["members"])
    workspace = Path(tempfile.mkdtemp(prefix="checkpoint-b-round-trip-"))
    try:
        first = workspace / "first"
        second = workspace / "second"
        names = extract_package(config.source_zip, first)
        check_extracted_identity(log, members, first)
        repacked = repack_package(first, names, workspace / "repacked.zip")
        extract_package(repacked, second)
        check_round_trip_transition(log, names, first, second)
        log.record(
            "round_trip_repacked_member_count", len(names), len(archive_names(repacked))
        )
    finally:
        shutil.rmtree(workspace, ignore_errors=False)

    log.record("round_trip_workspace_destroyed", False, workspace.exists())
    return emit(subcommand, log)


# ---------------------------------------------------------------------------
# Dispatch.
# ---------------------------------------------------------------------------


def build_argument_parser() -> argparse.ArgumentParser:
    """Construct the verifier CLI. Pure: no I/O, no mutation, no network."""
    parser = argparse.ArgumentParser(
        prog="checkpoint_b_verifier",
        description="Exact verifier V3 for the frozen Checkpoint B module and suite package.",
    )
    parser.add_argument("subcommand", help="one of the twelve implemented subcommands")
    parser.add_argument("--source-zip", type=Path, default=DEFAULT_SOURCE_ZIP)
    parser.add_argument(
        "--checkpoint-a-zip", type=Path, default=DEFAULT_CHECKPOINT_A_ZIP
    )
    parser.add_argument("--n1-zip", type=Path, default=DEFAULT_N1_ZIP)
    parser.add_argument(
        "--authorization-zip", type=Path, default=DEFAULT_AUTHORIZATION_ZIP
    )
    parser.add_argument("--repository", type=Path, default=DEFAULT_REPOSITORY)
    parser.add_argument("--python-executable", type=Path, default=DEFAULT_PYTHON)
    return parser


def dispatch(subcommand: str, config: Config) -> int:
    """Route one known subcommand to its implementation."""
    if subcommand == "verify-source-package":
        return verify_source_package(config)
    if subcommand == "verify-governed-coordinate":
        return verify_governed_coordinate(config)
    if subcommand == "reconstruct-and-verify-s0":
        return reconstruct_and_verify_s0(config)
    if subcommand == "verify-environment-fingerprint":
        return verify_environment_fingerprint(config)
    if subcommand == "verify-module-evidence":
        return verify_module_evidence(config)
    if subcommand == "verify-suite-evidence":
        return verify_suite_evidence(config)
    if subcommand == "verify-checkpoint-a-nine-id-equality":
        return verify_checkpoint_a_nine_id_equality(config)
    if subcommand == "verify-causal-record-completeness":
        return verify_causal_record_completeness(config)
    if subcommand == "verify-census-reconciliation":
        return verify_census_reconciliation(config)
    if subcommand == "verify-nonchange":
        return verify_nonchange(config)
    if subcommand == "verify-package":
        return verify_package(config)
    return verify_round_trip(config)


def main(argv: list[str] | None = None) -> int:
    """Verify one Checkpoint B property and return its exit code."""
    parser = build_argument_parser()
    arguments = parser.parse_args(argv)
    subcommand = str(arguments.subcommand)
    if subcommand not in SUBCOMMANDS:
        return emit_unknown(subcommand)

    config = Config(
        source_zip=Path(arguments.source_zip),
        checkpoint_a_zip=Path(arguments.checkpoint_a_zip),
        n1_zip=Path(arguments.n1_zip),
        authorization_zip=Path(arguments.authorization_zip),
        repository=Path(arguments.repository),
        python_executable=Path(arguments.python_executable),
    )
    try:
        return dispatch(subcommand, config)
    except VerifierInputError as error:
        log = CheckLog()
        log.fail("governing_input", str(error))
        return emit(subcommand, log)
    except zipfile.BadZipFile as error:
        log = CheckLog()
        log.fail("archive_readable", f"not a readable ZIP archive: {error}")
        return emit(subcommand, log)
    except ElementTree.ParseError as error:
        log = CheckLog()
        log.fail(
            "junit_parseable", f"the raw JUnit document is not well formed: {error}"
        )
        return emit(subcommand, log)
    except (KeyError, ValueError, TypeError) as error:
        log = CheckLog()
        log.fail(
            "evidence_shape",
            f"{type(error).__name__} while reading required evidence: {error}",
        )
        return emit(subcommand, log)


if __name__ == "__main__":
    raise SystemExit(main())
