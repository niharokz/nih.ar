---
title : "Arch Linux installation Guide"
subtitle : "Arch Installation process is the gap between newbie and pro. Any Linux installation without any installer is good way to understand basic linux architecture."
showInHome : True
date : 2023-09-16
---
            

Are you eager to dive into the world of Arch Linux with dwm, but feeling overwhelmed by the installation process? Fear not! This step-by-step guide will walk you through the installation process, making it easy to set up your system and get started with your Arch Linux adventure.

## 1. Create a Bootable Disk

Begin by creating a bootable disk with the Arch Linux ISO. Use the lsblk command to identify your USB drive, then use dd to write the ISO to the disk:

    lsblk
    dd bs=4M if=path/to/archlinux-version-x86_64.iso of=/dev/disk/by-id/usb-My_flash_drive conv=fsync oflag=direct status=progress

## 2. Connect to the Internet

For wireless connection, use iwctl. List available networks, then connect to your desired network:

    iwctl
    station device get-networks
    iwctl --passphrase passphrase station device connect SSID

## 3. Clear/Format Disk

Clear and format your disk using fdisk:

    fdisk /dev/sda
    g   # create new gpt label
    p   # print the partition table
    n   # create a new partition
    d   # delete a partition
    q   # quit without saving changes
    w   # write the new partition table and exit

Format disk type:

    mkfs.fat -F32 /dev/sda1
    mkfs.ext4 /dev/sda2

## 4. Mounting and File Structure

Mount your partitions and create necessary directories:

    mount /dev/sda2 /mnt
    mkdir -p /mnt/{home,data,etc}
    mount /dev/sdb1 /mnt/data

## 5. Basic Setup

Generate fstab and chroot into the new system:

    genfstab -U -p /mnt >> /mnt/etc/fstab
    pacstrap -i /mnt base
    arch-chroot /mnt

## 6. Install Software

Install necessary software packages:

    pacman -S linux-lts linux-lts-headers base-devel linux-firmware vim networkmanager wpa_supplicant wireless_tools netctl dialog nvidia-lts nvidia-utils grub efibootmgr os-prober mtools dosfstools intel-ucode xorg-server xorg neofetch pulseaudio pamixer termite dolphin git vlc vifm i3

## 7. System Settings

Set up time and language:

    ln -sf /usr/share/zoneinfo/Asia/Kolkata > /etc/localtime
    hwclock --systohc
    vim /etc/locale.gen   # uncomment desired locale
    locale-gen
    echo "LANG=en_US.UTF-8" > /etc/locale.conf

Initiate Linux:

    mkinitcpio -p linux-lts

## 8. User Addition

Create a new user and enable them as admin:

    useradd -m -g users -G wheel myusername
    passwd myusername
    visudo   # enable wheel group


## 9. Install Grub

For UEFI systems:

    mkdir /boot/efi
    mount /dev/sda1 /boot/efi
    grub-install --target=x86_64-efi --bootloader-id=grub --recheck
    grub-mkconfig -o /boot/grub/grub.cfg

## 10. Hostname and Host

Set hostname and hosts:

    echo "mySystemName" > /etc/hostname
    echo -e "127.0.0.1\tlocalhost\n::1\tlocalhost\n127.0.1.1\tmySystemName.localdomain\tmySystemName" > /etc/hosts

## 11. Enable Network

Enable NetworkManager:

    systemctl enable NetworkManager

## 12. Reboot

Reboot your system:

    reboot

## 13. After Installation

After reboot, connect to WiFi:

    nmcli device wifi connect SSID password "password"

## 14. Additional Software Installation

Install additional software packages using yay:

    git clone https://aur.archlinux.org/yay.git
    cd yay
    makepkg -si
    yay -S brave optimus-manager optimus-manager-qt code zsh vim vi unzip zsh-you-should-use zsh-syntax-highlighting wget pamixer libreoffice-still youtube-dl opusfile opus-tools libopusenc opus cmus openssh

## 15. Vim Plug

Install Vim Plug for neovim:

    sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'

## 16. Install FiraCode

Download and install FiraCode:

    mkdir /usr/share/fonts/firacode
    # Copy FiraCode.zip to this directory
    fc-cache -vf

## 17. Additional Configurations

Configure autologin for tty1:

    sudo systemctl edit getty@tty1.service
    # Paste the following:
    #[Service]
    #ExecStart=
    #ExecStart=-/usr/bin/agetty --autologin username --noclear %I $TERM
    #Type=idle

## 18. Grub Configuration

Modify Grub timeout:

    vi /etc/default/grub
    GRUB_TIMEOUT=0
    sudo grub-mkconfig -o /boot/grub/grub.cfg

## 19. Timezone Configuration

Set timezone:

    sudo timedatectl set-timezone Asia/Kolkata

## 20. Theme Installation

Install theme:

    cd /usr/share/themes
    # Copy Material-Black-/usr/share/themes to this directory
    lxappearance

## 21. Additional Software

Install rclone:

    yay -S rclone
    rclone sync your_folder cloud:your_folder

Congratulations! You've successfully installed Arch Linux with dwm and configured your system. Enjoy your customized and efficient Linux setup!

