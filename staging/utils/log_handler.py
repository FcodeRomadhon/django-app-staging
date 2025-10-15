# staging/utils/log_handler.py
import os
from datetime import datetime
import logging  # ← tambahkan ini

class DailyLoggerHandler(logging.Handler):  # ← warisi dari logging.Handler
    def __init__(self, base_dir="logs"):
        super().__init__()  # ← panggil parent constructor
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def emit(self, record):
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            log_dir = os.path.join(self.base_dir, today)
            os.makedirs(log_dir, exist_ok=True)

            filename = f"info.{record.name}.log"
            filepath = os.path.join(log_dir, filename)

            # Gunakan formatter dari settings
            msg = self.format(record)

            with open(filepath, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
        except Exception:
            self.handleError(record)