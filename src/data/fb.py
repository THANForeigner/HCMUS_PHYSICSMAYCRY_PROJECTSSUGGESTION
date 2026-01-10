import os
from pathlib import Path
from dotenv import load_dotenv

# Get the absolute path to the directory containing this file
current_dir = Path(__file__).parent
# Go up two levels to reach the project root
project_root = current_dir.parent.parent
# Construct the path to the .env file in the project root
dotenv_path = project_root / ".env"

load_dotenv(dotenv_path=dotenv_path)

FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
TOOLKIT_URL = os.environ.get("TOOLKIT_URL")
PROJECT_ID = os.environ.get("PROJECT_ID")
BASE_FIRESTORE_URL = os.environ.get("BASE_FIRESTORE_URL")


def firebase_login(email, pwd):
    url = f"{TOOLKIT_URL}signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": pwd, "returnSecureToken": True}
    try:
        r = requests.post(url, json=payload)
        data = r.json()
        if "error" in data:
            return {"error": data["error"]["message"]}
        return data
    except Exception as e:
        return {"error": str(e)}


def firebase_register(email, pwd, name):
    url = f"{TOOLKIT_URL}signUp?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": pwd, "returnSecureToken": True}
    try:
        r = requests.post(url, json=payload)
        auth_data = r.json()
        if "error" in auth_data:
            return {"error": auth_data["error"]["message"]}
        id_token = auth_data["idToken"]
        update_url = f"{TOOLKIT_URL}update?key={FIREBASE_API_KEY}"
        requests.post(update_url, json={"idToken": id_token, "displayName": name})
        auth_data["displayName"] = name
        final_profile = create_new_user_profile(auth_data, name)
        return final_profile
    except Exception as e:
        return {"error": str(e)}


def firebase_forgot_password(email):
    url = f"{TOOLKIT_URL}sendOobCode?key={FIREBASE_API_KEY}"
    payload = {"requestType": "PASSWORD_RESET", "email": email}
    try:
        r = requests.post(url, json=payload)
        data = r.json()
        if "error" in data:
            return {"error": data["error"]["message"]}
        return {"email": email, "status": "Success"}
    except Exception as e:
        return {"error": str(e)}


def create_new_user_profile(user_auth_data, user_name):
    uid = user_auth_data.get("localId")
    id_token = user_auth_data.get("idToken")
    email = user_auth_data.get("email")
    profile_data = {
        "email": email,
        "name": user_name,
        "hasGeneratedPath": False,
        "proj": [],
        "completedProjects": [],
        "favoriteProjects": [],
    }
    user_db_url = f"{DATABASE_URL}users/{uid}.json?auth={id_token}"

    try:
        response = requests.put(user_db_url, json=profile_data)
        if response.status_code == 200:
            profile_data["localId"] = uid
            profile_data["idToken"] = id_token
            return profile_data
        else:
            print(f"Lỗi DB: {response.text}")
            return user_auth_data
    except Exception as e:
        print(f"Lỗi mạng khi tạo profile: {e}")
        return user_auth_data


def get_user_profile(user_auth_data):
    uid = user_auth_data.get("localId")
    id_token = user_auth_data.get("idToken")
    if not uid:
        return {"error": "No UID provided"}
    url = f"{DATABASE_URL}users/{uid}.json?auth={id_token}"
    try:
        response = requests.get(url)
        if response.status_code == 200 and response.json() is not None:
            db_data = response.json()
            full_profile = {
                "localId": uid,
                "idToken": id_token,
                "email": db_data.get("email", user_auth_data.get("email")),
                "name": db_data.get("name", user_auth_data.get("displayName", "User")),
                "hasGeneratedPath": db_data.get("hasGeneratedPath", False),
                "proj": db_data.get("proj", []),
                "completedProjects": db_data.get("completedProjects", []),
                "favoriteProjects": db_data.get("favoriteProjects", []),
            }
            return full_profile
        else:
            user_name = user_auth_data.get("displayName", "User")
            return {
                "localId": uid,
                "idToken": id_token,
                "email": user_auth_data.get("email"),
                "name": user_name,
                "hasGeneratedPath": False,
                "proj": [],
            }
    except Exception as e:
        return user_auth_data


def fb_add(path, data, id_token):
    url = f"{DATABASE_URL}{path}.json?auth={id_token}"
    try:
        r = requests.post(url, json=data)
        return r.status_code == 200
    except:
        return False


def fb_update(path, data, id_token):
    url = f"{DATABASE_URL}{path}.json?auth={id_token}"
    try:
        r = requests.patch(url, json=data)
        return r.status_code == 200
    except:
        return False


def fb_delete(path, id_token):
    url = f"{DATABASE_URL}{path}.json?auth={id_token}"
    try:
        r = requests.delete(url)
        return r.status_code == 200
    except:
        return False


def _parse_firestore_value(field_value):
    if "stringValue" in field_value:
        return field_value["stringValue"]
    elif "integerValue" in field_value:
        return int(field_value["integerValue"])
    elif "doubleValue" in field_value:
        return float(field_value["doubleValue"])
    elif "booleanValue" in field_value:
        return field_value["booleanValue"]

    elif "arrayValue" in field_value:
        return [
            _parse_firestore_value(v)
            for v in field_value["arrayValue"].get("values", [])
        ]
    elif "mapValue" in field_value:
        return _parse_firestore_document(field_value["mapValue"].get("fields", {}))
    return None


def _parse_firestore_document(fields):
    return {k: _parse_firestore_value(v) for k, v in fields.items()}


def get_all_projects(id_token=None):
    url = f"{BASE_FIRESTORE_URL}/prj"
    headers = {}
    if id_token:
        headers["Authorization"] = f"Bearer {id_token}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:  # NOT_FOUND
            return []
        if response.status_code == 403:  # PERMISSION_DENIED
            return []
        if response.status_code != 200:
            return []
        data = response.json()
        documents = data.get("documents", [])
        final_projects = []
        for doc in documents:
            raw_fields = doc.get("fields", {})
            parsed_data = _parse_firestore_document(raw_fields)
            req_mat = parsed_data.get("Required_material", [])
            if isinstance(req_mat, str):
                req_mat = [req_mat]
            try:
                est_hours = int(parsed_data.get("Estimated_hours", 0))
            except:
                est_hours = 0
            project_obj = {
                "Title": parsed_data.get("Title", "No Title"),
                "Description": parsed_data.get("Description", ""),
                "Skills": parsed_data.get("Skills", []),
                "Major": parsed_data.get("Major", "General"),
                "Interests": parsed_data.get("Interests", []),
                "Required_material": req_mat,
                "Estimated_hours": est_hours,
                "TutorialLink": parsed_data.get("TutorialLink", []),
            }
            final_projects.append(project_obj)
        return final_projects
    except Exception as e:
        return []

