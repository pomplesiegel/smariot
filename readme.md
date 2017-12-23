### SmarIoT
#### Barebones REST App for IoT
Very simple REST application written using Python and the Flask framework. Can be depolyed to [Heroku](https://heroku.com)'s free-tier and hookedup to [TheThingsNetwork](https://thethingsnetwork.org) via `HTTP Integration` feature. Receives data on `/recv` endpoint and displays five latest messages on the homepage.

### Live Preview
Hosted on [Heroku](https://smariot.herokuapp.com/)

### ToDo
- ~Hook-up to TTN for testing~
- ~Auto-refresh homepage~
- ~Timestamps for requests~
- Pretty printing of requests on homepage
- Save data to DB
- DB housekeeping (rotate out old data so that it stays under 10k rows limit)
- Visualization of data (charts and stuff)
