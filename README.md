# DoE Credential Manager

This project is a Streamlit-based credential management app designed for local use without sharing data or requiring explicit installation of dependencies.

## How to Run the App Locally

### Using the Portable Python Environment

1. Ensure the portable_python folder is present in the project root, containing WinPython with all dependencies installed.
2. Open a command prompt in the project root directory.
3. Run the following command to start the app:

```sh

portable_python\python\python.exe -m streamlit run app\main.py

```

# Using the Batch File

1. Double-click Run_Credential_Manager.bat (previously run_streamlit_app.bat) in the project root.
2. This will launch the app in your default web browser.
3. If an error occurs, the command prompt window will display the error message. Press any key to close the window after reading the message.

# Project Structure

 
Project
│
├── app
│   ├── main.py
│   ├── utils.py
│   └── config.py
│
├── data
│   ├── secret.key
│   ├── credentials.db
│   └── url_credentials.csv
│
├── portable_python (WinPython portable environment with dependencies)
│
├── Run_Credential_Manager.bat
│
├── launch_app.py (optional launcher script)
│
└── requirements.txt


# Notes

1. The app uses a portable Python environment to avoid dependency and installation issues.
2. No global Python or package installations are required.
3. Users run the app locally and do not share data between each other.
4. Make sure to extract the entire project folder from the zip before running.
5. If you encounter errors, check the command prompt window launched by the batch file for messages.
6. If the app doesn’t start or shows "module not found" errors, ensure the portable_python folder is complete and dependencies are installed.
