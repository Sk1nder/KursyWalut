# KursyWalut

The **KursyWalut** application allows users to monitor current exchange rates in a clear and intuitive interface. This project is developed in Python, using Flask and additional libraries for data analysis and visualization.

## Features
- Fetch and display exchange rates from external sources (e.g., banking APIs).
- Present data through charts (using Plotly, Seaborn, Matplotlib).
- Handle user forms for selecting date ranges, currencies, and analysis scope.
- Intuitive interface with Bootstrap integration.

## Technology Stack
- **Backend**: Flask (with Flask-WTF for form handling)
- **Frontend**: Flask-Bootstrap
- **Libraries**:
  - Pandas (for data analysis)
  - Matplotlib, Plotly, Seaborn (for visualization)
  - Requests (for fetching data from APIs)
  - Python-dotenv (for managing environment variables)
  - WTForms (for user forms)

## Requirements
Ensure the required dependencies are installed before running the application. Use the following command:

```bash
pip install -r requirements.txt

# Step 1: Create a virtual environment
python -m venv .venv

# Step 2: Activate the virtual environment
# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Step 3: Install required dependencies
pip install -r requirements.txt

# Step 4: Verify the virtual environment is active
which python  # It should point to the .venv directory

KursyWaluit/
│
├── app.py          # Główny plik aplikacji
├── config.py       # Konfiguracja aplikacji
├── templates/      # Pliki HTML
├── static/         # Pliki CSS, JS
├── .env            # Zmienne środowiskowe
└── requirements.txt # Lista zależności
