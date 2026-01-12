import requests
import pathlib
import json
import argparse

def api_to_json(url: str, out_path: pathlib.Path) -> None:
    response: requests.Response = requests.get(url)
    if response.status_code == 200:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as j: 
            json.dump(response.json(), j, ensure_ascii=False, indent=2)
    else: 
        return response.status_code

def read_json(raw_input: pathlib.Path) -> list[dict]:
    if raw_input:
        with open(raw_input, "r", encoding="utf-8") as i:
            return [user for user in json.load(i)]

def stripped_str(value: str | None) -> str | None:
    return None if value == None or value.strip()=="" else str(value.strip())

def user_to_record(user: dict) -> dict:
    raw_id = user.get("id")
    if raw_id is None: 
        raise ValueError(f'ID for {user.get("name")} missing.')
    address = user.get("address") or {}
    geo = address.get("geo") or {}
    company = user.get("company") or {}
    email = stripped_str(user.get("email"))
    email = email.lower() if email else None
    email = email if email and "@" in email else None
    try: 
        lat = float(geo.get("lat"))
    except (TypeError, ValueError):
        lat = None
    try: 
        lng = float(geo.get("lng"))
    except (TypeError, ValueError):
        lng = None
    return {
        "id" : int(raw_id),
        "name": stripped_str(user.get("name")),
        "username" : stripped_str(user.get("username")),
        "email" : (email if email is not None and "@" in email else None),
        "city" : stripped_str(address.get("city")),
        "zipcode" : stripped_str(address.get("zipcode")),
        "lat" : lat,
        "lng" : lng,
        "company_name" : stripped_str(company.get("name")),
        "website" : stripped_str(user.get("website"))
        }

def write_to_clean(users: list[dict], output: pathlib.Path) -> None:
    records = [user_to_record(u) for u in users]
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as j: 
        json.dump(records, j, ensure_ascii=False, indent=2)

def main() -> None: 
    #api_to_json("https://jsonplaceholder.typicode.com/users", pathlib.Path("out/users_raw.json"))
    write_to_clean(read_json("out/users_raw.json"), pathlib.Path("out/users_clean.json"))

if __name__ == "__main__":
    main()