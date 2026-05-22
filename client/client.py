import collections
from typing import Optional

import matplotlib.pyplot as plt
import requests

if __package__:
    from .exceptions import *
    from .models.models import (
        Area,
        Canton,
        DirectPaymentCategory,
        DirectPaymentObservation,
        FarmingCategory,
        Observation,
    )
else:
    from exceptions import *
    from models.models import (
        Area,
        Canton,
        DirectPaymentCategory,
        DirectPaymentObservation,
        FarmingCategory,
        Observation,
    )


class Client:
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _handle_response(self, response):
        if response.status_code == 404:
            raise NotFoundError(response.json().get("error"))
        if response.status_code == 400:
            raise ValidationError(response.json().get("error"))
        if response.status_code >= 500:
            raise ServerError("Server error")
        return response.json()

    def _exclude_summary(self, observations: list[Observation]) -> list[Observation]:
        return [o for o in observations if o.canton != "Switzerland"]

    def get_areas(self) -> list[Area]:
        r = self.session.get(f"{self.base_url}/areas")
        return [Area(**a) for a in self._handle_response(r)]

    def create_area(self, name: str) -> Area:
        r = self.session.post(f"{self.base_url}/areas", json={"name": name})
        data = self._handle_response(r)
        return Area(**data["area"])

    def update_area(self, area_id: int, name: str) -> Area:
        r = self.session.put(f"{self.base_url}/areas/{area_id}", json={"name": name})
        data = self._handle_response(r)
        return Area(**data["area"])

    def delete_area(self, area_id: int) -> None:
        r = self.session.delete(f"{self.base_url}/areas/{area_id}")
        self._handle_response(r)

    def get_cantons(self) -> list[Canton]:
        r = self.session.get(f"{self.base_url}/cantons")
        return [Canton(**c) for c in self._handle_response(r)]

    def get_categories(self) -> list[FarmingCategory]:
        r = self.session.get(f"{self.base_url}/categories")
        return [FarmingCategory(**c) for c in self._handle_response(r)]

    def get_observation(self, observation_id: int) -> Observation:
        r = self.session.get(f"{self.base_url}/observations/{observation_id}")
        return Observation(**self._handle_response(r))

    def get_all_observations(self) -> list[Observation]:
        r = self.session.get(f"{self.base_url}/observations")
        return [Observation(**o) for o in self._handle_response(r)]

    def create_observation(
        self,
        area_id: int,
        canton_id: int,
        category_id: int,
        value: Optional[float] = None,
    ) -> Observation:
        r = self.session.post(
            f"{self.base_url}/observations",
            json={
                "area_id": area_id,
                "canton_id": canton_id,
                "category_id": category_id,
                "value": value,
            },
        )
        data = self._handle_response(r)
        return self.get_observation(data["observation_id"])

    def update_observation(self, observation_id: int, **kwargs) -> None:
        r = self.session.put(f"{self.base_url}/observations/{observation_id}", json=kwargs)
        self._handle_response(r)

    def delete_observation(self, observation_id: int) -> None:
        r = self.session.delete(f"{self.base_url}/observations/{observation_id}")
        self._handle_response(r)

    def filter_observations(
        self,
        area_id=None,
        canton_id=None,
        category_id=None,
        min_value=None,
        max_value=None,
    ) -> list[Observation]:
        params = {}
        if area_id:
            params["area_id"] = area_id
        if canton_id:
            params["canton_id"] = canton_id
        if category_id:
            params["category_id"] = category_id
        if min_value is not None:
            params["min_value"] = min_value
        if max_value is not None:
            params["max_value"] = max_value

        r = self.session.get(f"{self.base_url}/observations/filter", params=params)
        return [Observation(**o) for o in self._handle_response(r)]

    def stats_by_canton(self) -> dict:
        observations = self._exclude_summary(self.get_all_observations())
        result = {}
        for o in observations:
            if o.value is None:
                continue
            result.setdefault(o.canton, []).append(o.value)
        return {
            name: {
                "mean": sum(vals) / len(vals),
                "min": min(vals),
                "max": max(vals),
                "count": len(vals),
            }
            for name, vals in result.items()
        }

    def stats_by_category(self) -> dict:
        observations = self._exclude_summary(self.get_all_observations())
        result = {}
        for o in observations:
            if o.value is None:
                continue
            result.setdefault(o.category, []).append(o.value)
        return {
            name: {
                "mean": sum(vals) / len(vals),
                "min": min(vals),
                "max": max(vals),
                "count": len(vals),
            }
            for name, vals in result.items()
        }

    def plot_bar_by_canton(self):
        stats = self.stats_by_canton()
        names = list(stats.keys())
        means = [stats[n]["mean"] for n in names]

        plt.figure(figsize=(10, 5))
        plt.bar(names, means)
        plt.title("Average Observation Value by Canton")
        plt.xlabel("Canton")
        plt.ylabel("Mean Value")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_bar_by_category(self):
        stats = self.stats_by_category()
        names = list(stats.keys())
        means = [stats[n]["mean"] for n in names]

        plt.figure(figsize=(10, 5))
        plt.bar(names, means, color="green")
        plt.title("Average Observation Value by Category")
        plt.xlabel("Category")
        plt.ylabel("Mean Value")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_histogram(self, bins: int = 30):
        observations = self._exclude_summary(self.get_all_observations())
        values = [o.value for o in observations if o.value is not None]

        plt.figure(figsize=(8, 5))
        plt.hist(values, bins=bins, color="steelblue", edgecolor="white", log=True)
        plt.title("Distribution of Observation Values (log scale)")
        plt.xlabel("Value")
        plt.ylabel("Frequency (log)")
        plt.tight_layout()
        plt.show()

    def plot_heatmap(self):
        observations = self._exclude_summary(self.get_all_observations())

        data = collections.defaultdict(lambda: collections.defaultdict(list))
        for o in observations:
            if o.value is not None:
                data[o.area][o.category].append(o.value)

        area_names = list(data.keys())
        cat_names = list({o.category for o in observations})
        matrix = [
            [sum(data[a][c]) / len(data[a][c]) if data[a][c] else 0 for c in cat_names]
            for a in area_names
        ]

        plt.figure(figsize=(14, 8))
        plt.imshow(matrix, aspect="auto")
        plt.colorbar(label="Mean Value")
        plt.xticks(range(len(cat_names)), cat_names, rotation=45)
        plt.yticks(range(len(area_names)), area_names)
        plt.title("Mean Value: Area x Category")
        plt.tight_layout()
        plt.show()

    def get_direct_payment_categories(self) -> list[DirectPaymentCategory]:
        r = self.session.get(f"{self.base_url}/direct_payment_categories")
        return [DirectPaymentCategory(**c) for c in self._handle_response(r)]

    def get_all_direct_payments(self) -> list[DirectPaymentObservation]:
        r = self.session.get(f"{self.base_url}/direct_payments")
        return [DirectPaymentObservation(**o) for o in self._handle_response(r)]

    def get_direct_payment(self, observation_id: int) -> DirectPaymentObservation:
        r = self.session.get(f"{self.base_url}/direct_payments/{observation_id}")
        return DirectPaymentObservation(**self._handle_response(r))

    def create_direct_payment(
        self,
        canton_id: int,
        payment_category_id: int,
        value: Optional[float] = None,
    ) -> DirectPaymentObservation:
        r = self.session.post(
            f"{self.base_url}/direct_payments",
            json={
                "canton_id": canton_id,
                "payment_category_id": payment_category_id,
                "value": value,
            },
        )
        data = self._handle_response(r)
        return self.get_direct_payment(data["direct_payment_observation_id"])

    def delete_direct_payment(self, observation_id: int) -> None:
        r = self.session.delete(f"{self.base_url}/direct_payments/{observation_id}")
        self._handle_response(r)

    def filter_direct_payment(
        self,
        canton_id=None,
        payment_category_id=None,
        min_val=None,
        max_val=None,
    ) -> list[DirectPaymentObservation]:
        params = {}
        if canton_id:
            params["canton_id"] = canton_id
        if payment_category_id:
            params["payment_category_id"] = payment_category_id
        if min_val is not None:
            params["min_val"] = min_val
        if max_val is not None:
            params["max_val"] = max_val
        r = self.session.get(f"{self.base_url}/direct_payments/filter", params=params)
        return [DirectPaymentObservation(**o) for o in self._handle_response(r)]

    def direct_payment_stats_by_canton(self) -> dict:
        observations = [
            o for o in self.get_all_direct_payments()
            if o.canton != "Switzerland"
        ]
        result = {}
        for o in observations:
            if o.value is None:
                continue
            result.setdefault(o.canton, []).append(o.value)
        return {
            name: {
                "mean": sum(vals) / len(vals),
                "min": min(vals),
                "max": max(vals),
                "count": len(vals),
            }
            for name, vals in result.items()
        }

    def direct_payment_stats_by_category(self) -> dict:
        observations = self.get_all_direct_payments()
        result = {}
        for o in observations:
            if o.value is None:
                continue
            result.setdefault(o.payment_category, []).append(o.value)
        return {
            name: {
                "mean": sum(vals) / len(vals),
                "min": min(vals),
                "max": max(vals),
                "count": len(vals),
            }
            for name, vals in result.items()
        }

    def plot_direct_payments_by_canton(self):
        stats = self.direct_payment_stats_by_canton()
        names = list(stats.keys())
        means = [stats[n]["mean"] for n in names]

        plt.figure(figsize=(12, 5))
        plt.bar(names, means, color="orange")
        plt.title("Average Direct Payment by Canton")
        plt.xlabel("Canton")
        plt.ylabel("Mean Value")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_direct_payments_by_category(self):
        stats = self.direct_payment_stats_by_category()
        names = list(stats.keys())
        means = [stats[n]["mean"] for n in names]

        plt.figure(figsize=(12, 5))
        plt.bar(names, means, color="purple")
        plt.title("Average Direct Payment by Category")
        plt.xlabel("Category")
        plt.ylabel("Mean Value")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
