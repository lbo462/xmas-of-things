# API Documentation

API team is in charge of starting the API dashboard and logic map.

## What's the logic map ?

The logic map is a python script that transforms sensors data into actions.

Here's how it works:
- Read uplink of a device on TTN
- Apply some business rules to determine actions to do
- Sends these actions as payload on the downlink topic of the device waiting these actions

Find details about the place of the logic map in the big picture on the [TTN documentation](../TTN/README.md).

Find more details about the logic map itself in [LogicMap.md](LogicMap.md).

## How to start the Web App and the Logic map ?

In the folder `API/src` ...

1. One need to __configure a [python virtual environment](https://docs.python.org/3/library/venv.html)__:

On Linux:
```bash
cd src/

python -m venv  # Create env
source venv/bin/activate  # Enter env
pip install -r requirements.txt  # Install dependencies
```

_Replace `source venv/bin/activate` with `.\venv\Scripts\Activate.bat` on Windows._

2. Then, __create a `.env` file__ following scheme below:

```
TTN_APP_ID=<app-name>
TTN_TENANT_ID=ttn
TTN_API_KEY=<api-key>
TTN_BASE_URL=eu1.cloud.thethings.network
TTN_PORT=1883
```

Replace the app name with the name of your application on TTN.

You also need to create an API key from the TTN web interface and paste it here.

3. And simply start the app with:

```bash
python main.py
```

View the page at http://localhost:5000

4. To start the logic map, click the button on the interface.
