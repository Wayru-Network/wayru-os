## WayruOS VM Setup

### Prerequisites

- Virtual Box

#### Steps

Download a stable release of the wayru-os-23.1.0-alpha-x86-generic-generic-ext4-combined.img

##### Convert downloaded img to VBox drive
- Open a terminal and go in the folder where you have downloaded the file (On windows make sure you are located on /Oracle/VirtualBox/)
- Convert it to native VBox format by writing this in command line:
>VBoxManage convertfromraw --format VDI wayru-os-*.img VDI-NAME.vdi.

This will create the .vdi file which will be a virtual drive for VBox virtual machine.

##### Creating the VM
Execute the following commands 
> VBoxManage createvm --name "WayruOS" --ostype "Linux26" --register
> VBoxManage modifyvm "WayruOS" --memory 512 --cpus 1 --nic1 nat --nic2 bridged
> VBoxManage storagectl "WayruOS" --name "SATA Controller" --add sata --controller IntelAhci
> VBoxManage storageattach "WayruOS" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium /route/to/disk/VDI-NAME.vdi

##### Start the VM
> VBoxManage startvm "WayruOS"

-Wait 4s for Grub to initialize openWRT.
-Press ENTER once the text stops scrolling.

##### Set up your VM

###### Configure the root password to prevent unauthorized access.
Execute the following command:
>passwd

###### Configure firewall rules for SSH access
Execute the following commands:

>uci add firewall rule
>uci set firewall.@rule[-1].src='wan'
>uci set firewall.@rule[-1].target='ACCEPT'
>uci set firewall.@rule[-1].proto='tcp'
>uci set firewall.@rule[-1].dest_port='22'
>uci set firewall.@rule[-1].name='Allow-SSH'
>uci commit firewall

To apply changes execute the following command:
>/etc/init.d/firewall restart



