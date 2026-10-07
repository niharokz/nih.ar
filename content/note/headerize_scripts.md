---
title : "Headerize Your Bash Scripts"
subtitle : "A small Bash tool that adds and updates a standard header in my shell scripts, so every script says what it does and when it changed."
tags: [note,home]
date : 2025-04-06
---
            
If you've ever stumbled across my code — especially the shell scripts — you'll notice something consistent: they all start with a **bold ASCII header**.

It’s not just for aesthetics (though it *does* look cool 😎). It helps me track:

* **When** the script was created  
* **Who** wrote it (me 👋)  
* And **when** it was last modified  

Manually updating that info? Nah. Too tedious.

So I built a lightweight CLI tool called `headerize` that **automatically adds or updates headers** in my `.sh` or `.py` files.

Let me walk you through how I did it — and how you can too.

## ⚡️ Why Automate Headers?

If you write a lot of scripts, a standardized header saves time and avoids confusion. Here’s what my headers look like:

    #!/bin/bash

    #
    #       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
    #       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
    #       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
    #       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
    #       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
    #       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
    #       DRAFTED BY [https://nih.ar] ON 10-04-2021.
    #       SOURCE [myscript.sh] LAST MODIFIED ON 06-04-2025.
    #

Now, imagine doing that manually every time, and updating the date whenever you tweak something.
This tool does it all — and even smartly preserves the original "drafted" date.

## 🧪 Meet headerize

This is a Bash script that:

* Adds a full header if one doesn't exist
* Updates the "last modified" date if a header is already present
* Works with .sh, .py, and any other files you want to include

Let’s set it up.

## Step 1: Create the headerize Script

📁 Location:
I like to keep my CLI tools in ~/bin, but you can place it wherever you like.

    mkdir -p ~/bin
    touch ~/bin/headerize
    chmod +x ~/bin/headerize


Main Script: 

    #!/bin/bash

    website="https://nih.ar"
    today=$(date +"%d-%m-%Y")
    file="$1"

    if [[ "${file##*.}" == "py" ]]; then
        cbang="#!/usr/bin/env python3"
    else
        cbang="#!/bin/bash"
    fi

    heading() {
        cat <<EOF > "$file"
    $cbang

    #
    #       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
    #       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
    #       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
    #       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
    #       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
    #       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
    #       DRAFTED BY [$website] ON $today.
    #       SOURCE [$file] LAST MODIFIED ON $today.
    #
    EOF
    }

    if [ -s "$file" ]; then
        line10=$(sed -n 10p "$file")

        if [[ "${line10:20:14}" != "$website" ]]; then
            # No header — prepend new header
            tmp="$(mktemp)"
            heading
            cat "$file" >> "$tmp"
            mv "$tmp" "$file"
        else
            # Header exists — just update the last modified line
            modline="#       SOURCE [$file] LAST MODIFIED ON $today."
            sed -i "11s|.*|$modline|" "$file"
        fi
    else
        heading
    fi

    echo "" >> "$file"

## Step 2: Add It to Your PATH

If ~/bin isn’t in your path yet, add this to your .bashrc or .zshrc:

    export PATH="$HOME/bin:$PATH"

Then reload your shell:

    source ~/.bashrc   # or ~/.zshrc

Now you can run it from anywhere:

    headerize myscript.sh

### Bonus: Add an Alias

    alias h='headerize'

Then just:

    h script.sh

## Real World Usage

Whenever I start a new script or edit an existing one, I just run:

    headerize filename.sh

If it's a new file → it adds a full header.
If it's an old file → it updates the "Last Modified" line only.
Creation date stays untouched. Clean and reliable.

###  That's It

I like building tools that do one job well.
This little script has saved me countless tiny moments — and made my codebase feel more personal and professional.

Feel free to fork it, tweak it, or drop me a line if you improve it.
