### SmarIoT
#### Barebones REST App for IoT
A very simple REST application written using Python and the Flask framework. Can be quickly depolyed to [Heroku](https://heroku.com)'s free-tier and hooked up to [TheThingsNetwork](https://thethingsnetwork.org) via `HTTP Integration` feature. 

- Send incoming data via `POST` to the `/data` endpoint. A `GET` on this endpoint (and the homepage) show the most recent messages. `POST`ed data is also persisted to DB
- `GET` present in the DB via the `/db` endpoint, an optional number determines the count records to retrieved. Eg: `GET` on `/db/15` will return 15 latest records (if available) from the DB
- Data in DB can be visualized as a line graph via the `/viz` endpoint

### Live Preview
Hosted on [Heroku](https://smariot.herokuapp.com/), and hooked up to stream of LoRaWAN messages from TTN (one message exepected every 3 mins). Messages themselves are sent from a LoRaWAN endnode.

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
- Add fectching via parameters (~by max count~, by timestamp, by Hardware ID)
- DB housekeeping (rotate out old data so that it stays under 10k rows limit)
- Pretty printing of requests on homepage using socketio
- Add a "live" chart (chart data as it is `POST`ed) using socketio
