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
    if i == 0:
        node = request.RawPC("head")
    else:
        node = request.RawPC("node" + str(i))
    node.cores = 4
    node.ram = 4096
    node.routable_countrol_ip = "true"
    node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD"
    iface = node.addInterface("if" + str(i))
    iface.component_id = "eth1"
    iface.addAddress(rspec.IPv4Address("192.168.1." + str(i + 1), "255.255.255.0"))
    link.addInterface(iface)
    node.addService(rspec.Execute(shell="/bin/sh",
                                 command="sudo su"))
    node.addService(rspec.Execute(shell="/bin/sh",
                                  command="sudo apt-get update -y"))
    node.addService(rspec.Execute(shell="/bin/sh",
                                  command="sudo apt-get install -y openjdk-8-jdk"))
    node.addService(rspec.Execute(shell="/bin/sh",
                                  command="export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/"))
    node.addService(rspec.Execute(shell="/bin/sh",
                                  command="sudo bash /local/repository/passwordless.sh"))
    node.addService(rspec.Execute(shell="/bin/sh",
                                 command="sudo bash /local/repository/install_docker.sh"))
    node.addService(rspec.Execute(shell="/bin/sh",
                                  command="DEBIAN_FRONTEND=noninteractive sudo apt-get -y install htcondor"))
    node.addService(rspec.Execute(shell="/bin/sh",
                                 command="sudo cp /local/repository/condor_config /etc/condor/condor_config"))
# add the condor user to the docker group so it can execute commands?
    node.addService(rspec.Execute(shell="/bin/sh",
                                  command="sudo usermod -aG docker condor"))
# Print the RSpec to the enclosing page.
    if i == 0:
        node.addService(rspec.Execute(
            shell="/bin/sh",
            command="sudo docker swarm init --advertise-addr 192.168.1.1"
        ))
        node.addService(rspec.Execute(
            shell="/bin/sh",
            command="sudo mkdir /docker_key"
        ))
        node.addService(rspec.Execute(
            shell="/bin/sh",
            command="docker swarm join-token worker -q > ~/token.txt"
        ))
        node.addService(rspec.Execute(
            shell="/bin/sh",
            command="sudo mv ~/token.txt /docker_key/"
        ))
        node.addService(rspec.Execute(
            shell="/bin/sh",
            command="sudo apt install nfs-kernel-server -y"
        ))
        node.addService(rspec.Execute(
            shell="/bin/sh",
            command="sudo systemctl start nfs-kernel-server.service"
        ))
        node.addService(rspec.Execute(
            shell="/bin/sh",
            command="cp /local/repository/exports /etc/exports"
        ))
        node.addService(rspec.Execute(
            shell="/bin/sh",
            command="exportfs -a"
        ))
    else:
        node.addService(rspec.Execute(
            shell="/bin/sh",
            command="sudo apt install nfs-common -y"
        ))
        node.addService(rspec.Execute(
            shell="/bin/sh",
            command="sudo mkdir /docker_key"
        ))
        node.addService(rspec.Execute(
            shell="/bin/sh",
            command="sudo mount 192.168.1.1:/docker_key /docker_key"
        ))
portal.context.printRequestRSpec(request)
