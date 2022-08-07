import signal
import sys

from art import tprint
from .main import main, signal_handler

try:
    main()
    signal.signal(signal.SIGINT, signal_handler)
except KeyboardInterrupt:
    tprint('Goodbye!', font='block')
finally:
    sys.exit(0)
