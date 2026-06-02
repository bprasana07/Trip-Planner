"""
find_attractions.py
───────────────────
Coded tool for the Activity Planner Agent in the Trip Advisor network.
Uses Foursquare Places API v3 (free tier — no credit card required).

Setup:
  1. Go to https://foursquare.com/developer
  2. Create a free account and a new Project
  3. Copy your API Key
  4. Add to your .env file:  FOURSQUARE_API_KEY=your_key_here

Free tier: 100,000 API calls/month.
API docs: https://docs.foursquare.com/developer/reference/place-search
"""

import os
import requests
from neuro_san.interfaces.coded_tool import CodedTool


# ── Foursquare v3 category IDs → label and indoor/outdoor classification ──────
CATEGORIES = {
    # INDOOR
    "10027": {"label": "Museum",               "type": "INDOOR"},
    "10024": {"label": "Art Gallery",           "type": "INDOOR"},
    "10025": {"label": "Performing Arts",       "type": "INDOOR"},
    "10026": {"label": "Movie Theatre",         "type": "INDOOR"},
    "10004": {"label": "Aquarium",              "type": "INDOOR"},
    "10044": {"label": "Science Museum",        "type": "INDOOR"},
    "10034": {"label": "Historic Site",         "type": "INDOOR"},
    "13000": {"label": "Restaurant / Food",     "type": "INDOOR"},
    "13065": {"label": "Cafe",                  "type": "INDOOR"},
    "10056": {"label": "Shopping Mall",         "type": "INDOOR"},
    # OUTDOOR
    "16032": {"label": "Park / Garden",         "type": "OUTDOOR"},
    "16008": {"label": "Beach",                 "type": "OUTDOOR"},
    "16020": {"label": "Historic Landmark",     "type": "OUTDOOR"},
    "16019": {"label": "Monument",              "type": "OUTDOOR"},
    "16035": {"label": "Scenic Viewpoint",      "type": "OUTDOOR"},
    "16007": {"label": "Castle / Fortress",     "type": "OUTDOOR"},
    "18000": {"label": "Sports & Recreation",   "type": "OUTDOOR"},
    "16000": {"label": "Outdoors & Nature",     "type": "OUTDOOR"},
    "10000": {"label": "Entertainment",         "type": "OUTDOOR"},
}

ALL_CATEGORY_IDS = ",".join(CATEGORIES.keys())

# Maps user interest keywords to Foursquare category IDs
INTEREST_MAP = {
    "art":       ["10024", "10027"],
    "history":   ["10034", "16020", "16019", "16007"],
    "food":      ["13000", "13065"],
    "nature":    ["16032", "16008", "16000", "16035"],
    "adventure": ["18000", "16000"],
    "culture":   ["10025", "10027", "10034"],
    "shopping":  ["10056"],
    "music":     ["10025"],
}


