import datetime
import traceback
from pathlib import Path


class ErrorLogger:
    """Writes unexpected failures to a fixed project log path."""

    def __init__(self, base_dir):
        self.log_dir = Path(base_dir) / "logs"
        self.log_file = self.log_dir / "error.log"

    def log_exception(self, exception_type, exception, exception_traceback):
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
            details = "".join(
                traceback.format_exception(
                    exception_type, exception, exception_traceback
                )
            )
            with self.log_file.open("a", encoding="utf-8") as output:
                output.write(f"[{timestamp}]\n{details}\n")
            return True
        except (OSError, UnicodeError):
            return False

