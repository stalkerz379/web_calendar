# web_calendar
Web calendar project

### Requirements
#### Stage 1/4: What should I do today?

- [x] Create a resource that handles GET requests for the /event/today endpoint and sends the following JSON object as a response:
`{"data":"There are no events for today!"}`

####  Stage 2/4: GET vs POST

Create a new resource that will handle POST requests for the /event endpoint. It must require the following arguments in the request body:

- [x] An event argument of the str type. If this argument is missing, please, respond with the following error message: The event name is required!
- [x] A date argument of the inputs.date type. If this argument is missing or it has the wrong format, please, respond with the following error message: The event date with the correct format is required! The correct format is `YYYY-MM-DD`!
- [x] If a user sends the correct response, display the following message: The event has been added!, and show the user data:
```
{
    "message": "The event has been added!",
    "event": "Client event name",
    "date": "Client date"
}
```

#### Stage 3/4: Relax

Create a model to save events to the database. The table should contain the following columns:

- [x] id of the INTEGER type. It should be our PRIMARY KEY.
- [x] event of the VARCHAR type. It should be NOT NULL.
- [x] date of the DATE type. It should be NOT NULL.
- [x] You can use any name for your database.

Now your REST API should have the following features:

- [x] `POST` request for the `/event endpoint` should save the event to your database. It should require the same arguments as in the previous stage.
- [x] `GET` request for the `/event endpoint` should return all the events from the database.
- [x] `GET` request for the `/event/today` endpoint should return the list of today's events.

#### Stage 4/4: Back to the future

In this stage, add a resource with the `/event/<int:id>` URL. It should handle the following requests:

- [x] A `GET` request should return the event with the ID in `JSON` format. If an event doesn't exist, return `404` with the following message: `The event doesn't exist!`.
- [x] A `DELETE` request should delete the event with the given ID and respond with the following response body:
```
{
    "message": "The event has been deleted!"
}
```
- [x] If the event with the ID doesn't exist, return `404` with the message The event doesn't exist!
- [x] A `GET` request for the /event endpoint with start_time and end_time parameters should return a list of events for the given time range. If the arguments are missing, return the list of all events.
- [x] The URLs from the previous stage should work in the same way.

