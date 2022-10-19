---
title : "Clean home via XDG Base Directory"
subtitle : "Using XDG Base Directory specification, declutter the home directory"
showInHome : True
date : 2021-05-07
---
        
The home path is where most of our command-line life begins. When you are a heavy command-line user, the home path is where most of the terminal defaults to. The home path generally consists of desktop apps, downloads, photos, videos, document directories, and other dot files. With time the home path becomes a mess if you play around with your desktop. As the number of dot files and directories increases, it becomes difficult to use the autocomplete features of different shells. Aesthetically, it also looks cluttery. 

Cleaning this clutter is again a manual task, which you have to perform every now or then. Cleaning this clutter is a cure to the messy problem. But what if we prevent it. That's what I will write about in the below guidelines.

One such way is to use XDG Base Directory specification as written by [freedesktop](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html). These specifications are to specify files, file formats, and config paths.

Below is just an overview of how I keep my home clean with XDG Base Directory Specifications. 

## Basic directory structure
Initialize the main environmental variables:

        export XDG_CONFIG_HOME="$HOME/.config"
        export XDG_CACHE_HOME="$HOME/.cache"
        export XDG_DATA_HOME="$HOME/.local/share"

These variables will configure where config, cache, and data are stored. 
Define these in your RC files (bashrc/zshrc/other shells RC). Or you can also define these as global environmental variables.

## Reconfigure the paths
All paths set in these environment variables must be absolute.  Reconfigure the configs inside the ".config" directory.
i.e. use /.config/zsh/zshrc instead of .zshrc at home path.

## Define application-level xdg configs
Some of the application's xdg specs I use regularly :

        export CARGO_HOME="$XDG_DATA_HOME/cargo"
        export XMONAD_CONFIG_HOME="$XDG_CONFIG_HOME/xmonad"
        export XMONAD_DATA_HOME="$XDG_CONFIG_HOME/xmonad"
        export XMONAD_DATA_HOME="$XDG_CONFIG_HOME/xmonad"
        export XMONAD_CACHE_HOME="$XDG_CONFIG_HOME/xmonad"
        export RUSTUP_HOME="$XDG_DATA_HOME/rustup"
        export XAUTHORITY="$XDG_RUNTIME_DIR/Xauthority"
        export XINITRC="$XDG_CONFIG_HOME/X11/xinitrc"
        export XSERVERRC="$XDG_CONFIG_HOME/X11/xserverrc"
        export HISTFILE="$XDG_DATA_HOME/bash/history"
        export GNUPGHOME="$XDG_CONFIG_HOME/gnupg"

If you want to check if your application support XDG base specifications, please go through [this arch wiki article](https://wiki.archlinux.org/title/XDG_Base_Directory).

That's all. After doing all above, this is what my home looks like :

        [nihar@fybox ~]$ ls -a | wc -l
        12
