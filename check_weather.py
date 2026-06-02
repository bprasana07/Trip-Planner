"""
check_weather.py
────────────────
Coded tool for the Weather Agent in the Trip Advisor network.
Calls the OpenWeatherMap 5-day forecast API (free tier).

Setup:
  1. Sign up free at https://openweathermap.org/api
  2. Get your API key from your account dashboard
  3. Add to your .env file:  OPENWEATHERMAP_API_KEY=your_key_here

API used: api.openweathermap.org/data/2.5/forecast  (free, 5-day/3-hour)
"""

import os
import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from neuro_san.interfaces.coded_tool import CodedTool


class CheckWeather(CodedTool):
    """
    Fetches a multi-day weather forecast for a given city.

    Expected args from the LLM agent:
        city_name   (str)  — e.g. "Paris"
        country_code (str) — e.g. "FR"  (ISO 3166-1 alpha-2)
        start_date  (str)  — e.g. "2025-06-15"  (YYYY-MM-DD)
        num_days    (int)  — number of days, e.g. 5
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

    def invoke(self, args: dict, sly_data: dict) -> tuple:
        """
        Synchronous invoke. Neuro SAN will call this automatically.
        Returns (result_string, sly_data).
        """
        city_name    = args.get("city_name", "London")
        country_code = args.get("country_code", "GB")
        start_date   = args.get("start_date", datetime.today().strftime("%Y-%m-%d"))
        num_days     = int(args.get("num_days", 5))

        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not api_key:
            return (
                "ERROR: OPENWEATHERMAP_API_KEY environment variable is not set. "
                "Please sign up at openweathermap.org and add the key to your .env file.",
                sly_data
            )

        # ── Call OpenWeatherMap API ───────────────────────────────────────
        params = {
            "q":     f"{city_name},{country_code}",
            "appid": api_key,
            "units": "metric",   # Celsius
            "cnt":   num_days * 8,  # 8 x 3-hour slots per day
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                return ("ERROR: Invalid OpenWeatherMap API key. Please check your key.", sly_data)
            elif response.status_code == 404:
                return (f"ERROR: City '{city_name}, {country_code}' not found. Check the city name.", sly_data)
            else:
                return (f"ERROR fetching weather: {str(e)}", sly_data)
        except requests.exceptions.ConnectionError:
            return ("ERROR: Could not connect to weather service. Check your internet connection.", sly_data)

        # ── Parse the forecast data ───────────────────────────────────────
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt   = start_dt + timedelta(days=num_days)

        # Group forecasts by day
        daily_data = defaultdict(list)
        for entry in data.get("list", []):
            entry_dt = datetime.fromtimestamp(entry["dt"])
            if start_dt <= entry_dt < end_dt:
                day_key = entry_dt.strftime("%Y-%m-%d")
                daily_data[day_key].append(entry)

        if not daily_data:
            # Fallback: use whatever is available (free tier only goes 5 days ahead)
            for entry in data.get("list", [])[:num_days * 8]:
                entry_dt = datetime.fromtimestamp(entry["dt"])
                day_key  = entry_dt.strftime("%Y-%m-%d")
                daily_data[day_key].append(entry)

        # Build a day-by-day summary
        daily_summaries = []
        all_temps  = []
        rain_days  = 0

        for day_str in sorted(daily_data.keys())[:num_days]:
            entries    = daily_data[day_str]
            temps      = [e["main"]["temp"] for e in entries]
            feels_like = [e["main"]["feels_like"] for e in entries]
            humidity   = [e["main"]["humidity"] for e in entries]
            conditions = [e["weather"][0]["description"] for e in entries]
            wind_speed = [e["wind"]["speed"] for e in entries]

            # Check for rain or snow
            has_rain = any(
                "rain" in c or "drizzle" in c or "snow" in c or "storm" in c
                for c in conditions
            )
            if has_rain:
                rain_days += 1

            all_temps.extend(temps)
            most_common_condition = max(set(conditions), key=conditions.count)

            daily_summaries.append({
                "date":       day_str,
                "min_temp_c": round(min(temps), 1),
                "max_temp_c": round(max(temps), 1),
                "feels_like": round(sum(feels_like) / len(feels_like), 1),
                "humidity":   round(sum(humidity) / len(humidity)),
                "condition":  most_common_condition,
                "wind_kmh":   round(max(wind_speed) * 3.6, 1),
                "has_rain":   has_rain,
            })

        # ── Build the result string ───────────────────────────────────────
        city_display = data.get("city", {}).get("name", city_name)
        country      = data.get("city", {}).get("country", country_code)

        result_lines = [
            f"WEATHER FORECAST — {city_display}, {country}",
            f"Period: {start_date} | {num_days} days",
            f"Overall temp range: {round(min(all_temps), 1)}°C – {round(max(all_temps), 1)}°C",
            f"Rainy days: {rain_days} out of {len(daily_summaries)}",
            "",
            "DAY-BY-DAY FORECAST:",
        ]

        for day in daily_summaries:
            rain_flag = "🌧️ Rain expected" if day["has_rain"] else "☀️ Dry"
            result_lines.append(
                f"  {day['date']}: {day['min_temp_c']}–{day['max_temp_c']}°C | "
                f"{day['condition'].title()} | {rain_flag} | "
                f"Wind: {day['wind_kmh']} km/h | Humidity: {day['humidity']}%"
            )

        result = "\n".join(result_lines)
        return (result, sly_data)
