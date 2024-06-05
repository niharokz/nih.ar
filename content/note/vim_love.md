---
title: Why I Really Really Really Love VIM!
subtitle: VIM or NeoVIM! Simple yet powerful text editor that can become an obsession in no time. This note is a reference for the most common commands.
showInHome : True
date: 2018-12-18
---

For the past five years, vi editor has been a trusty companion, saving me from the hassle of copying files between servers and local machines. Despite being aware of Vim's existence, I never bothered to give it a try.

However, a couple of months ago, I decided to delve deeper into the world of Vim. Fast forward to today, and Neovim has become my default text editor. Interestingly, my muscle memory now instinctively reaches for hjkl keys even when using other text editors like Sublime Text.

With most of my time now spent in the terminal, I've compiled a handy cheat sheet of Vim commands that I've picked up along the way.

## Basic Commands in VIM

**Modes of Vim:**
- Normal mode: Pressing the escape key brings you to normal mode.
- Insert mode: Use i, a, s, o, or similar to enter insert mode.
- Visual mode: v for visual, shift+v for visual-line, cntr+v for visual block.
- Command mode: Type : or / to show commands at the bottom of the Vim screen.
- Replace mode: r for replacing a single character, R for replacing multiple characters.

**Navigation in Vim:**
- h: Move left
- j: Move down
- k: Move up
- l: Move right
- gg: Go to the top
- G: Go to the bottom
- w: Move to the beginning of the next word
- b: Move to the beginning of the previous word
- f: Find the next occurrence of a character
- /: Search forward
- ?: Search backward
- n: Repeat the last search in the same direction
- 0: Move to the beginning of the line
- ^: Move to the first non-blank character of the line
- $: Move to the end of the line

**Operations in Vim:**
- i: Insert at the current position
- a: Append after the current position
- o: Insert a new line below the current line
- O: Insert a new line above the current line
- u: Undo
- ctrl+r: Redo
- x: Delete a character
- dd: Delete the current line
- yy: Yank the current line
- p: Paste

## Registers, Macros, Bookmark, Buffers in VIM

**Bookmark:**
- ma: Set a bookmark named 'a'
- `a: Move to the location of bookmark 'a'
- :marks: List all bookmarks
- :delmarks a: Delete bookmark 'a'

**Macros:**
- qa: Start recording a macro named 'a'
- Enter your Vim actions
- q: Stop recording the macro
- @a: Play the recorded macro 'a'

**Registers:**
- "aY: Yank the current line in register 'a'
- "ap: Paste from register 'a'

**Buffers:**
- :ls: List all buffers
- :badd <file>: Add a file to a new buffer
- :b2: Switch to the second buffer
- :bn: Move to the next buffer
- :bp: Move to the previous buffer
- :bd: Delete the current buffer

**Tab and Windows:**
- :vs: Vertical split
- :sp: Horizontal split
- :vs file: Open a file in a vertical split
- :tabnew: Add a new tab
- :tabclose: Close the current tab
- :tabnext: Move to the next tab
- ctrl+w +: Increase window size

By combining these commands creatively, Vim's power truly shines. And while this list only scratches the surface of Vim's capabilities, it's a testament to the efficiency and versatility of this legendary text editor.