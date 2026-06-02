"""
find_hotels.py
──────────────
Coded tool for the Stay Advisor Agent in the Trip Advisor network.

Uses the RapidAPI Hotels4 endpoint (used by Hotels.com).
If the API key is not set, falls back to curated mock data
so you can demo the agent immediately without any setup.

Setup (optional — for live hotel data):
  1. Sign up free at https://rapidapi.com
  2. Subscribe to "Hotels4" API (free tier available)
  3. Add to .env:  RAPIDAPI_KEY=your_key_here

Without the key: realistic mock hotel data is returned for any city.
"""

import os
import requests
from neuro_san.interfaces.coded_tool import CodedTool


# ── Realistic mock hotel data (used when no API key is set) ──────────────────
# Adjust for your target cities or just let the agent reason over this.
MOCK_HOTELS = {
    "budget": {
        "name":         "City Budget Inn",
        "stars":        2,
        "price_per_night_gbp": 55,
        "rating":       7.2,
        "location":     "15-minute walk from city centre, near public transport",
        "amenities":    ["Free WiFi", "24-hour reception", "Shared kitchen"],
        "best_for":     "Solo travellers and backpackers on a tight budget",
        "breakfast":    False,
        "parking":      False,
    },
    "mid_range": {
        "name":         "Comfort & Co Hotel",
        "stars":        3,
        "price_per_night_gbp": 115,
        "rating":       8.4,
        "location":     "5-minute walk from city centre, near main attractions",
        "amenities":    ["Free WiFi", "Breakfast included", "Gym", "Luggage storage"],
        "best_for":     "Couples and families wanting comfort without overspending",
        "breakfast":    True,
        "parking":      True,
    },
    "luxury": {
        "name":         "Grand Prestige Hotel & Spa",
        "stars":        5,
        "price_per_night_gbp": 280,
        "rating":       9.2,
        "location":     "City centre, walking distance to top landmarks",
        "amenities":    ["Free WiFi", "Full breakfast", "Spa & pool", "Concierge", "Fine dining"],
        "best_for":     "Business travellers and those wanting a premium experience",
        "breakfast":    True,
        "parking":      True,
    }
}


