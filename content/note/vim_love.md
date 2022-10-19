---
title: Why I Really Really Really Love VIM!
subtitle: VIM or NeoVIM! Simple yet powerful text editor that can become an obsession in no time. This note is a reference for the most common commands.
showInHome : True
date: 2018-12-18
---

I have been using vi editor for the last half-decade. But it was when I feel lazy to copy files from the servers to local and edit them. I was aware of vim but never bothered to use it.    

A couple of months back, I decided to try out vim more often. Today, my default text editor is neovim. Sometimes, when I try to use sublime text or other plain text editors, my finger will behave like hjkl escape.    

Nowadays, most of the time I spent now is on the terminal. This note contains a quick cheat sheet for the things I pick up now and then.     

## Basic commands in VIM

Modes of vim:

	normal mode - escape key will bring you to normal mode.
	insert mode - i, a, s, o, or similar to get into insert mode.
	visual mode - v visual, shift+v visual-line, cntr+v visual block.
	command mode - : or / will show command at bottom of the vim screen.
	replace mode - r, R its just an extension of insert mode.

Navigation in vim:

	h - left shift
	j - bottom shift
	k - up shift
	l - right shift

	gg - go to the top
	5g - go to 5th line
	:5 - go to the 5th line
	G - go to the bottom
	
	w - left word shift, cursor at the beginning
	W - left word shift (including special characters)
	e - left word shift, cursor at the end
	E - left word shift (including special characters)
	b - right word shift, cursor at the beginning
	B - right word shift (including special characters)

	f - Shift before till next occurrence left
	F - Shift before till next occurrence right
	t - Shift one char before till next occurrence left
	T - Shift one char before till next occurrence right

	/ - Search and go
	? - Search reverse and go
	n - After search / ? to rotate
	N - After search / ? to reverse rotate
	
	0 - Go to the beginning of the line
	^ - Go to the beginning of line
	$ - Go to end of line
	
	[0-9] + any of the above commands will multiply the commands
	
Operation in vim:

	i - Insert at the current position
	I - Insert at beginning of line
	a - Append after current position
	A - Append after current postiion

	o - Insert in new line below
	O - Insert in new line above
	u - undo
	ctrl+r - redo

	x - Delete a character
	X - Delete line from
	dd - Delete whole line
	D - Delete one character backward
	cc - Delete line and insert on
	C - Delete line and insert on
	
	s - Replace and insert current
	S - Replace line and insert current
	r - Only replace one character
	R - Replace the whole line from position

Yank and Visual operation:
	
	y - Yank from the current position
	yy/Y - Yank current line
	v - visual selection current pos
	V - visual select line
	ctrl+v - Visual block

Commandline mode in vim:

	:set number - shows the number
	:q - quit
	:w - write
	:help - show all manual for command

Above commands were just basic vim commands. But the power of vim relies on how you combine it to get proper results. Below are few examples:

	dfi - Delete all till next occurrence of i
	dit - Delete everything inside tag
	dat - Delete everything including tag
	dis - Delete statement
	dib - Delete block
	yt} - Yank before }
	y/power - Yank from current to next occ of "power"
	2yas - Yank 2 statements.

If I add all possible combinations, this note will never end. At end of this note, there are few Q&A which will contain some more commands combination.   

## Registers, Macros, Bookmark, Buffers in VIM

### Bookmark
	
	ma - Bookmark will be created with the name a.
	`a - Move to bookmark 'a' location.
	'a - Move to start of bookmark.
	:marks - List all bookmarks
	:delmarks a - delete bookmark a

### Macros: Vim macros is a extremely powerful tool. Its based on 4 stages. 

* Start recording: q followed by any lowercase letter.
* Enter your vim actions
* Stop recording: Enter q
* Play recording: Enter @lowercase letter    

Example:

	qa - start recording macro named 'a'
	"a   INOTE : ^[j - vim action
	10@a - Macro run 10 times.
	:reg - check all macros

### Registers   

Named registers: We can use 26 named registers; we can use a-z or A-Z. By default vim doesn’t uses these registers.    

Numbered registers: We can use 0 to 9 named registers. Vim fills these registers with text from yank and delete command.    

	"aY - yank current line in register a
	"ap - Paste from register a
	" - Default registers used for yank/dd

### Buffers

	:buffers/:ls - List all buffers
	:badd <file> - Add file into new buffer
	:b2 - Switch to 2nd buffer. 
	:bn - Move to the next buffer in buffer list
	:bp - Move to the previous buffer in buffer list
	:bf - Move to the first buffer
	:ball - Load all buffers
	:bufdo set nu - line numbers enabled for all buf
	:bufdo %s/#/@/g | w - global substitute from # to g
	shift+w - To move from different windows
	:wall - write to all
	:bd - delete current buffer

### Tab and Windows

	:vs - vertical split
	:sp - horizontal split
	:vs file - open file in vertical split
	:tabnew - Add new tab
	:tabclose - tab close
	:tabnext - next tab
	:on - all other window will be closed
	ctrl+w + - increase window
