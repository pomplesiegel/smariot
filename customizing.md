# Customizing SmarIoT

SmarIoT should be fairly straight forward to customize. Here's the "big-picture" stuff:
- The python (and flask) source is contained in a single file `app.py`. 
- `templates` directory contains Jinja templates and `static` directory contains the CSS files.
    - `main.css` is use throughout the website
    - `iframe.css` is used for `iframes` (duh!) on the homepage for dumping incoming raw JSON and on the `/viz` endpoint for showing line charts corresponding to each endnode
- Javascript files are loaded off of CDNs. SmarIoT uses [ChartJS](http://www.chartjs.org) ver 2.

### ORM
- SmarIoT uses the [SQLAlchemy](https://www.sqlalchemy.org) ORM toolkit
- Two ORM classes are defined:
  - `DeviceData` : Stores basic device (board/endnode) info (currently this is only being used to generate the endnode/device list)
  - `SensorData` : Parses and stores sensor readings (this guy holds all sensor readings in the `msg` field)
- `hw_id` is used to keep track of which endnode sent what

### Data Parsing Functions
- `msg_parse_val` contains the logic for interpreting raw payload data from TTN
- This function _WILL_ need to be modified to suit the data your hardware is sending


### Adapting for source other than TTN
- `msg_get_hw_id`, `msg_get_value` and `msg_get_timestamp` are abstractions for extracting the Hardware ID, Sensor Data and Timestamp respectively. These will need to be modified for as per the JSON structure
- `msg_parse_val` will likely need to updated to remove the `base64` decoding
