"""Development launcher that restarts the game after valid Python changes."""

import ast
import hashlib
import subprocess
import sys
import time
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
MAIN_FILE = PROJECT_DIR / "Main.py"
IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__"}


def iter_python_files(project_dir=PROJECT_DIR):
    for path in Path(project_dir).rglob("*.py"):
        if not any(part in IGNORED_DIRS for part in path.parts):
            yield path


def snapshot_python_files(project_dir=PROJECT_DIR):
    snapshot = {}
    for path in iter_python_files(project_dir):
        try:
            stat = path.stat()
            digest = hashlib.sha256(path.read_bytes()).digest()
            snapshot[path] = (stat.st_mtime_ns, stat.st_size, digest)
        except OSError:
            continue
    return snapshot


def changed_files(previous, current):
    paths = set(previous) | set(current)
    return sorted(
        path for path in paths if previous.get(path) != current.get(path)
    )


def validate_python_files(project_dir=PROJECT_DIR):
    errors = []
    for path in iter_python_files(project_dir):
        try:
            source = path.read_text(encoding="utf-8-sig")
            ast.parse(source, filename=str(path))
        except (OSError, UnicodeError, SyntaxError) as error:
            errors.append(f"{path}: {error}")
    return not errors, tuple(errors)


def start_game(project_dir=PROJECT_DIR, main_file=MAIN_FILE):
    return subprocess.Popen(
        [sys.executable, str(main_file)],
        cwd=str(project_dir),
    )


def stop_game(process, timeout=3):
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=timeout)


class ChangeSignal:
    """Collects optional watchdog events without coupling the runner to it."""

    def __init__(self):
        self.pending = False

    def mark(self):
        self.pending = True

    def consume(self):
        pending = self.pending
        self.pending = False
        return pending


def create_watchdog(project_dir, signal):
    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except ImportError:
        return None

    class PythonChangeHandler(FileSystemEventHandler):
        def on_any_event(self, event):
            if not event.is_directory and event.src_path.endswith(".py"):
                signal.mark()

    observer = Observer()
    observer.schedule(PythonChangeHandler(), str(project_dir), recursive=True)
    observer.start()
    return observer


class DevRunner:
    def __init__(self, project_dir=PROJECT_DIR, poll_interval=0.5):
        self.project_dir = Path(project_dir)
        self.main_file = self.project_dir / "Main.py"
        self.poll_interval = max(0.1, float(poll_interval))
        self.process = None
        self.snapshot = snapshot_python_files(self.project_dir)
        self.signal = ChangeSignal()
        self.observer = None

    def restart(self):
        valid, errors = validate_python_files(self.project_dir)
        if not valid:
            print("[dev_runner] Syntax check failed; current game kept running.")
            for error in errors:
                print(error)
            return False

        stop_game(self.process)
        self.process = start_game(self.project_dir, self.main_file)
        print("[dev_runner] Game restarted.")
        return True

    def check_for_changes(self):
        current = snapshot_python_files(self.project_dir)
        changes = changed_files(self.snapshot, current)
        self.snapshot = current
        return changes

    def run(self):
        self.observer = create_watchdog(self.project_dir, self.signal)
        mode = "watchdog + polling" if self.observer else "polling fallback"
        print(f"[dev_runner] Watching Python files ({mode}).")
        self.restart()
        try:
            while True:
                time.sleep(self.poll_interval)
                changes = self.check_for_changes()
                signaled = self.signal.consume()
                if changes or signaled:
                    # One more interval absorbs multi-file editor save bursts.
                    time.sleep(self.poll_interval)
                    changes.extend(self.check_for_changes())
                    names = sorted({path.name for path in changes})
                    if names:
                        print(f"[dev_runner] Changed: {', '.join(names)}")
                    self.restart()
        except KeyboardInterrupt:
            print("[dev_runner] Stopping.")
        finally:
            if self.observer is not None:
                self.observer.stop()
                self.observer.join(timeout=3)
            stop_game(self.process)


if __name__ == "__main__":
    DevRunner().run()
