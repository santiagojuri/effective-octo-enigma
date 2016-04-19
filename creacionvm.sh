#!/bin/bash
if [ $# -ne 3 ]; then
	echo "$0 necesita tres argumentos"
	echo " $0 <nombre> <N cpus> <Ram Size>"
	exit 0
fi
VM=$1
NCpus=$2
Memsize=$3
#Unicacion hizo ej: /home/dhernandez49/Descargas/ubuntu-14.04.4-desktop-amd64.iso
#Es necesario tener el .iso en el mismo Directorio que este script
DirectorioIso=$(pwd)
#Cambiar nombreIso , por la imagen del OS que desea instalar. 
nombreIso=/ubuntu-14.04.4-desktop-amd64.iso
ubicacionIso=$DirectorioIso$nombreIso
VBoxManage createhd --filename $VM.vdi --size 6000
VBoxManage createvm --name $VM --ostype "Windows2008_64" --register
VBoxManage storagectl $VM --name "SATA Controller" --add sata --controller IntelAHCI
VBoxManage storageattach $VM --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium $VM.vdi
VBoxManage storagectl $VM --name "IDE Controller" --add ide
VBoxManage storageattach $VM --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium $ubicacionIso
VBoxManage modifyvm $VM --ioapic on
VBoxManage modifyvm $VM --boot1 dvd --boot2 disk --boot3 none --boot4 none
VBoxManage modifyvm $VM --memory $Memsize --vram 128
VBoxmanage modifyvm $VM --cpus $2
echo "El Software $0 a creado exitosamente la maquina virtual" 