class FindHotels(CodedTool):
    """
    Searches for hotel options at a given destination.

    Expected args from the LLM agent:
        city_name         (str) — e.g. "Paris"
        country_code      (str) — e.g. "FR"
        check_in          (str) — YYYY-MM-DD
        num_nights        (int) — number of nights
        budget_preference (str) — "budget", "mid-range", or "luxury"
    """

    def invoke(self, args: dict, sly_data: dict) -> tuple:
        city_name         = args.get("city_name", "London")
        country_code      = args.get("country_code", "GB").upper()
        check_in          = args.get("check_in", "2025-06-15")
        num_nights        = int(args.get("num_nights", 3))
        budget_preference = args.get("budget_preference", "mid-range").lower()

        api_key = os.getenv("RAPIDAPI_KEY")

        if api_key:
            # ── Live path: RapidAPI Hotels4 ──────────────────────────────
            result = self._fetch_live_hotels(
                api_key, city_name, check_in, num_nights
            )
            if result:
                return (result, sly_data)
            # Fall through to mock if live call fails

        # ── Mock path: return curated data ───────────────────────────────
        return (self._build_mock_response(city_name, country_code, check_in, num_nights, budget_preference), sly_data)

    def _fetch_live_hotels(self, api_key, city_name, check_in, num_nights):
        """Attempt to fetch real hotel data from RapidAPI Hotels4."""
        from datetime import datetime, timedelta

        check_in_dt  = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_dt = check_in_dt + timedelta(days=num_nights)
        check_out    = check_out_dt.strftime("%Y-%m-%d")

        headers = {
            "X-RapidAPI-Key":  api_key,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        }

        # Step 1: Get destination ID
        try:
            loc_resp = requests.get(
                "https://hotels4.p.rapidapi.com/locations/v3/search",
                headers=headers,
                params={"q": city_name, "locale": "en_GB", "langid": "1033", "siteid": "300000001"},
                timeout=10
            )
            loc_resp.raise_for_status()
            loc_data = loc_resp.json()
            suggestions = loc_data.get("sr", [])
            if not suggestions:
                return None
            dest_id = suggestions[0].get("gaiaId") or suggestions[0].get("regionId")
            if not dest_id:
                return None
        except Exception:
            return None

        # Step 2: Search hotels
        try:
            hotel_resp = requests.post(
                "https://hotels4.p.rapidapi.com/properties/v2/list",
                headers=headers,
                json={
                    "currency":        "GBP",
                    "eapid":           1,
                    "locale":          "en_GB",
                    "siteId":          300000001,
                    "destination":     {"regionId": str(dest_id)},
                    "checkInDate":     {"day": int(check_in.split("-")[2]), "month": int(check_in.split("-")[1]), "year": int(check_in.split("-")[0])},
                    "checkOutDate":    {"day": int(check_out.split("-")[2]), "month": int(check_out.split("-")[1]), "year": int(check_out.split("-")[0])},
                    "rooms":           [{"adults": 2}],
                    "resultsStartingIndex": 0,
                    "resultsSize":     10,
                    "sort":            "REVIEW",
                },
                timeout=15
            )
            hotel_resp.raise_for_status()
            hotel_data = hotel_resp.json()
            hotels = hotel_data.get("data", {}).get("propertySearch", {}).get("properties", [])
            if not hotels:
                return None
        except Exception:
            return None

        # Build result from live data
        lines = [
            f"LIVE HOTEL RESULTS — {city_name.upper()}, {country_code}",
            f"Check-in: {check_in} | {num_nights} nights",
            ""
        ]
        for i, h in enumerate(hotels[:6], 1):
            name   = h.get("name", "Unknown")
            price  = h.get("price", {}).get("lead", {}).get("formatted", "N/A")
            rating = h.get("reviews", {}).get("score", "N/A")
            lines.append(f"{i}. {name} | {price}/night | Rating: {rating}/10")

        return "\n".join(lines)

    def _build_mock_response(self, city_name, country_code, check_in, num_nights, budget_preference):
        """Build a realistic mock hotel response for demonstration."""
        lines = [
            f"ACCOMMODATION OPTIONS — {city_name.upper()}, {country_code}",
            f"Check-in: {check_in} | {num_nights} nights",
            f"Showing: Budget / Mid-range / Luxury options",
            "=" * 60,
            ""
        ]

        for tier_key, tier_label in [("budget", "BUDGET"), ("mid_range", "MID-RANGE"), ("luxury", "LUXURY")]:
            h           = MOCK_HOTELS[tier_key]
            total_cost  = h["price_per_night_gbp"] * num_nights
            star_str    = "★" * h["stars"] + "☆" * (5 - h["stars"])
            breakfast   = "✅ Breakfast included" if h["breakfast"] else "❌ Breakfast not included"
            parking     = "✅ Parking available" if h["parking"] else "❌ No parking"
            amenities   = " | ".join(h["amenities"])
            recommended = " ← RECOMMENDED FOR YOU" if (
                (tier_key == "budget" and "budget" in budget_preference) or
                (tier_key == "mid_range" and "mid" in budget_preference) or
                (tier_key == "luxury" and "luxury" in budget_preference)
            ) else ""

            lines += [
                f"🏨 [{tier_label}]{recommended}",
                f"   {h['name']}  {star_str}",
                f"   📍 {h['location']}",
                f"   💰 £{h['price_per_night_gbp']}/night  →  £{total_cost} total for {num_nights} nights",
                f"   ⭐ Guest rating: {h['rating']}/10",
                f"   ✅ Amenities: {amenities}",
                f"   {breakfast}  |  {parking}",
                f"   👤 Best for: {h['best_for']}",
                ""
            ]

        lines.append(
            "NOTE: These are illustrative options. "
            "Add RAPIDAPI_KEY to .env for live hotel prices and availability."
        )
        return "\n".join(lines)
