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
- Pretty printing of requests on homepage
- Load latest 5 messages from DB into cache on app restart
- ~Save data to DB~
- ~Add `/db` Endpoint for fetching data from DB~
- Add fectching options (~by count~, by time etc)
- DB housekeeping (rotate out old data so that it stays under 10k rows limit)
- ~Visualization of data (charts and stuff)~
- Add a "live" chart (chart data as it is `POST`ed)
- ~Simple API Key auth for `POST`ing data to `/data`~
