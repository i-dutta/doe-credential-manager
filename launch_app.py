import subprocess
import os
import sys

# Get the base path — use sys._MEIPASS for PyInstaller or fallback to script dir
base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
app_dir = os.path.join(base_dir, "app")
main_file = os.path.join(app_dir, "main.py")

print(f"Base dir: {base_dir}")
print(f"Running Streamlit with: {sys.executable} -m streamlit run {main_file}")
print(f"Working directory: {base_dir}")

try:
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", main_file],
        cwd=base_dir,
        check=True
    )
    print("Streamlit exited successfully.")
except subprocess.CalledProcessError as e:
    print(f"❌ Failed to launch the app: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

input("Press Enter to exit...")