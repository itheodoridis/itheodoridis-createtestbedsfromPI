import requests
import json
import logging
from requests.auth import HTTPBasicAuth
import time
import yaml
from credentials import dev_username, dev_password, dev_enablepass
from primeapidata import PI_ADDRESS, USERNAME, PASSWORD

requests.packages.urllib3.disable_warnings()

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='CreateTestbeds.log', level=logging.INFO)

def getSimpleDevicesList():
    DeviceList = []
    logging.info(" - Getting all devices url list")
    url = "https://"+PI_ADDRESS+"/webacs/api/v4/data/Devices.json?.full=true&.maxResults=1000"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
    r_json = response.json()
    for entity in r_json['queryResponse']['entity']:
        device = entity["devicesDTO"]
        if (device["reachability"] == "REACHABLE") and (
        device["productFamily"] == "Switches and Hubs") and (
        "YPOK" not in device["location"]) and ("nx-os" not in device["softwareType"].lower()):
            DeviceList.append(device)
    logging.info(" - Got all devices in list of dictionaries")
    return (DeviceList)

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

def createTestbeds(DevList, LocList):
    Devs_per_loc = dict()
    for location in LocList:
        Devs_per_loc[location] = []

    for device in DevList:
        location = device["location"].strip()
        if "2950" in device["deviceType"]:
            deviceProtocol = "telnet"
            devicePort = "23"
            deviceName = device["deviceName"]
        else:
            deviceProtocol = "ssh"
            devicePort = "22"
            divdevname = device["deviceName"].split(".")
            deviceName = divdevname[0]
        deviceIpAddress = device["ipAddress"]
        deviceOS = device["softwareType"].lower()

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
        initial_string = (f"testbed:\n"
                          f"  name: {location}\n"
                          f"  credentials:\n"
                          f"    default:\n"
                          f"      username: {dev_username}\n"
                          f"      password: {dev_password}\n"
                          f"      enable:\n"
                          f"        password: {dev_enablepass}\n")

        testbed_filename = location + ".yaml"
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
                if device["protocol"]=="ssh":
                  writer.write(" "*8 + "ssh_options: -o KexAlgorithms=+diffie-hellman-group1-sha1\n")
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
