---
title : "Self-Hosting your Gemini Capsule"
subtitle : "All about Gemini Protocol and Capsule."
showInHome : True
date : 2022-03-23
---


Gemini is a novel internet protocol distinct from HTTP and Gopher. It offers a cleaner experience and boasts a growing community of hackers.

## Why Opt for the Gemini Protocol?

Gemini capsules, or Gemini webpages, are lightweight, minimal, and demand minimal resources. They can seamlessly coexist with your existing websites, utilizing port 1965 by default while your web server operates on ports 80 or 443. Exploring this alternative protocol opens avenues for serving data and blogs differently. Accessing Gemini URLs (e.g., gemini://example.org) requires a Gemini client such as Amfora, Lagrange, or Elpher.


### 1. Creating a Gemini User

For security and cleanliness, it's advisable to establish a separate Gemini user:

    useradd -m -s /bin/bash gemini

Then, switch to the Gemini user:
    
    su -l gemini

To create and serve a Gemini capsule, follow these three basic steps:

1. Content: These are the webpages within your capsule.
2. TLS Certificate: Gemini necessitates an encrypted connection.
3. Gemini Server: This program makes your capsule available, akin to Nginx for HTTP.

As the Gemini user, organize three directories to streamline the process:

    mkdir -p ~/gemini/{content,certificate,server}

### 2. Content

This directory will house your capsule files. Gemini employs text/gemini markup (similar to Markdown). Create a gemini file within the content directory:

    nano gemini/content/index.gmi

Add your desired content to this Gemini capsule file:

    # This is a Sample Gemini page
    ## With header 1 and header 2
    And a short paragraph like this.
    => /index.gmi Link to the same page

### 3. TLS Certificate

Navigate to the certificate directory and generate a TLS certificate using OpenSSL:

    cd ~/gemini/certificate/
    openssl req -new -subj "/CN=example.org" -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -days 3650 -nodes -out cert.pem -keyout key.pem

### 4. Gemini Server

Download and prepare the server. We'll use the Agate server, a simple Gemini server written in Rust:

    cd ~/gemini/server
    wget https://github.com/mbrubeck/agate/releases/download/v3.1.0/agate.x86_64-unknown-linux-gnu.gz
    gunzip agate.x86_64-unknown-linux-gnu.gz
    mv agate.x86_64-unknown-linux-gnu agate-server
    chmod +x agate-server

### 5. Create a System Service

Switch back to root to create a systemd service:

    nano /etc/systemd/system/agate.service

Customize the highlighted text to your setup:

    [Unit]
    Description=agate
    After=network.target

    [Service]
    User=gemini
    Type=simple
    ExecStart=/home/gemini/gemini/server/agate-server --content /home/gemini/gemini/content --certs /home/gemini/gemini/certificate/ --hostname example.org --lang en-US

    [Install]
    WantedBy=default.target

Enable and start the Agate server:

    systemctl enable agate
    systemctl start agate

### 6. Firewall

If you're running a firewall, remember to open port 1965:

    ufw allow 1965

## Finalization

With everything set up, your server should be running. Access your Gemini capsule via any Gemini client with a URL like gemini://example.org.

For reference, check out a sample Gemini site: gemini://gemini.circumlunar.space.

Enjoy your first Gemini capsule!

For information about how to write in "gemtext" the markup language in Gemini, see this site: https://gemini.circumlunar.space/docs/gemtext.gmi. As you might guess, it also has an analogous gemini capsule here: gemini://gemini.circumlunar.space/docs/gemtext.gmi

My gemini capsule: [https://portal.mozz.us/gemini/nih.ar/](https://portal.mozz.us/gemini/nih.ar/) 
-------------------------------------------------

This ariticle is also available at [landchad](https://landchad.net/gemini/)
