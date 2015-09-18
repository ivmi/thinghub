REST Web server for devices to post data and handle requests.

Example data
temperature,system=boiler,device=sensor1 value=32.8 1437171724

API:
update fields
GET /fields/update
    api_key (string) - Write API Key for the field
    measurement
    system
    device
    time_created (datetime) - Date when this feed entry was created, in ISO 8601 format, for example: 2014-12-31 23:59:59 . Time zones can be specified via the timezone parameter (optional)
    value

Retrieve feeds
GET /fields/feeds    
    api_key (string) Read API Key for this specific Channel (optional--no key required for public channels)
    results (integer) Number of entries to retrieve, 8000 max, default of 100 (optional)
    days (integer) Number of 24-hour periods before now to include in feed (optional)
    start (datetime) Start date in format YYYY-MM-DD%20HH:NN:SS (optional)
    end (datetime) End date in format YYYY-MM-DD%20HH:NN:SS (optional)
    timezone (string) Timezone identifier for this request (optional)
    offset (integer) Timezone offset that results should be displayed in. Please use the timezone parameter for greater accuracy. (optional)
    status (true/false) Include status updates in feed by setting "status=true" (optional)
    metadata (true/false) Include Channel's metadata by setting "metadata=true" (optional)
    location (true/false) Include latitude, longitude, and elevation in feed by setting "location=true" (optional)
    min (decimal) Minimum value to include in response (optional)
    max (decimal) Maximum value to include in response (optional)
    round (integer) Round to this many decimal places (optional)
    timescale (integer or string) Get first value in this many minutes, valid values: 10, 15, 20, 30, 60, 240, 720, 1440, "daily" (optional)
    sum (integer or string) Get sum of this many minutes, valid values: 10, 15, 20, 30, 60, 240, 720, 1440, "daily" (optional)
    average (integer or string) Get average of this many minutes, valid values: 10, 15, 20, 30, 60, 240, 720, 1440, "daily" (optional)
    median (integer or string) Get median of this many minutes, valid values: 10, 15, 20, 30, 60, 240, 720, 1440, "daily" (optional)

Tasks
    Add task
        GET /tasks/add
        
        
            
        