# itheodoridis-createtestbedsfromPI
# Description

Create testbeds for Cisco PyATS from device groups (e.g. switches) managed by Cisco Prime Infrastructure
The code in this repo is the result of common work from Ioannis Theodoridis and Katerina Dardoufa, engineers, co-workers, and friends.
The initial code that contains the idea of querrying an Enterprise's Prime Infrastrcture server for active network devices so that the device list and attributes can be used for various purposes, is contained in two different repositories created by Katerina Dardoufa at:
- https://github.com/kdardoufa/DeviceInfo_from_PI
- https://github.com/kdardoufa/CollectIP

The code in this repo is purposed for creating Cisco PyATS testbeds for active network devices per location. It's limited for switches as Device Type but it can easily be adjusted to include other types. It has adjustments compared to the initial code created by Katerina Darfoufa in order to querry the PI server for a full device list directly, instead of going through the device groups, as the main goal is speed.

Indeed the code should complete a full run in a few seconds for a few hundreds of devices.

The repo will soon be completed with a second script using the same technique to create the testbeds in memory using existing functions from the createtestbeds.py. This is usefull if you need to do something quickly in a script, without worrying about accessing disk/file locations.

# Installation - Configuration

To install just clone this repository and replace the values in the credentials.py file, as well as the location of your prime infrastructure and credentials in the primeapidata.py file.
Of course, the user credentials you use in those two files should already have been created on your devices/access servers. For PI especially lookup how you can create a user that will have access to the API but have no other access whatsoever, for security reasons.

The script runs as any other python script, for example:

<code>python3 CreateTestbeds.py</code>

# Additional Notes

As the requests are made to the PI REST API, you could of course adapt this to use it with DNA Center, if that is what you use instead of Prime Infrastructure. You can probably find some scripts getting the device list from DNA Center, in several Devnet Learning Labs and Courses, or from Adam Radford, the man himself, in his github repo. I will not link to those repos here.

The reason we made this script is that Prime Infrastructure, unlike a documentation system or a NSOT (Network Source of Truth) like Netbox, provides access to what is active and operational on the network. An NSOT system should give you access to what should be active on the network which is not the ideal source to run operational tasks and tests. If what you need is a way to get Testsbeds created from Netbox list of Devices, I think that is already supported or will soon be, directly on PyATS.

If you like PyATS, follow them everywhere (webex teams, Twitter, developer.cisco.com), they are a wonderfull team of gifted human beings.

If you have questions you can look me up on Twitter @mythryll. 
My blog is at http://www.mythryll.com/
mail : itheodori@gmail.com

