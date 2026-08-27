# f1_tools.py
# OpenF1 API se F1 data nikalne wale functions

import requests

BASE_URL = "https://api.openf1.org/v1"

def get_sessions(year, country_name=None):
    """
    Kisi saal ke saare race sessions dhundo.
    Optional: country_name se specific race filter kar sakte ho (e.g. "Monaco")
    """
    params = {"year": year, "session_type": "Race"}
    if country_name:
        params["country_name"] = country_name

    response = requests.get(f"{BASE_URL}/sessions", params=params)
    return response.json()


def get_drivers(session_key):
    """
    Kisi session ke saare drivers ki list nikalo (number, naam, team).
    """
    response = requests.get(f"{BASE_URL}/drivers", params={"session_key": session_key})
    return response.json()


def get_laps(session_key, driver_number=None):
    """
    Session ke lap times nikalo. driver_number diya to sirf usi driver ka data.
    Sirf zaroori fields rakhte hain — heavy telemetry arrays hata dete hain
    taaki LLM ko bhejne layak size chhota rahe.
    """
    params = {"session_key": session_key}
    if driver_number:
        params["driver_number"] = driver_number

    response = requests.get(f"{BASE_URL}/laps", params=params)
    raw_data = response.json()

    # Sirf zaroori fields rakho, bhaari segment arrays hata do
    trimmed = []
    for lap in raw_data:
        trimmed.append({
            "driver_number": lap.get("driver_number"),
            "lap_number": lap.get("lap_number"),
            "lap_duration": lap.get("lap_duration"),
            "is_pit_out_lap": lap.get("is_pit_out_lap")
        })

    return trimmed


def get_stints(session_key, driver_number=None):
    """
    Tyre stints nikalo — kaunsa driver kaunse compound pe kitni laps chala.
    """
    params = {"session_key": session_key}
    if driver_number:
        params["driver_number"] = driver_number

    response = requests.get(f"{BASE_URL}/stints", params=params)
    raw_data = response.json()

    trimmed = []
    for stint in raw_data:
        trimmed.append({
            "driver_number": stint.get("driver_number"),
            "compound": stint.get("compound"),
            "lap_start": stint.get("lap_start"),
            "lap_end": stint.get("lap_end"),
            "tyre_age_at_start": stint.get("tyre_age_at_start")
        })

    return trimmed

def get_weather(session_key):
    """
    Track weather nikalo — temperature, rain, humidity.
    Tyre choice ko justify karne ke liye useful context.
    """
    response = requests.get(f"{BASE_URL}/weather", params={"session_key": session_key})
    return response.json()


# --- Quick test (isi file ko seedha chalane pe chalega) ---
if __name__ == "__main__":
    # Test: 2024 Monaco race dhundo
    sessions = get_sessions(year=2024, country_name="Monaco")
    print("Sessions found:", len(sessions))
    if sessions:
        print(sessions[0])   # pehla session dikhao dekhne ke liye