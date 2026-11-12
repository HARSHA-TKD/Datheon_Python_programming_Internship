⚡ PRO FILE ORGANIZER

Intelligent Desktop File Automation | Python

<p align="center">
  <b>Organize smarter. Work cleaner. Save time.</b>
</p><p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Automation-Desktop-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Internship-Datheon-purple?style=for-the-badge" />
</p>---

📌 Overview

Pro File Organizer is an automated desktop utility developed using Python to eliminate the hassle of manually organizing cluttered directories.

The application scans a selected directory, identifies files based on their extensions, dynamically creates categorized folders, and moves files into their appropriate locations.

Built with reliability and simplicity in mind, it includes duplicate filename handling and permission-related exception management to make file organization safer and more efficient.

✨ Key Features

Feature| Description
🔍 Smart Scanning| Scans directories to identify files automatically.
📁 Dynamic Folders| Creates category folders when required.
🗂️ Auto Classification| Groups files based on their extensions.
🛡️ Collision Handling| Prevents accidental overwriting of duplicate filenames.
⚙️ Exception Handling| Handles permission-related errors.
🚀 Automated Movement| Moves files using Python's file management modules.

🧠 How It Works

       USER DIRECTORY
             |
             ▼
      DIRECTORY SCANNER
        (os.scandir)
             |
             ▼
      FILE EXTENSION CHECK
             |
             ▼
       CATEGORY DETECTION
             |
       ┌─────┼──────┬──────┐
       ▼     ▼      ▼      ▼
   Documents Images Videos Archives
             |
             ▼
      DYNAMIC FOLDER CREATION
             |
             ▼
        SAFE FILE MOVEMENT
        (shutil.move)
             |
       ┌─────┴────────┐
       ▼              ▼
   Collision       Permission
   Handling        Handling
       |              |
       └──────┬───────┘
              ▼
       ORGANIZED DIRECTORY

📂 Supported File Categories

Folder| Example Extensions
Documents| ".pdf", ".docx", ".txt", ".doc"
Images| ".png", ".jpg", ".jpeg", ".gif"
Videos| ".mp4", ".mkv", ".avi"
Archives| ".zip", ".rar", ".7z"
Code| ".py", ".c", ".cpp", ".html", ".css", ".js"

Note: Supported extensions depend on the mappings configured in the source code.

🛠️ Technology Stack

- Language: Python 3
- Directory Scanning: "os.scandir()"
- File Management: "shutil"
- File System Operations: "os"
- Exception Handling: Python "try-except"

🚀 Getting Started

Prerequisites

- Python 3.x
- Visual Studio Code or any Python-compatible editor

Installation

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL

2. Navigate to the project directory

cd task3_file_automation

3. Run the application

python organizer.py

4. Provide the directory path

Enter the path of the directory you want to organize when prompted by the program.

The organizer will scan the directory and automatically arrange supported files into categorized folders.

🧪 Testing & Validation

The application was checked for the following scenarios:

- [x] Normal file organization.
- [x] Automatic category folder creation.
- [x] Duplicate filename handling.
- [x] Permission exception handler implementation.
- [x] Successful file movement.
- [ ] Permission-denied runtime scenario (platform-dependent).

📁 Project Structure

task3_file_automation/
│
├── organizer.py
├── README.md
└── test_file/
    ├── Documents/
    ├── Images/
    ├── Videos/
    ├── Archives/
    └── Code/

🎯 Learning Outcomes

Through this project, I explored:

- Python-based desktop automation.
- File and directory manipulation.
- Dynamic directory creation.
- Extension-based file classification.
- Exception handling and collision prevention.
- Practical application of Python standard libraries.

🔮 Future Improvements

- GUI-based file selection.
- Custom category configuration.
- File organization logs and reports.
- Dry-run mode before moving files.
- Recursive directory organization.
- More advanced file classification.

👨‍💻 Internship Information

Detail| Information
Organization| Datheon
Internship Domain| Python Programming
Project| Pro File Organizer
Task| Task 3
Language| Python

---

<p align="center">
  <b>Built with Python ⚡</b>
  <br/>
  <i>Automating everyday tasks, one directory at a time.</i>
</p>