# Artificial Generative Nested Environment System (AGNES)
**AGNES** is a specialized home assistant that can be fully customized to your preferences while also including all the standard features of a typical home assistant, such as controlling lights, heating, and sensors.

## Features
**Must have**:
- Rice calc.
- Clock / alarm
- Control light

**Should have**:
- Weather statation
- Clacluator (Inger's formular)
- Calender
- Intrinsic value calc.
- Bargin offers -> Føtex
- Syntax in prog. lan. eg. (C, Java, Python, JS)

**Could have**:
- Binary & hex converter
- Pen. test of websites
- Hash/code breaker (brute force), eg. HashCat

## Technologies Used
- AGNES voice: gTTS (Google Translate)
- Speech recognition: Google
- Playing mp3 files: playsound

## Project Structure
```plaintext
src/
├── calc.py         # Calculation and eaquations
├── converter.py    # Converts to and from diff. vaules
├── main.py         # Communication (I/O)
└── timer.py        # Set diff. timers for user
```

## Getting Started
### Prerequisites
Ensure you have the following connected to the computer:
- Microphone
- Speaker

### Setting Up the Backend
(Not relevant for now)

### Setup the project
1.	Clone the repository:
```bash
git clone https://github.com/Fzz1n/AGNES.git
```
2. Navigate to the project directory:
```bash
cd AGNES
```
3. Create venv folder
```bash
python -m venv .venv
```

4. Activate venv folder
```bash
# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

### Running the App for the First Time
Connect your iOS device and start the program with:
```bash
python -m src.main
```

### Running tests
(Not yet integrated)

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
git switch -c bugfix/bug-name
```

3. Commit your changes:
```bash
git commit
# Write commit message in opened editor, save and exit editor
```

4. Push local branch to remote:
```bash
git push origin feature-name
```
5. Open a pull request to the staging branch, test it, and then create a new pull request for main.
