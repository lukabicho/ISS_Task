This program works by fetching live api data from https://wheretheiss.at/ , appending it to a satellite_data.jsonl datalake, 
parsing that data to a GeoLocation.py. The result of the GeoLocator id then stored in PostgreSQL database.
We then fetch the neccessary data from the database tables and log the output into the terminal.
*****************
We need an .env file to configure API keys and PostgreSQL database configuration parameters.
An .env example is provided. 

The user also can set the time interval to their liking from the main.py.

The logs are also saved into an iss_tracker.log file