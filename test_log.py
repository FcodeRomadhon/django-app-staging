# test_log.py
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'staging.settings')
import django
django.setup()

import logging
logger = logging.getLogger('signature')
logger.info("✅ Test log dari script luar")