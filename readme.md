### SmarIoT
#### Barebones REST App for IoT. Hooks up with [TheThingsNetwork](https://thethingsnetwork.org)
A very simple REST application written using Python and the Flask framework. Can be depolyed to [Heroku](https://heroku.com)'s free-tier and hooked up to [TheThingsNetwork](https://thethingsnetwork.org) via `HTTP Integration`

- Receives incoming JSON data as `POST` on the `/data` endpoint. A `GET` on this endpoint show the most recent message. `POST`ed data is parsed and the relevant info is persisted to PostgreSQL. `POST`s are secured via an `API_KEY`. Unauthorized `POST`s will be rejected with a `401`

- A `GET` on the `/db` endpoint will return data available in the DB. An optional count of records to retrieve is supported. Eg: `GET` on `/db/15` will return 15 latest records (if available) where as a simple `GET` on `/db` will return the latest record (which is the same as what `/data` returns)

- Data in DB can be visualized as a line graph via the `/viz` endpoint. A dropdown is presented so that data from different endnodes may be visualized separately.

### Live Preview
Hosted on [Heroku](https://smariot.herokuapp.com/), and hooked up to stream of LoRaWAN messages from TTN (one message exepected every 5 mins). Messages themselves are sent from out from a [LoPy](https://pycom.io/product/lopy/) device.

### ToDo
- ~Hook-up to TTN for testing~
- ~Auto-refresh homepage~
- ~Timestamps for requests~
- ~Implement GET on the endpoint~
- ~Save data to DB~
- ~Add `/db` Endpoint for fetching data from DB~
- ~Visualization of data (charts and stuff)~
- ~Simple API Key auth for `POST`ing data to `/data`~
- ~Upgrade to new data format~
- ~Upgrade to chart.js ver 2.x~
- ~Plot multi-line chart~
- ~Get rid of cache + prep socketio (local machine)~
- ~Pretty printing of requests on homepage using socketio~
- ~Separate chart for each endnode's data~
- Add fectching via parameters (~by max count~, by timestamp, by Hardware ID)
- DB housekeeping (rotate out old data so that it stays under 10k rows limit)
- Add a "live" chart (chart data as it is `POST`ed) using socketio
