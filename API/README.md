# API Documentation

API team is in charge of starting the logic-map.
Check the [doc](../LogicMap.md) for more details.

## How to start the Web App and the Logic map ?

Both start with the Flask app, with a single command.
But first, one need to configure a [python virtual environment](https://docs.python.org/3/library/venv.html):

On Linux:
```bash
cd src/

python -m venv  # Create env
source venv/bin/activate  # Enter env
pip install -r requirements.txt  # Install dependencies
```

Replace `source venv/bin/activate` with `.\venv\Scripts\Activate.bat` on Windows.

And simply start the app with:

```bash
python main.py
```

View the page at http://localhost:5000