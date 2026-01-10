# HCMUS PHYSICSMAYCRY PROJECTS SUGGESTION

This is a Flet-based desktop application that provides project suggestions for students, based on their interests and skills. It features user authentication, project browsing, and a personalized learning path.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7+
- pip (Python package installer)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/THANForeigner/HCMUS_PHYSICSMAYCRY_PROJECTSSUGGESTION.git
   cd HCMUS_PHYSICSMAYCRY_PROJECTSSUGGESTION
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

This project uses Firebase for authentication and as a database. You will need to set up your own Firebase project to run the application.

1. **Create a Firebase Project:**
   - Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project.
   - Enable the following services:
     - **Authentication:** Enable the "Email/Password" sign-in method.
     - **Realtime Database:** Create a new database.
     - **Firestore:** Create a new database.

2. **Get your Firebase credentials:**
   - In your Firebase project settings, find your **Web API Key**.
   - In the Realtime Database settings, find your **Database URL**.
   - Your **Project ID** is also in the project settings.

3. **Create the `.env` file:**
   - In the project's root directory, create a new file named `.env`.
   - Add the following content to the `.env` file, replacing the placeholder values with your own Firebase credentials:

   ```
   FIREBASE_API_KEY=your-firebase-api-key
   DATABASE_URL=your-database-url
   TOOLKIT_URL=https://identitytoolkit.googleapis.com/v1/accounts:
   PROJECT_ID=your-project-id
   BASE_FIRESTORE_URL="https://firestore.googleapis.com/v1/projects/${PROJECT_ID}/databases/(default)/documents"
   ```

## Running the Application

Once you have installed the dependencies and configured your `.env` file, you can run the application with the following command:

```bash
flet run  -r
```

This will launch the Flet desktop application.

## Project Structure

- **`src/main.py`**: The main entry point for the Flet application.
- **`src/components/`**: Contains the UI components of the application (e.g., forms, dialogs, cards).
- **`src/logic/`**: Contains the business logic of the application (e.g., project suggestions, user info).
- **`src/services/`**: Contains services for interacting with external APIs (e.g., Firebase Authentication).
- **`src/data/`**: Contains data-related files, including the `.env` configuration file and Firebase interaction logic.
- **`requirements.txt`**: A list of the Python dependencies for the project.
- **`README.md`**: This file.
