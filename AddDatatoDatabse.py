import requests
import json

SUPABASE_URL = "https://vcucpobbtjizdsfjnzcs.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZjdWNwb2JidGppemRzZmpuemNzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDA3MTE2NCwiZXhwIjoyMDY5NjQ3MTY0fQ.0oenAjvPQ7QMbiC7zvEYSnW-cS8GlxlhKciOIp0cvm0"



SUPABASE_TABLE_ENDPOINT = f"{SUPABASE_URL}/rest/v1/students"

HEADERS = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"  # so repeated ids get updated
}

data = [
    {
        "id": "321654",
        "name": "Murtaza Hassan",
        "major": "Robotics",
        "starting_year": 2017,
        "total_attendance": 7,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
    {
        "id": "852741",
        "name": "Emly Blunt",
        "major": "Economics",
        "starting_year": 2021,
        "total_attendance": 12,
        "standing": "B",
        "year": 1,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
    {
        "id": "963852",
        "name": "Elon Musk",
        "major": "Physics",
        "starting_year": 2020,
        "total_attendance": 7,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
{
        "id": "277299",
        "name": "Bhomaram Suthar",
        "major": "Computer Engineering",
        "starting_year": 2023,
        "total_attendance": 0,
        "standing": "G",
        "year": 3,
        "last_attendance_time": "2022-12-11 00:54:34"
    }
]

response = requests.post(
    SUPABASE_TABLE_ENDPOINT,
    headers=HEADERS,
    data=json.dumps(data)
)

print(response.status_code, response.text)
