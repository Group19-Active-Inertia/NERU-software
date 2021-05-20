# Active-Inertia-NERU

## Folder layout

### **/classes**
Contains all custom classes.

### **/doc**
Contains all documentation.

### **/tests**
Contains unit tests.


## Communication between database
The format for some of these has not been decided yet, database team please let us know what formats would be best for you.
### Data read from database by the NERU
1. All NERU IPs, corresponding ports, latitude and longitude. 
2. Access to the MQTT broker, which can be a link to the downloadable credential files or the files themselves. (link would likely be more useful)

### Data written to database by the NERU
1. The NERU's own IP (in case it changes).
2. New disturbance records

### Other communication
1. Logging in