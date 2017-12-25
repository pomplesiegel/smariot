### SmarIoT
#### Barebones REST App for IoT
A very simple REST application written using Python and the Flask framework. Can be quickly depolyed to [Heroku](https://heroku.com)'s free-tier and hooked up to [TheThingsNetwork](https://thethingsnetwork.org) via `HTTP Integration` feature. 

- `POST` and `GET` implemented on the `/data` endpoint. Homepage shows the messages in memory, five latest messages retained. `POST`ed data is also persisted to DB
- Can `GET` in DB via the `/db` endpoint, an optional number provides the number of records to retrieve. Eg: `GET` on `/db/5` will return 5 latest records from the DB
- Data in DB can be visualized as a line graph via the `/viz` endpoint (WIP:returns random dummy data for now)

### Live Preview
Hosted on [Heroku](https://smariot.herokuapp.com/), and hooked up to stream of LoRaWAN messages from TTN (one message exepected every 3 mins). Messages themselves are sent from a LoRaWAN endnode.

### ToDo
- ~Hook-up to TTN for testing~
- ~Auto-refresh homepage~
- ~Timestamps for requests~
- ~Implement GET on the endpoint~
- Pretty printing of requests on homepage
- ~Save data to DB~
- ~Add `/db` Endpoint for fetching data from DB~
- Add fectching options (~by count~, by time etc)
- DB housekeeping (rotate out old data so that it stays under 10k rows limit)
- Visualization of data (~charts and stuff~)
