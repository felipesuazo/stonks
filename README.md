# Twitch Event Subscription
### Events tracking:
- channel.follow
- stream.online
- stream.offline

### Websockets
I didn't complete de websocket part. I'm not sure how to apply it in this Framework.
With Firebase is easy.

### Event table structure
The structure for this database table is:
- id
- streamer_name
- event_type
- viewer_name
- created_at

Also it have two indexes for a fast access to the data. One with the streamer_name and one
using streamer_name and event_type

### How would you deploy the above on AWS? 
We can have two applications. One for receive the Twitch Events and save them to  the database and one
for expose the web endpoints. The application for the events can be written in GO, since GO is powerful
for multithreading and can process the information very fast. The other application can be in any language.

### Where do you see bottlenecks in your proposed architecture and how would you approach scaling this app starting from 100 reqs/day to 900MM reqs/day over 6 months?
The amount of data is very big. We can process the data and send to a Big Query or a database able to manage these streams and
since the web app only cares about the last 10 events, we can have them in Firebase to show them.

For the event processing we can use a GO application with an Elastic Load Balancer and scale the app having
multiples instances of the app.
