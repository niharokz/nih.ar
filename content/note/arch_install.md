---
title : "Arch Installation Guide Minimalist Way"
subtitle : "Arch Installation process is the gap between newbie and pro. Any Linux installation without any installer is good way to understand basic linux architecture."
showInHome : True
date : 2023-09-16
---
            

This note is a guide to install arch Linux flavoured with dwm.

## Connect to internet

iwctl   :   For wifi connection.

    station device get-networks

    iwctl --passphrase passphrase station device connect SSID


##  Clear/Format disk

    fdisk /dev/sda
    g create new gpt label
    p print the partition table
    n create a new partition
    d delete a partition
    q quit without saving changes
    w write the new partition table and exit

## Format disk type

    mkfs.fat -F32   /dev/sda1
    mkfs.ext4   /dev/sda2

## Mounting and file Structure

    mount /dev/sda2 /mnt
    mkdir -p /mnt/{home,data,etc}
    mount /dev/sdb1 /mnt/data

## Basic setup 

    genfstab -U -p /mnt >> /mnt/etc/fstab

    pacstrap -i /mnt base

    arch-chroot /mnt

## Install some software
I use linux-lts instead of linux. If you prefer linux, then replace linux-lts with linux.

    pacman -S linux-lts linux-lts-headers base-devel linux-firmware vim networkmanager wpa_supplicant wireless_tools netctl dialog nvidia-lts nvidia-utils grub efibootmgr os-prober mtools dosfstools intel-ucode xorg-server xorg neofetch pulseaudio pamixer termite dolphin git vlc vifm i3

## System Settings
Setup time 
    
    ln -sf /usr/share/zoneinfo/Asia/Kolkata > /etc/localtime
    hwclock --systohc

Setup language
    
    vim /etc/locale.gen
    locale-gen
    vim /etc/locale.conf
    LANG=en_US.UTF-8

Initiate linux
    mkinitcpio -p linux-lts

## User addition

    useradd -m -g users -G wheel myusername
    passwd
    passwd myusername

Enable users as admin

    visudo
    enable wheels

## Install Grub

    GRUB UEFI
    mkdir /boot/efi
    mount /dev/sda1 /boot/efi
    grub-install --target=x86_64-efi --bootloader-id=grub --recheck
    ls -lart /boot/grub/locale/en*mo
    cp /usr/share/locale/en@quot/LC_MESSAGES/grub.mo /boot/grub/locale/en.mo

    grub-mkconfig -o /boot/grub/grub.cfg

## Optional Swap file

    swapfile

    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    echo "/swapfile none swap sw 0 0' | tee -a /etc/fstab

## Hostname and host 

    vim /etc/hostname
    mySystemName

    vim /etc/hosts
    127.0.0.1   localhost
    ::1     localhost
    127.0.1.1   mySystemName.localdomain    mySystemName

## Enable network

    systemctl enable NetworkManager

## Reboot

## After installation

    nmcli device wifi list
    nmcli device wifi connect SSID password "password"

    vim /etc/pacman.d/conf
    enable multilib
    ILoveCandy

    git clone https://aur.archlinux.org/yay.git
    yay git
    makepkg -si
    Install additional software

    yay -S brave optimus-manager optimus-manager-qt code zsh vim vi unzip zsh-you-should-use zsh-syntax-highlighting wget pamixer libreoffice-still youtube-dl opusfile opus-tools libopusenc opus cmus openssh
    Vim Plug

    sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
    nvim .config/nvim/init.vim
    PlugInstall
    Install FiraCode

Download Firacode.zip from google
mkdir /usr/share/fonts/firacode

    sudo systemctl edit getty@tty1.service
    Paste below
    [Service]
    ExecStart=
    ExecStart=-/usr/bin/agetty --autologin username --noclear %I $TERM
    Type=idle
    Grub config

    vi /etc/default/grub
    GRUB_TIMEOUT=0
    sudo grub-mkconfig -o /boot/grub/grub.cfg
    sudo timedatectl set-timezone Asia/Kolkata

    /usr/share/themes -> Material-Black-/usr/share/themes lxappearance

    rclone
    rclone sync your_folder cloud:your_folder 
