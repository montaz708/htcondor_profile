import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.igext as IG

pc = portal.Context()
request = rspec.Request()


params = pc.bindParameters()
tourDescription = \
"""
Testing Spark cluster environment
"""

#
# Setup the Tour info with the above description and instructions.
#
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)

# Create a link with type LAN
link = request.LAN("lan")

# Generate the nodes
for i in range(5):
    node = request.RawPC("node" + str(i))
    node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD"
    iface = node.addInterface("if" + str(i))
    iface.component_id = "eth1"
    iface.addAddress(rspec.IPv4Address("192.168.1." + str(i + 1), "255.255.255.0"))
    link.addInterface(iface)

    node.addService(rspec.Execute(shell="/bin/sh",
                                  command="sudo apt-get update -y"))
    node.addService(rspec.Execute(shell="/bin/sh",
                                  command="sudo apt-get install -y openjdk-8-jdk"))
    node.addService(rspec.Execute(shell="/bin/sh",
                                  command="export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/"))
    node.addService(rspec.Execute(shell="/bin/sh",
                                  command="sudo apt-get htcondor"))
    #figure out how to write condor config scripts    
    if i != 0:
        pass
        # start condor master here
    else:
        node.routable_control_ip = True

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec(request)
