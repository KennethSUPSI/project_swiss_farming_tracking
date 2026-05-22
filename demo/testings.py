
from pathlib import Path
import sys

from requests.exceptions import RequestException

PROJECT_ROOT = Path(__file__).resolve().parents[1]
project_root = str(PROJECT_ROOT)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from client.client import Client


def show_first_items(title, items, n=5):
    print(f"\n=== {title} ===")
    for item in items[:n]:
        print(item)
    print(f"Total shown: {min(len(items), n)} / {len(items)}")


def main():
    api = Client("http://127.0.0.1:5000")

    print("SWISS AGRICULTURE Farm Statistics API Demo")
    print(" URL: http://127.0.0.1:5000")

    try:
        areas = api.get_areas()
        cantons = api.get_cantons()
        categories = api.get_categories()
        payment_categories = api.get_direct_payment_categories()
        observations = api.get_all_observations()
        direct_payments = api.get_all_direct_payments()
    except RequestException as exc:
        print("\nCould not connect to the backend API.")
        print("Start it from the backend folder with:")
        print(r"  .\.venv\Scripts\python.exe app\n_app.py")
        print(f"\nOriginal error: {exc}")
        return

    print(f"Areas: {len(areas)}")
    print(f"Cantons: {len(cantons)}")
    print(f"Farming categories: {len(categories)}")
    print(f"Observations: {len(observations)}")
    print(f"Direct payment categories: {len(payment_categories)}")
    print(f"Direct payment observations: {len(direct_payments)}")

    if cantons and categories and areas:
        filtered = api.filter_observations(
            area_id=areas[0].area_id,
            canton_id=cantons[1].canton_id,
            category_id=categories[0].category_id,
        )
        show_first_items("Filtered farming observations", filtered)

    if cantons and payment_categories:
        filtered_payments = api.filter_direct_payment(
            canton_id=cantons[1].canton_id,
            payment_category_id=payment_categories[0].payment_category_id,
        )
        show_first_items("Filtered direct payments", filtered_payments)

    api.plot_bar_by_canton()
    api.plot_bar_by_category()
    api.plot_histogram()
    api.plot_heatmap()
    api.plot_direct_payments_by_canton()
    api.plot_direct_payments_by_category()


if __name__ == "__main__":
    main()
