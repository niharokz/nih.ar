---
title : "An Automated Server Setup Script"
subtitle : "Installation of basic server tools in new server: zsh neovim exa zsh-syntax-highlighting zsh-autosuggestions python3-venv python3-pip neofetch git nginx certbot python3-certbot-nginx "
tags: [note,home]
date : 2024-01-26
---

Are you tired of spending hours configuring a new server every time you spin one up? Do you wish there was a quicker, more efficient way to get your server up and running with all the necessary software and configurations? Look no further! In this post, we'll walk you through the creation and utilization of an automated server setup script that will save you time and effort.

Setting up a new server can be a tedious and time-consuming task, involving multiple steps such as updating software, installing packages, configuring users, and more. To streamline this process, we've created a bash script that automates these tasks, allowing you to set up a new server quickly and effortlessly.

    echo "Automated Server Setup Script"

    echo "Enter new hostname for the server:"
    read host_name

    echo "Enter new username for user creation"
    read user_name

    echo "Server update started"
    sleep 2

    echo "sudo apt-get update -y"
    sudo apt-get update -y
    echo "update date"
    echo "sudo apt-get upgrade -y"
    sleep 5

    sudo apt-get dist-upgrade -y
    sudo "upgrade done"
    echo "sudo apt-get dist-upgrade -y"
    sleep 5

    sudo apt-get dist-upgrade -y
    echo "dist upgrade done"
    echo "installing software"
    sleep 5

    sudo apt-get install zsh neovim exa zsh-syntax-highlighting zsh-autosuggestions python3-venv python3-pip neofetch git nginx certbot python3-certbot-nginx -y
    echo "software installed"
    echo "creating directories and moving files"
    sleep 5

    sudo mkdir -p ~/.config/{nvim,zsh,.local/share,.cache}
    sudo mv init.vim ~/.config/nvim/
    sudo mv .zshrc ~/.config/zsh/
    sudo mv .zprofile ~/
    echo "Directories created and file moved"
    echo "Changing shell to zsh"
    sleep 5

    sudo chsh -s /bin/zsh
    sudo source .zprofile
    echo "Shell changed"
    echo "adding user $user_name"
    sleep 5

    sudo useradd -m -s /bin/zsh $user_name && sudo passwd
    sudo usermod -aG sudo $user_name
    sudo cp -r .ssh/ .zprofile .config /home/$user_name/
    cd /home/$user_name
    sudo chown -R $user_name:$user_name .config .zprofile .zshrc .ssh
    echo "$user_name user created"
    echo "setup finished"
    echo "changing hostname"
    sudo hostnamectl set-hostname $host_name
    echo "Please update sshd"
    sleep 5

    sudo nvim /etc/ssh/sshd_config
    echo "Finished sshd configuration"
    echo "restarting nginx sshd"
    sleep 5

    sudo systemctl restart sshd
    sudo systemctl enable nginx
    sudo systemctl start nginx
    echo "restarted all service"
    sleep 5

    sudo zsh

Source Code: [gitlab](https://gitlab.com/niharokz/narch/-/blob/master/server_setup/server_setup.sh)

## How to Use the Script

To use the script, follow these simple steps:

1. Copy the script into a new file on your server, for example, setup.sh.
2. Make the script executable by running chmod +x setup.sh.
3. Run the script with ./setup.sh.
4. Follow the prompts to enter the new hostname and username for user creation.
5. Sit back and relax while the script automates the server setup process.

## Conclusion

With the automated server setup script, you can significantly reduce the time and effort required to set up a new server. By automating tasks such as software installation, user creation, and configuration, you can focus on more important aspects of your project without worrying about tedious setup processes. Give it a try and see how much time and effort you can save!

"Feel free to customize this script further according to your specific needs, such as adding additional software packages or configuring different settings. Happy automating!"
