from pathlib import Path
import sys

from requests.exceptions import RequestException

PROJECT_ROOT = Path(__file__).resolve().parents[1]
project_root = str(PROJECT_ROOT)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from client.client import Client


SHOW_PLOTS = True


def show_first_items(title, items, n=5):
    print(f"\n=== {title} ===")
    for item in items[:n]:
        print(item)
    print(f"Total shown: {min(len(items), n)} / {len(items)}")


def show_stats(title, stats, n=5):
    print(f"\n=== {title} ===")
    for name, values in list(stats.items())[:n]:
        print(
            f"{name}: "
            f"mean={values['mean']:.2f}, "
            f"min={values['min']:.2f}, "
            f"max={values['max']:.2f}, "
            f"count={values['count']}"
        )
    print(f"Total groups: {len(stats)}")


def run_check(name, callback):
    print(f"\n[TEST] {name}")
    try:
        result = callback()
    except Exception as exc:
        print(f"[FAIL] {name}: {type(exc).__name__}: {exc}")
        raise

    print(f"[PASS] {name}")
    return result


def test_get_functions(api):
    areas = run_check("get_areas", api.get_areas)
    cantons = run_check("get_cantons", api.get_cantons)
    categories = run_check("get_categories", api.get_categories)
    observations = run_check("get_all_observations", api.get_all_observations)
    payment_categories = run_check(
        "get_direct_payment_categories",
        api.get_direct_payment_categories,
    )
    direct_payments = run_check("get_all_direct_payments", api.get_all_direct_payments)

    print("\n=== GET result counts ===")
    print(f"Areas: {len(areas)}")
    print(f"Cantons: {len(cantons)}")
    print(f"Farming categories: {len(categories)}")
    print(f"Observations: {len(observations)}")
    print(f"Direct payment categories: {len(payment_categories)}")
    print(f"Direct payment observations: {len(direct_payments)}")

    if observations:
        observation_id = observations[0].observation_id
        observation = run_check(
            f"get_observation({observation_id})",
            lambda: api.get_observation(observation_id),
        )
        print(observation)
    else:
        print("\n[SKIP] get_observation: no observations returned")

    if direct_payments:
        payment_id = direct_payments[0].direct_payment_observation_id
        direct_payment = run_check(
            f"get_direct_payment({payment_id})",
            lambda: api.get_direct_payment(payment_id),
        )
        print(direct_payment)
    else:
        print("\n[SKIP] get_direct_payment: no direct payment observations returned")

    return areas, cantons, categories, observations, payment_categories, direct_payments


def test_filter_functions(api, areas, cantons, categories, payment_categories):
    if cantons and categories and areas:
        filtered = run_check(
            "filter_observations",
            lambda: api.filter_observations(
                area_id=areas[0].area_id,
                canton_id=cantons[0].canton_id,
                category_id=categories[0].category_id,
            ),
        )
        show_first_items("Filtered farming observations", filtered)
    else:
        print("\n[SKIP] filter_observations: missing areas, cantons, or categories")

    if cantons and payment_categories:
        filtered_payments = run_check(
            "filter_direct_payment",
            lambda: api.filter_direct_payment(
                canton_id=cantons[0].canton_id,
                payment_category_id=payment_categories[0].payment_category_id,
            ),
        )
        show_first_items("Filtered direct payments", filtered_payments)
    else:
        print("\n[SKIP] filter_direct_payment: missing cantons or payment categories")


def test_stats_functions(api):
    stats_canton = run_check("stats_by_canton", api.stats_by_canton)
    show_stats("Farming stats by canton", stats_canton)

    stats_category = run_check("stats_by_category", api.stats_by_category)
    show_stats("Farming stats by category", stats_category)

    payment_stats_canton = run_check(
        "direct_payment_stats_by_canton",
        api.direct_payment_stats_by_canton,
    )
    show_stats("Direct payment stats by canton", payment_stats_canton)

    payment_stats_category = run_check(
        "direct_payment_stats_by_category",
        api.direct_payment_stats_by_category,
    )
    show_stats("Direct payment stats by category", payment_stats_category)


def show_plots(api):
    if not SHOW_PLOTS:
        print("\n[SKIP] plots: SHOW_PLOTS is False")
        return

    print("\nOpening plot windows. Close each one to continue.")
    run_check("plot_bar_by_canton", api.plot_bar_by_canton)
    run_check("plot_bar_by_category", api.plot_bar_by_category)
    run_check("plot_histogram", api.plot_histogram)
    run_check("plot_heatmap", api.plot_heatmap)
    run_check("plot_direct_payments_by_canton", api.plot_direct_payments_by_canton)
    run_check("plot_direct_payments_by_category", api.plot_direct_payments_by_category)


def main():
    api = Client("http://127.0.0.1:5000")

    print("SWISS AGRICULTURE Farm Statistics API Demo")
    print("URL: http://127.0.0.1:5000")

    try:
        areas, cantons, categories, observations, payment_categories, direct_payments = (
            test_get_functions(api)
        )
        test_filter_functions(api, areas, cantons, categories, payment_categories)
        test_stats_functions(api)
        show_plots(api)
    except RequestException as exc:
        print("\nCould not connect to the backend API.")
        print("Start it from the backend folder with:")
        print(r"  .\.venv\Scripts\python.exe app\n_app.py")
        print(f"\nOriginal error: {exc}")
        return

    print("\nAll demo checks completed.")


if __name__ == "__main__":
    main()