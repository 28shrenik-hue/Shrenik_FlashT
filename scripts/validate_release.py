from __future__ import annotations

import argparse
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services import learning_service
from services.excel_service import ExcelService
from version import __version__


EXPECTED_VERSION = "1.0.0-rc18"
EXPECTED_PREPARED = {
    "Risk & Decision Making": "Risk-Informed Decision Making",
    "BCBS 239 & Data Governance": "BCBS 239 & Data Governance",
    "Human-in-the-loop AI controls": "Human-in-the-Loop AI Controls",
    "Issues & Errors Management": "Issues & Errors Management",
    "Legal-obligation impact assessments": "Legal-Obligation Impact Assessment",
    "Alternative investments and portfolio diversification": (
        "Understanding Alternative Investments"
    ),
}
REQUIRED_FILES = (
    "START_FLASHTILE_MAC.command",
    "main.py",
    "version.py",
    "requirements.txt",
    "assets/branding/FlashTile_3D_Logo.png",
    "ui/qml/Main.qml",
    "services/learning_service.py",
    "services/excel_service.py",
)


def check_source_tree() -> None:
    if __version__ != EXPECTED_VERSION:
        raise RuntimeError(f"Expected {EXPECTED_VERSION}, found {__version__}")
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f"Required release file is missing or empty: {relative}")
    if len(learning_service.PRIMARY_TOPICS) != 3:
        raise RuntimeError("The three flagship learning areas changed unexpectedly")
    if sum(len(items) for items in learning_service.LESSONS.values()) != 25:
        raise RuntimeError("The release must contain twenty-five reviewed lessons")
    if learning_service.PREPARED_LEARNING_TOPICS.keys() != EXPECTED_PREPARED.keys():
        raise RuntimeError("Prepared learning-topic labels do not match RC18")


def check_learning_and_persistence() -> None:
    with TemporaryDirectory() as folder:
        workbook_path = Path(folder) / "FlashTile.xlsx"
        original_store = learning_service.ExcelService
        learning_service.ExcelService = lambda: ExcelService(workbook_path)
        try:
            learning = learning_service.LearningService()
            if learning.appVersion != EXPECTED_VERSION:
                raise RuntimeError("The UI service does not expose the RC18 version")
            if len(learning.topLearningItems) != 9:
                raise RuntimeError("Main learning selector must contain nine choices")
            for subject, expected_title in EXPECTED_PREPARED.items():
                if not learning.openPreparedLearningTopic(subject):
                    raise RuntimeError(f"Prepared topic did not open: {subject}")
                if learning.title != expected_title:
                    raise RuntimeError(
                        f"Prepared topic routed incorrectly: {subject} -> {learning.title}"
                    )

            result = learning.createCustomLearningPath(
                "Advanced supply-chain forecasting"
            )
            if not result.startswith("REQUESTED|"):
                raise RuntimeError("Unavailable custom topic was not queued")
            duplicate = learning.createCustomLearningPath(
                "  advanced supply-chain forecasting  "
            )
            if "already" not in duplicate.casefold():
                raise RuntimeError("Duplicate topic request was not detected")

            learning.saveWindowPosition(48, 96)
            resumed = learning_service.LearningService()
            if resumed.store.window_position() != (48, 96):
                raise RuntimeError("Window position did not survive relaunch")
        finally:
            learning_service.ExcelService = original_store


def check_package(package: Path) -> None:
    if not package.is_file():
        raise RuntimeError(f"Release package not found: {package}")
    with ZipFile(package) as archive:
        names = set(archive.namelist())
        missing = [name for name in REQUIRED_FILES if name not in names]
        if missing:
            raise RuntimeError(f"Release package is missing: {', '.join(missing)}")
        packaged_version = archive.read("version.py").decode("utf-8")
        if EXPECTED_VERSION not in packaged_version:
            raise RuntimeError("Release package contains the wrong version")
        packaged_learning = archive.read("services/learning_service.py").decode(
            "utf-8"
        )
        for subject in EXPECTED_PREPARED:
            if subject not in packaged_learning:
                raise RuntimeError(f"Release package is missing topic: {subject}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a FlashTile release")
    parser.add_argument("--package", type=Path)
    args = parser.parse_args()

    check_source_tree()
    print("PASS  Source tree and version")
    check_learning_and_persistence()
    print("PASS  Learning routes, requests, and persistence")
    if args.package:
        check_package(args.package)
        print(f"PASS  Release package: {args.package}")
    print("FlashTile release validation complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
