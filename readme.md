### SmarIoT
#### Barebones REST App for IoT
A very simple REST application written using Python and the Flask framework. Can be quickly depolyed to [Heroku](https://heroku.com)'s free-tier and hooked up to [TheThingsNetwork](https://thethingsnetwork.org) via `HTTP Integration` feature. `POST` and `GET` implemented on the `/data` endpoint (five latest messages retained). Homepage shows the messages in memory.

### Live Preview
Hosted on [Heroku](https://smariot.herokuapp.com/), and hooked up to stream of LoRaWAN messages from TTN (one message exepected every 3 mins). Messages themselves are sent from a LoRaWAN endnode.

### ToDo
- ~Hook-up to TTN for testing~
- ~Auto-refresh homepage~
- ~Timestamps for requests~
- ~Implement GET on the endpoint~
- Pretty printing of requests on homepage
- Save data to DB
- DB housekeeping (rotate out old data so that it stays under 10k rows limit)
- Visualization of data (charts and stuff)
