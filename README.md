# Artificial Generative Nested Environment System (AGNES)
**AGNES** is a specialized home assistant that can be fully customized to your preferences while also including all the standard features of a typical home assistant, such as controlling lights, weather, and calendar.

## Features
- Calculate water to rice ratio
- Clock / alarm
- Control light
- Weather statation
- Calculator (Inger's formular)
- Calendar

### Planned Features
- Intrinsic value calc.
- Bargin offers (e.g. Føtex)
- Syntax in prog. lan. eg. (C, Java, Python, JS)
- Binary & hex converter
- Security testing tools (for educational purposes)

## Technologies Used
- AGNES voice: gTTS (Google Translate)
- Speech recognition: Google
- Playing mp3 files: playsound

## Project Structure
```plaintext
├── credentials.json            # Google Calendar authentication
├── .usage_report/              # Stores yearly usage reports
└── src/
    ├── _tests_/                # Unit tests
    ├── external_services/      # API integrations
    ├── mp3_files/              # Audio files
    ├── app.py                  # The main program 
    ├── calc.py                 # Calculation and equations
    ├── converter.py            # Converts to and from diff. vaules
    ├── global_var.py           # Global variables and DB communication
    ├── notes.py                # Read and write to txt files
    ├── sound_effects.py        # Playing diff. mp3 files, and adjust the sound
    ├── timer.py                # Set diff. timers for user
    └── voice_communication.py  # Communication (I/O), from/to user
```

## Getting Started
### Prerequisites
Ensure you have the following connected to the computer:
- Microphone
- Speaker

### Setup the project
1.	Clone the repository:
```bash
git clone https://github.com/Fzz1n/AGNES.git
```
2. Navigate to the project directory:
```bash
cd AGNES
```

3. Create virtual environment:
```bash
python -m venv .venv
```

4. Activate venv folder:
```bash
# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Create a `.env` file in the root folder (`AGNES`) and fill it with values from `.env.example`.

7. Add Google credentials by creating a `credentials.json` file (see: https://developers.google.com/workspace/guides/create-credentials).

8. Linux only: Update line 17 in `sound_effects.py` to match your speaker port.

### Running the app for the first time
Connect your iOS device and start the program:
```bash
python -m app
```

### Running tests
Run all tests:
```bash
python -m pytest
```

Run a specific test file:
```bash
python -m pytest src/_test_/{file_name}
```

# Contributing
Contributions are welcome! Follow these steps:
1. Make sure you are on `staging` and it is up to date.
```bash
git switch staging
git pull
```

2. Create a branch for your feature or bugfix:
```bash
git switch -c feat/feature-name
# or
git switch -c bugfix/bug-name
```

3. Commit your changes:
```bash
# If dependencies changed
pip freeze > requirements.txt

git commit
# Write commit message in opened editor, save and exit editor
```

4. Push local branch to remote:
```bash
git push origin feature-name
```
5. Open a pull request to `staging` and test it, and then create a new pull request for main.