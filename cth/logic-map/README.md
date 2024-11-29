# Logic map

This defines the business rules transforming sensors data into action commands.

- __Village lights__ (require _noise level_)

When the noise level exceeds _some value_ trigger the village lights

- __Tree light__ (require _brightness level_)

When the brightness level drops, light up the Christmas tree.

- __Snow spray__ (require _temperature_)

When the temperatures drop, trigger the snow spray

## Other commands

- __Billboard text__

Send text ID

- __Ferris wheel__

Send a boolean to trigger the ferris wheel

- __Music__

Send the music ID

## Technical details

### How to start the script

- Create a [python virtual environment](https://docs.python.org/3/library/venv.html) and install the dependencies with 

```bash
pip install -r requirements.txt
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

- Start the script

```bash
python main.py
```

- ... or start other sample script

```bash
python read_sensors.py  # read sensors data
# or
python read_actions_queue.py  # read actions
```
