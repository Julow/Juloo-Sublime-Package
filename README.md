# Juloo-Sublime-Package

All my sublime plugins.

## Installation

`git clone` this repo in `%Sublime text location%/Packages/Juloo-Sublime-Package`<br />
or download it manually.

If you want to update the package, use `git pull`.

## Content

### 42 Header

* `Insert the 42 Header` Insert the header at the top of the file
* `Update the 42 Header` Update the header

The header is automatically updated on save

```js
	// Disable header update on save
	"juloo_42_header": false
	// Set pseudo (by default, $USER is used)
	"pseudo": "your name"
```

### Run Command

* `ctrl+b` show a prompt that execute a command

Before the command is run, the pwd is set to the first opened folder

Save the last used command

### Shell Insert

* `Insert Line number` Insert the line number
* `Insert Column number` Insert the column index
* `Insert Shell command output`:

The command is executed using `bash`

Before executing the command, the pwd is set to the current dir
and some variables are set:

```shell
	"$FILE" # The current file name
	"$LINE" # The current line number
	"$COLUMN" # The current column number
	"$TEXT" # The content of the selected region (or the whole line if the selection is empty)
```

Note: If there is multiple selections, the command is executed for each cursors

### Focus

* `ctrl+pageup/pagedown` Switch next/prev view in group
* `ctrl+shift+pageup/pagedown` Switch next/prev group
* `ctrl+alt+pageup/pagedown` Move view to the right/left
* `ctrl+alt+shift+pageup/pagedown` Move view to the next/prev group

### Cursor

* `alt+s` Save current cursors
* `alt+shift+s` Restore saved cursors
* `alt+x` Remove saved cursors

* `alt+d` Jump to the next saved cursor
* `alt+shift+d` Jump to the previous saved cursor

* `alt+up` Jump before previous paragraph
* `alt+down` Jump after next paragraph
* `alt+shift+up` or `alt+shift+down` Same but selecting

### Side Bar

* `ctrl+,` Toggle and focus side bar + Reveal current file

### Include Sort

Sort C/C++ includes on save.

Can be disabled:
```js
	// Disable automatic include sorting
	"juloo_sort_include": false
```

* `Sort Includes` command

### Layout Spliter

Change easily the Sublime Text layout

Shortcuts:

* `ctrl+k, ctrl+d` Split vertical
* `ctrl+k, ctrl+shift+d` Split horizontal
* `ctrl+k, ctrl+m` Merge

Commands:

* `Split vertical` (Split the current view vertically into 2 equal parts)
* `Split horizontal` (Split the current view horizontally into 2 equal parts)
* `Merge` (Merge 2 splitted views into 1)
* `Reset` (Reset the layout: 1 view)

### Misc

Color schemes:

* `Juloo2`
* `Juloo4`

Syntax:

* `ASM syntax`

Snippets:

* `main` C main function
* `/*` Comment
* `** =` Comment separator (full line of '=')
* `*/` Extend the comment
* `# =` Comment separator
* `std::cout` std::cout <<  << std::endl;

Commands:

* `.hpp` Create a Coplien form class header
* `.cpp` Create a Coplien form class
* `.h` Insert `#ifndef` header protection
