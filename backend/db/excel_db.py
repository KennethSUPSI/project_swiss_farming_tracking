from pathlib import Path
import sys

import pandas as pd
from flask import Flask

# --------------------------------------------------
# PATH SETUP
# --------------------------------------------------

# CURRENT_DIR = backend/db
CURRENT_DIR = Path(__file__).resolve().parent

# BACKEND_DIR = backend
BACKEND_DIR = CURRENT_DIR.parent

# Allows Python to import from backend/
sys.path.append(str(BACKEND_DIR))

from db.database import (
    db,
    Area,
    Canton,
    FarmingCategory,
    Observation,
    DirectPaymentCategory,
    DirectPaymentObservation
)

# Files inside backend/db/
FIRST_EXCEL_FILE = CURRENT_DIR / "dataset_.xlsx"
SECOND_EXCEL_FILE = CURRENT_DIR / "direct_payments.xlsx"

DB_FILE = CURRENT_DIR / "data.db"

CURRENT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# CHECK FILES
# --------------------------------------------------

if not FIRST_EXCEL_FILE.exists():
    raise FileNotFoundError(f"First Excel file not found: {FIRST_EXCEL_FILE}")

if not SECOND_EXCEL_FILE.exists():
    raise FileNotFoundError(f"Second Excel file not found: {SECOND_EXCEL_FILE}")

print("First Excel file:", FIRST_EXCEL_FILE)
print("Second Excel file:", SECOND_EXCEL_FILE)
print("Database file:", DB_FILE)


# --------------------------------------------------
# FLASK APP SETUP ONLY FOR DATABASE IMPORT
# --------------------------------------------------

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE.as_posix()}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def get_or_create(model, **kwargs):
    item = model.query.filter_by(**kwargs).first()

    if item is None:
        item = model(**kwargs)
        db.session.add(item)
        db.session.flush()

    return item


# --------------------------------------------------
# IMPORT FIRST EXCEL FILE
# dataset_.xlsx
# --------------------------------------------------

def import_farm_statistics_excel():
    raw = pd.read_excel(FIRST_EXCEL_FILE, header=None)

    # Excel structure:
    # row index 3 = category / indicator names
    # row index 4 = area names
    # row index 5 onward = canton data
    indicators = raw.iloc[3]
    areas = raw.iloc[4]
    data = raw.iloc[5:].copy()

    # First column contains canton names
    data = data.rename(columns={0: "canton"})

    inserted = 0
    skipped = 0

    for col in data.columns[1:]:
        category_name = indicators[col]
        area_name = areas[col]

        if pd.isna(category_name) or pd.isna(area_name):
            skipped += 1
            continue

        category_name = str(category_name).strip()
        area_name = str(area_name).strip()

        category = get_or_create(FarmingCategory, name=category_name)
        area = get_or_create(Area, name=area_name)

        for _, row in data.iterrows():
            canton_name = row["canton"]
            value = row[col]

            if pd.isna(canton_name) or pd.isna(value):
                skipped += 1
                continue

            canton_name = str(canton_name).strip()

            canton = get_or_create(Canton, name=canton_name)

            observation = Observation(
                area=area,
                canton=canton,
                category=category,
                value=float(value)
            )

            db.session.add(observation)
            inserted += 1

    print("Farm statistics import completed.")
    print(f"Inserted farm observations: {inserted}")
    print(f"Skipped farm cells/columns: {skipped}")


# --------------------------------------------------
# IMPORT SECOND EXCEL FILE
# direct_payments.xlsx
# --------------------------------------------------

def import_direct_payments_excel():
    raw = pd.read_excel(SECOND_EXCEL_FILE, header=None)

    # Second Excel structure:
    # row index 1 = headers
    # column 0 = canton names
    # column 1 onward = payment categories
    headers = raw.iloc[1]
    data = raw.iloc[4:].copy()

    data = data.rename(columns={0: "canton"})

    inserted = 0
    skipped = 0

    for col in data.columns[1:]:
        payment_category_name = headers[col]

        if pd.isna(payment_category_name):
            skipped += 1
            continue

        payment_category_name = str(payment_category_name).strip().replace("\n", " ")

        payment_category = get_or_create(
            DirectPaymentCategory,
            name=payment_category_name
        )

        for _, row in data.iterrows():
            canton_name = row["canton"]
            value = row[col]

            if pd.isna(canton_name) or pd.isna(value):
                skipped += 1
                continue

            canton_name = str(canton_name).strip()

            canton = get_or_create(Canton, name=canton_name)

            direct_payment_observation = DirectPaymentObservation(
                canton=canton,
                payment_category=payment_category,
                value=float(value)
            )

            db.session.add(direct_payment_observation)
            inserted += 1

    print("Direct payments import completed.")
    print(f"Inserted direct payment observations: {inserted}")
    print(f"Skipped direct payment cells/columns: {skipped}")


# --------------------------------------------------
# MAIN IMPORT FUNCTION
# --------------------------------------------------

def import_excel_to_database():
    with app.app_context():

        # WARNING:
        # This deletes the old database and rebuilds everything.
        # This is okay if you want a clean import from both Excel files.
        db.drop_all()
        db.create_all()

        import_farm_statistics_excel()
        import_direct_payments_excel()

        db.session.commit()

        print("All Excel files imported successfully.")


if __name__ == "__main__":
    import_excel_to_database()