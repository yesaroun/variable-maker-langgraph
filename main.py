import sys
import os
import threading
import subprocess
import time

project_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(project_root, "frontend"))
sys.path.insert(0, os.path.join(project_root, "backend"))


def start_backend():
    """Backend FastAPI 서버 시작"""
    backend_dir = os.path.join(project_root, "backend")
    subprocess.run(
        ["uvicorn", "app.main:app", "--reload", "--port", "8000"], cwd=backend_dir
    )


def start_frontend():
    """Frontend Streamlit 앱 시작"""
    time.sleep(2)  # Backend가 먼저 시작되도록 대기
    import streamlit.web.cli as stcli

    frontend_app_path = os.path.join(project_root, "frontend", "src", "app.py")
    sys.argv = ["streamlit", "run", frontend_app_path]
    stcli.main()


if __name__ == "__main__":
    # Backend를 별도 스레드에서 시작
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()

    # Frontend 시작
    start_frontend()