class FindAttractions(CodedTool):
    """
    Fetches top tourist attractions for a given city using Foursquare Places API v3.

    Expected args from the LLM agent:
        city_name    (str) - e.g. "Paris"
        country_code (str) - e.g. "FR"
        limit        (str) - max attractions to return (default "20")
        interests    (str) - optional comma-separated interests e.g. "history,art,food"
    """

    BASE_URL = "https://api.foursquare.com/v3/places/search"

    def invoke(self, args: dict, sly_data: dict) -> tuple:
        city_name    = args.get("city_name", "London")
        country_code = args.get("country_code", "GB").upper()
        limit        = int(args.get("limit", 20))
        interests    = args.get("interests", "")

        api_key = os.getenv("FOURSQUARE_API_KEY")
        if not api_key:
            return (
                "ERROR: FOURSQUARE_API_KEY is not set. "
                "Sign up free at foursquare.com/developer and add the key to your .env file.",
                sly_data,
            )

        # Build priority category IDs from user interests
        interest_list = [i.strip().lower() for i in interests.split(",") if i.strip()]
        priority_ids  = set()
        for interest in interest_list:
            priority_ids.update(INTEREST_MAP.get(interest, []))

        headers = {
            "Authorization": api_key,
            "Accept":        "application/json",
        }
        params = {
            "near":       f"{city_name}, {country_code}",
            "categories": ALL_CATEGORY_IDS,
            "limit":      min(limit * 2, 50),   # fetch extra, trim later
            "sort":       "POPULARITY",
            "fields":     "name,categories,rating,popularity,location,distance",
        }

        # ── Call Foursquare ───────────────────────────────────────────────
        try:
            response = requests.get(
                self.BASE_URL, headers=headers, params=params, timeout=15
            )
            if response.status_code == 401:
                return (
                    "ERROR: Invalid Foursquare API key. Please check FOURSQUARE_API_KEY.",
                    sly_data,
                )
            if response.status_code == 400:
                return (
                    f"ERROR: City '{city_name}, {country_code}' not recognised by Foursquare.",
                    sly_data,
                )
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.ConnectionError:
            return (
                "ERROR: Could not connect to Foursquare. Check your internet connection.",
                sly_data,
            )
        except Exception as exc:
            return (f"ERROR fetching attractions: {str(exc)}", sly_data)

        places = data.get("results", [])
        if not places:
            return (
                f"No attractions found for {city_name}, {country_code}. "
                "Try a different city name or country code.",
                sly_data,
            )

        # ── Parse and classify results ────────────────────────────────────
        results    = []
        seen_names = set()

        for place in places:
            name = place.get("name", "").strip()
            if not name or name in seen_names:
                continue
            seen_names.add(name)

            place_cats     = place.get("categories", [])
            category_label = "Point of Interest"
            venue_type     = "OUTDOOR"
            cat_id_match   = None

            for cat in place_cats:
                cat_id = str(cat.get("id", ""))
                if cat_id in CATEGORIES:
                    category_label = CATEGORIES[cat_id]["label"]
                    venue_type     = CATEGORIES[cat_id]["type"]
                    cat_id_match   = cat_id
                    break

            rating     = place.get("rating")
            rating_str = f"{rating:.1f}/10" if rating else "Not rated"
            distance   = place.get("distance", 0)
            dist_str   = f"{distance}m from centre" if distance else ""
            matches    = (
                cat_id_match in priority_ids
                if (priority_ids and cat_id_match)
                else False
            )

            results.append({
                "name":             name,
                "category":         category_label,
                "venue_type":       venue_type,
                "rating":           rating or 0,
                "rating_str":       rating_str,
                "distance":         dist_str,
                "matches_interest": matches,
            })

        # Interest matches first, then by rating descending
        results.sort(key=lambda x: (-int(x["matches_interest"]), -x["rating"]))
        results = results[:limit]

        if not results:
            return (f"No suitable attractions found for {city_name}.", sly_data)

        # ── Build output string ───────────────────────────────────────────
        indoor_count  = sum(1 for r in results if r["venue_type"] == "INDOOR")
        outdoor_count = sum(1 for r in results if r["venue_type"] == "OUTDOOR")

        lines = [
            f"ATTRACTIONS IN {city_name.upper()}, {country_code}",
            f"Total: {len(results)}  |  Indoor: {indoor_count}  |  Outdoor: {outdoor_count}",
            f"Source: Foursquare Places API",
            "",
        ]
        for i, r in enumerate(results, 1):
            interest_tag = "  * MATCHES YOUR INTERESTS" if r["matches_interest"] else ""
            dist_tag     = f"  |  {r['distance']}" if r["distance"] else ""
            lines.append(
                f"{i:2}. [{r['venue_type']:7}]  {r['name']}"
                f"  |  {r['category']}"
                f"  |  Rating: {r['rating_str']}"
                f"{dist_tag}{interest_tag}"
            )

        return ("\n".join(lines), sly_data)
