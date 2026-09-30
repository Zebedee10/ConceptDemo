from pathlib import Path


# ============================================================
# APPLICATION PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

SAMPLE_DATA_FILE = (
    DATA_DIR / "Sample_data.csv"
)

SAMPLE_EXCEPTIONS_FILE = (
    DATA_DIR / "Sample_exceptions.csv"
)

SAMPLE_ADRS_FILE = (
    DATA_DIR / "Sample_adrs.csv"
)

SAMPLE_CHANGE_PORTFOLIOS_FILE = (
    DATA_DIR / "Sample_change_portfolios.csv"
)

SAMPLE_PATTERNS_FILE = (
    DATA_DIR / "Sample_patterns.csv"
)

SAMPLE_COMMERCIAL_RENEWALS_FILE = (
    DATA_DIR / "Sample_commercial_renewals.csv"
)

SAMPLE_COMMERCIAL_DIVISION_ROADMAPS_FILE = (
    DATA_DIR / "Sample_commercial_division_roadmaps.csv"
)


# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = "Architecture Governance Navigator"

APP_SUBTITLE = "Architecture Governance Navigator"


# ============================================================
# DATA SOURCE
# ============================================================

DATA_SOURCE = "csv"