# Active-Inertia-NERU

## Description
This repository contains the software meant to be run on NERU units to communicate disturbances as well as including functionality required to authenticate users, ensure security of communications and schedule events to simulate disturbances ahead of time to test the network. The communication protocols (CoAP and MQTT) run concurrently allowing for minimum average delays in communication.

### Example disturbance message

{
      "Latitude" : 37.9838,
      "Longitude" : 23.7275,
      "device_id_1" : "Athens 1",
      "time" : "2021-06-12 12:01:30.001206",
      "type" : "Phase Shift"
}

### Example arrival message

{
    "device_id_1" : "Newcastle 1",
    "delay" : "0:00:00.010506",
    "message received" : {
      "Latitude" : 37.9838,
      "Longitude" : 23.7275,
      "device_id_1" : "Athens 1",
      "time" : "2021-06-12 12:01:30.001206",
      "type" : "Phase Shift"
    },
    "message type" : "CoAP",
    "time" : "2021-06-12 12:01:30.011712"
}

### Example scheduling message

sched 2021-06-04 12:01:30


## Folder layout

### **/classes**
Contains all custom classes.

### **/doc**
Contains all documentation.

### **/tests**
Contains unit tests.


## Communication between database
The NERU communicates with the database, sending messages containing details about detected inertia events. It sends these messages to nearby NERUs using CoAP, and all NERUs in the network using MQTT (on the 'iot/topic' topic). The MQTT broker then forwards these messages to the database. In order to authenticate a NERU machine and update its information (such as its ID or Longitude and Latitude) on the database, the NERU also communicates with the database. On arrival of a message a delay value is also calculated and this is sent via MQTT to the broker (on the 'firebase' topic). NERUs are also able to receive commands (in the form of MQTT messages) to schedule a disturbance to be simulated at an appointed time in the future (on the 'update' topic).

### Data read from database by the NERU
1. All NERU IPs, corresponding ports, latitude and longitude. 
2. Access to the MQTT broker, which can be a link to the downloadable credential files or the files themselves. (link would likely be more useful)

### Data written to database by the NERU
1. The NERU's own IP (in case it changes).
2. New disturbance records
3. Arrival messages documenting delays

### Other communication
1. Logging in


## Instruction for running

Clone the repository on your machine using the following command. Make sure that you have git installed for this step:

```
git clone https://github.com/Group19-Active-Inertia/NERU-software
```

Ensure that you have you latest version of python and proceed to download the required dependencies with the following command:

```
pip3 install -r requirements.txt
```

You can then run the program as follows:

```
python3 main.py
```

For best results, you should have a time service/daemon to maintain good accuracy for your clock, such as ntpd or chrony. This is important for accurate delay measurement. For our simulations we used Raspberry Pi units to simulate the NERUs. These units had chrony installed and used PPS capable GPS receivers (In the form of a Raspberry Pi Hardware Attached on Top (HAT) device) as a time source to discipline the system clock and achieve microsecond accuracy (KPPS). However, even just using a time daemon like chrony can help achieve millisecond accuracy, which is satisfactory for the purposes of delay measurement.
