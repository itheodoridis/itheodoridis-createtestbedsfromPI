# itheodoridis-createtestbedsfromPI
# Description

Create testbeds for Cisco PyATS from device groups (e.g. switches) managed by Cisco Prime Infrastructure
The code in this repo is the result of common work from Ioannis Theodoridis and Katerina Dardoufa, engineers, co-workers, and friends.
The initial code that contains the idea of querrying an Enterprise's Prime Infrastrcture server for active network devices so that the device list and attributes can be used for various purposes, is contained in two different repositories created by Katerina Dardoufa at:
- https://github.com/kdardoufa/DeviceInfo_from_PI
- https://github.com/kdardoufa/CollectIP

The code in this repo is purposed for creating Cisco PyATS testbeds for active network devices per location. It's limited for switches as Device Type but it can easily be adjusted to include other types. It has adjustments compared to the initial code created by Katerina Dardoufa in order to querry the PI server for a full device list directly, instead of going through the device groups, as the main goal is speed.

Indeed the code should complete a full run in a few seconds for a few hundreds of devices.

The repo will soon be completed with a second script using the same technique to create the testbeds in memory using existing functions from the createtestbeds.py. This is usefull if you need to do something quickly in a script, without worrying about accessing disk/file locations.

# Installation - Configuration

To install just clone this repository and replace the values in the credentials.py file, as well as the location of your prime infrastructure and credentials in the primeapidata.py file.
Of course, the user credentials you use in those two files should already have been created on your devices/access servers. For PI especially lookup how you can create a user that will have access to the API but have no other access whatsoever, for security reasons.

The script runs as any other python script, for example:

<code>python3 CreateTestbeds.py</code>

The python requests library is required to be installed.

# Code adjustments
The code contains certain criteria for the search that you might want to adjust.
- Active only devices
- Type "Switches and Hubs" : You have to check the supported types/groups in Prime and choose the ones you want, or eliminate the criteria to get eveyrything. But be mindfull. Prime Infrastructure doesn't always recognize equipment as you would like it to, for example some router models or Cisco ISE. You really don't want any type of device in your testbeds and the ones you do want in, better be of the correct type!
- only IOS devices, not nxos. Again this is something you need to figure out for your topology. If you have nexus switches all over your network than by all means, don't exclude them but you need to take this into account when you map the devices to PyATS device types (os, models, series, etc).
- In the original code I would limit the devices to main sites only, not branches. You can add criteria to the if statement or substract from it to adjust the result.

Like most people playing with REST APIs we used Postman to play with the requests for adjusting the python code. Get it at https://www.postman.com .

# Cisco Prime Infrastructure API
You can find a downloadable programmaing guide for all active Cisco Prime Infrastructure versions in this page:
https://www.cisco.com/c/en/us/support/cloud-systems-management/prime-infrastructure/products-programming-reference-guides-list.html

There is also live documentation. If you want to start from there, go to https://developer.cisco.com/site/prime-infrastructure/
Also check the tutorial at https://developer.cisco.com/site/prime-infrastructure/documents/api-reference/tutorial/ 
You can also check the API in your own server by appending /webacs/api/v4/ to your server https url (notice the version, some api calls are version dependant, v1 is depricated but v2 is very much in use).

# Additional Notes

As the requests are made to the PI REST API, you could of course adapt this to use it with DNA Center, if that is what you use instead of Prime Infrastructure. You can probably find some scripts getting the device list from DNA Center, in several Devnet Learning Labs and Courses, or from Adam Radford, the man himself, in his github repo. I will not link to those repos here.

The reason we made this script is that Prime Infrastructure, unlike a documentation system or a NSOT (Network Source of Truth) like Netbox, provides access to what is active and operational on the network. An NSOT system should give you access to what should be active on the network which is not the ideal source to run operational tasks and tests. If what you need is a way to get Testsbeds created from Netbox list of Devices, I think that is already supported or will soon be, directly on PyATS.

If you like PyATS, follow them everywhere (webex teams, Twitter, developer.cisco.com), they are a wonderfull team of gifted human beings.

If you have questions you can look me up on Twitter @mythryll. 

My blog is at http://www.mythryll.com/

This is not an example for proper REST API usage. You can find plenty of courses out there to teach you just that, a lot in Cisco Devnet Learning Paths as well, at https://developer.cisco.com/

