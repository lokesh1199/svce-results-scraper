import os
import sys

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    '..'
)))

from app.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0')