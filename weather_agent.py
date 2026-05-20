import sys
import requests

sys.stdout.reconfigure(encoding="utf-8")
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": (
            "Get the current temperature and weather conditions for a city or location. "
            "Use this whenever the user asks about weather anywhere."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and region/country to look up, e.g. 'Charlotte, NC' or 'Paris, France'."
                }
            },
            "required": ["location"]
        }
    }
]


def interpret_weather_code(code: int) -> str:
    if code == 0:              return "Clear sky"
    elif code <= 2:            return "Partly cloudy"
    elif code == 3:            return "Overcast"
    elif code in (45, 48):    return "Foggy"
    elif code in (51, 53, 55): return "Drizzle"
    elif code in (61, 63, 65): return "Rain"
    elif code in (71, 73, 75): return "Snow"
    elif code in (80, 81, 82): return "Rain showers"
    elif code in (95, 96, 99): return "Thunderstorm"
    else:                      return f"Unknown (code {code})"


US_STATES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia",
}


def get_weather(location: str) -> str:
    print(f"  [Tool] Geocoding '{location}'...")
    parts = [p.strip() for p in location.split(",")]
    city_name = parts[0]
    qualifier = parts[1].upper() if len(parts) > 1 else None
    if qualifier in US_STATES:
        qualifier = US_STATES[qualifier]

    geo_response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city_name, "count": 10, "language": "en", "format": "json"}
    )
    geo_data = geo_response.json()

    if not geo_data.get("results"):
        return f"Could not find coordinates for '{location}'. Try a more specific location name."

    candidates = geo_data["results"]
    if qualifier:
        result = next(
            (r for r in candidates
             if qualifier.lower() in r.get("admin1", "").lower()
             or qualifier.lower() in r.get("country", "").lower()),
            candidates[0]
        )
    else:
        result = candidates[0]
    lat = result["latitude"]
    lon = result["longitude"]
    place_name = result.get("name", location)
    country = result.get("country", "")
    print(f"  [Tool] Found: {place_name}, {country} ({lat}, {lon})")

    print(f"  [Tool] Fetching weather...")
    weather_response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,weathercode,windspeed_10m",
            "temperature_unit": "fahrenheit",
            "windspeed_unit": "mph",
            "timezone": "auto"
        }
    )
    weather_data = weather_response.json()
    current = weather_data["current"]

    temp = current["temperature_2m"]
    windspeed = current["windspeed_10m"]
    code = current["weathercode"]
    condition = interpret_weather_code(code)

    return (
        f"Location: {place_name}, {country}\n"
        f"Temperature: {temp}°F\n"
        f"Conditions: {condition}\n"
        f"Wind: {windspeed} mph"
    )


def run_agent(user_message: str):
    print(f"\n[User] {user_message}")
    print("-" * 50)

    messages = [{"role": "user", "content": user_message}]

    while True:
        print("\n[Agent] Sending request to Claude...")

        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            tools=tools,
            messages=messages
        ) as stream:
            printed_header = False
            for text in stream.text_stream:
                if not printed_header:
                    print("\n[Claude] ", end="", flush=True)
                    printed_header = True
                print(text, end="", flush=True)
            response = stream.get_final_message()

        print(f"\n[Agent] Stop reason: {response.stop_reason}")

        if response.stop_reason == "end_turn":
            print()
            return

        if response.stop_reason == "tool_use":
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

            tool_results = []
            for tool_use_block in tool_use_blocks:
                tool_name   = tool_use_block.name
                tool_input  = tool_use_block.input
                tool_use_id = tool_use_block.id

                print(f"\n[Agent] Claude requested tool: '{tool_name}'")
                print(f"[Agent] Tool input: {tool_input}")

                if tool_name == "get_weather":
                    tool_result = get_weather(tool_input["location"])
                else:
                    tool_result = f"Unknown tool: {tool_name}"

                print(f"[Agent] Tool result:\n{tool_result}")
                print("-" * 50)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": tool_result
                })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = input("Ask about the weather: ")

    run_agent(question)
