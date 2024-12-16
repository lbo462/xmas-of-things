# Logic map

The logic map is a python script that transforms sensors data into actions.

Here's how it works:
- Read uplink of a device on TTN
- Apply some business rules to determine actions to do
- Sends these actions as payload on the downlink topic of the device waiting these actions

Find details more on the [TTN documentation](TTN/README.md).

## How to start the logic map

__Work in `API/src/`__:

```bash
cd API/src/
```

- Create a [python virtual environment](https://docs.python.org/3/library/venv.html) and install the dependencies with 

```bash
pip install -r requirements.txt  # Only in the virtual env!
```

- Create a `.env` file containing the following:

```
TTN_APP_ID=<app-name>
TTN_TENANT_ID=ttn
TTN_API_KEY=<api-key>
TTN_BASE_URL=eu1.cloud.thethings.network
TTN_PORT=1883
```

Replace `<app-name>` and `<api-key>` with the correct values.

- Start the main script to launch the API:

```bash
python main.py
```

- Go on the web interface at http://localhost:5000 and click on the button to turn on the logic map.
