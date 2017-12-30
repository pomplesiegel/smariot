# SmarIoT
##### Barebones REST App for IoT. Hooks up with TheThingsNetwork
![build](https://api.travis-ci.org/bhargavbhat/smariot.svg?branch=master)
[![Requirements Status](https://requires.io/github/bhargavbhat/smariot/requirements.svg?branch=master)](https://requires.io/github/bhargavbhat/smariot/requirements/?branch=master)

### What it is
- A very simple REST application written using Python and the Flask framework.
- Can be depolyed to [Heroku](https://heroku.com)'s free-tier
- Can be connected to [TheThingsNetwork](https://thethingsnetwork.org) via `HTTP Integration` to receive, store and visualize sensor data.


### What it does
- Receives incoming JSON data as `POST` on the `/data` endpoint. `POST`ed data is parsed and the relevant info is persisted to PostgreSQL DB. `POST`s are secured via an `API_KEY`. Unauthorized `POST`s will be rejected with a `401`

- Retrevies stored records as JSON via `GET` on the `/db` endpoint. A (optional) count of records to retrieve maybe specified. Eg: `GET` on `/db/15` will return 15 latest records (if available) whereas a simple `GET` on `/db` will return the latest record

- Data in DB can be visualized as a line graph via the `/viz` endpoint.


### Live Preview
A live instance is [hosted](https://smariot.herokuapp.com/) and hooked up to receive a stream of LoRaWAN messages from TTN (one message exepected every 5 mins). Messages themselves are sent from out from a [LoPy](https://pycom.io/product/lopy/) board.


### Run Your Own Instance
- Create a new heroku via [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

- Once the instance is up, navigate to Heroku's Dashboard -> _Your Application Name_ -> Settings and take note of the generated environment variable named `API_KEY`
![Imgur](https://i.imgur.com/Bn9QSxX.png)

- Follow TTN [documentation](https://www.thethingsnetwork.org/docs/applications/http/) and add a new `HTTP Integration`. Use your heroku's URL followed by `/data` for the URL field

- Ensure that the `Custom Header Name` is set to `x-api-key` and `Custom Header Value` is set to match the generated `API_KEY`
![Imgur](https://i.imgur.com/djzUnOm.png)

- Wait for some data to arrive. If everything is setup correctly, it'll show up on the homepage

### Customizing SmarIoT
Details in [customizing.md](customizing.md)

#### ToDo
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
