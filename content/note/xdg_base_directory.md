---
title : "Organizing XDG Base Directory"
subtitle : "Using XDG Base Directory specification, declutter the home directory"
tags: [note,home]
date : 2021-05-07
---
        

Ah, the humble home path – where our command-line adventures often kick off. If you're a die-hard terminal dweller like me, you know it's where the heart of your digital life resides. But let's face it, over time, that trusty ol' home path can start to resemble a virtual junk drawer, cluttered with desktop apps, downloads, dot files, and more.

Enter the XDG Base Directory specification, courtesy of freedesktop. This nifty set of guidelines offers a solution to our clutter conundrum. Here's a quick rundown of how I keep my digital abode squeaky clean using these specs:


## Basic directory structure

First things first, let's set up the main environmental variables:

        export XDG_CONFIG_HOME="$HOME/.config"
        export XDG_CACHE_HOME="$HOME/.cache"
        export XDG_DATA_HOME="$HOME/.local/share"

These variables dictate where our config, cache, and data are stored. Pop these babies into your RC files (think bashrc/zshrc/other shells RC), or go big and make them global environmental variables.

## Reconfigure the paths

Now, all paths set in these environment variables need to be absolute. Think of it as giving your configs a new address – instead of .zshrc chilling in your home path, it's now kicking back in /.config/zsh/zshrc.

## Define Application-Level XDG Configs

Here are a few XDG specs I swear by for some of my go-to applications:

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

## Wrapping Up

If you want to check if your application support XDG base specifications, please go through [this arch wiki article](https://wiki.archlinux.org/title/XDG_Base_Directory).

And voilà! With these tweaks in place, my home path is now as tidy as Marie Kondo's sock drawer. So, the next time you peek into your digital dwelling, may you be greeted by a sight as refreshing as a clean slate. 🏠✨

That's all. After doing all above, this is what my home looks like :

        [nihar@fybox ~]$ ls -a | wc -l
        12
