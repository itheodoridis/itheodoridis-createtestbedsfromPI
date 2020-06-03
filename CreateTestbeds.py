"""
Create testbeds for Cisco PyATS from device groups (e.g. switches) managed by Cisco Prime Infrastructure The code in this repo is the result of common work from Ioannis Theodoridis and Katerina Dardoufa (https://github.com/kdardoufa), engineers, co-workers, and friends. The original code that contains the idea of querrying an Enterprise's Prime Infrastrcture server for active network devices so that the device list and attributes can be used for various purposes, is contained in two different repositories created by Katerina Dardoufa at:

    https://github.com/kdardoufa/DeviceInfo_from_PI
    https://github.com/kdardoufa/CollectIP

The code in this repo is purposed for creating Cisco PyATS testbeds for active network devices per location. It's limited for switches as Device Type but it can easily be adjusted to include other types. It has adjustments compared to the initial code created by Katerina Dardoufa in order to querry the PI server for a full device list directly, instead of going through the device groups, as the main goal is speed.

Indeed the code should complete a full run in a few seconds for a few hundreds of devices.
"""

import requests
import json
import logging
from requests.auth import HTTPBasicAuth
import time
import yaml
from credentials import dev_username, dev_password, dev_enablepass
from primeapidata import PI_ADDRESS, USERNAME, PASSWORD

# this line is used to get rid of the fact that your server probably has a self signed certificate that you can't verify in code.
requests.packages.urllib3.disable_warnings()

# this line as well as the other logging commands create logs to help you verify what the code did. They are not necessary and can be removed from the code (don't forget to remove all instances)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='CreateTestbeds.log', level=logging.INFO)

# this function gets the list of devices from prime infrastructure as a list of dictionaries.
def getSimpleDevicesList():
    DeviceList = []
    logging.info(" - Getting all devices url list")
    url = "https://"+PI_ADDRESS+"/webacs/api/v4/data/Devices.json?.full=true&.maxResults=1000"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
    r_json = response.json()
    for entity in r_json['queryResponse']['entity']:
        device = entity["devicesDTO"]
        # this if block limits devices to reachable only, switches and excludes NXOS devices
        if (device["reachability"] == "REACHABLE") and (
        device["productFamily"] == "Switches and Hubs") and ("nx-os" not in device["softwareType"].lower()):
            DeviceList.append(device)
    logging.info(" - Got all devices in list of dictionaries")
    return (DeviceList)

# this creates a list of the separate locations defined in prime infrastructure for the devices already in the list of devices.
def getLocationsList(DevList):
    logging.info(" - Getting all different locations")
    LocationsList = []
    for device in DevList:
        location = device["location"].strip()
        if location not in LocationsList:
            LocationsList.append(location)
            logging.info(f" - Appended location {location}")
    return(LocationsList)
# End of Function

# this functions creates the testbeds in files per location (one testbed for each location defined in the previous function).
def createTestbeds(DevList, LocList):
    Devs_per_loc = dict()
    for location in LocList:
        Devs_per_loc[location] = []

    # define protocol  for each device depending on version and rest of details
    for device in DevList:
        location = device["location"].strip()
        if ("2950" in device["deviceType"]) or ("3550" in device["deviceType"]) or ("3750" in device["deviceType"]):
            deviceProtocol = "telnet"
            devicePort = "23"
            deviceName = device["deviceName"]
        else:
            deviceProtocol = "ssh"
            devicePort = "22"
            # the following line is necessary to get rid of the domain suffix or PyATS will not recognize the device hostname
            divdevname = device["deviceName"].split(".")
            deviceName = divdevname[0]
        deviceIpAddress = device["ipAddress"]
        deviceOS = device["softwareType"].lower()

        # define dict to contain device parameters and add to the list
        devdict = {
            "deviceName" : deviceName,
            "os" : deviceOS,
            "type" : "switch",
            "ip" : deviceIpAddress,
            "protocol" : deviceProtocol,
            "port" : devicePort
            }
        Devs_per_loc[location].append(devdict)

    logging.info(" - Creating Testbeds")
    for location in LocList:
        #this is the initial testbed block - this is actually optional
        initial_string = (f"testbed:\n"
                          f"  name: {location}\n"
                          f"  credentials:\n"
                          f"    default:\n"
                          f"      username: {dev_username}\n"
                          f"      password: {dev_password}\n"
                          f"    enable:\n"
                          f"      password: {dev_enablepass}\n")

        # testbed filename definition
        testbed_filename = location + ".yaml"
        # open filename and write testbed and devices blocks
        with open(testbed_filename, 'w') as writer:
            writer.write(initial_string)
            writer.write("\ndevices:\n")
            for device in Devs_per_loc[location]:
                writer.write(" "*2 + device["deviceName"] + ":\n")
                writer.write(" "*4 + "os: " + device["os"] + "\n")
                writer.write(" "*4 + "type: " + device["type"] + "\n")
                writer.write(" "*4 + "connections:\n")
                writer.write(" "*6 + "console:\n")
                writer.write(" "*8 + "ip: " + device["ip"] + "\n")
                writer.write(" "*8 + "protocol: " + device["protocol"] + "\n")
                writer.write(" "*8 + "port: " + device["port"] + "\n")
                # this was necessary for some of our old devices, using the latest version of the PyATS docker container
                if device["protocol"]=="ssh":
                  writer.write(" "*8 + "ssh_options: -o KexAlgorithms=+diffie-hellman-group1-sha1 -c aes128-cbc,3des-cbc,aes192-cbc,aes256-cbc\n")
                if device["protocol"]=="telnet":
                    writer.write(" "*8 + "settings:\n")
                    writer.write(" "*10 + "ESCAPE_CHAR_CHATTY_TERM_WAIT: 0.4\n")
                    writer.write(" "*10 + "ESCAPE_CHAR_PROMPT_WAIT: 0.4\n")
                    writer.write(" "*4 + "credentials:\n")
                    writer.write(" "*6 + "default:\n")
                    writer.write(" "*8 + f"username: {dev_username}\n")
                    writer.write(" "*8 + f"password: {dev_password}\n")
                    writer.write(" "*6 + "enable:\n")
                    writer.write(" "*8+ f"password: {dev_password}\n")
    return
# End of function

# Main Function
def main():
    SimpleDevicesList = getSimpleDevicesList()
    LocationsList = getLocationsList(SimpleDevicesList)
    createTestbeds(SimpleDevicesList, LocationsList)
    logging.info(" - All testbeds have been created.\nEND")
    return()


if __name__ == "__main__":
    main()
