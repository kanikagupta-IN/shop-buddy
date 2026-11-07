import os
import sys
import subprocess

if __name__ == "__main__":
    print("Initializing Production runtime loop...")
    # Ensure the root path is inside the python path environment dictionary
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(os.path.dirname(__file__))

    # Add project root directory explicitly to path variables
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Run the main presentation app module using Streamlit orchestration binaries
    subprocess.run(["streamlit", "run", "app/ui.py"], env=env)
