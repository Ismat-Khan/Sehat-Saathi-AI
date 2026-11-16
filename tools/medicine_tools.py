
import requests


def search_medicine(medicine_name):

    try:
        url = "https://api.fda.gov/drug/label.json"

        params = {
            "search": f'openfda.brand_name:"{medicine_name}"',
            "limit": 2
        }

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            return "No matching FDA label information found."

        results = response.json().get("results", [])

        if not results:
            return "No matching medicine record found."

        medicine = results[0]

        return {
            "brand": medicine.get("openfda", {}).get(
                "brand_name", []
            ),
            "generic": medicine.get("openfda", {}).get(
                "generic_name", []
            ),
            "uses": medicine.get("indications_and_usage", []),
            "warnings": medicine.get("warnings", []),
            "side_effects": medicine.get(
                "adverse_reactions", []
            )
        }

    except Exception as error:
        return f"Medicine database error: {error}"
