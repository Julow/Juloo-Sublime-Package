# Juloo-Sublime-Package

All my sublime plugins.

\- [42 Header](#42-header) - [Shell Insert](#shell-insert) - [Focus](#focus) - [Cursor](#cursor) - [Jump](#jump) - [Side bar](#side-bar) - [Include Sort](#include-sort) - [Color Highlight](#color-highlight) - [C++](#cpp) - [Layout Spliter](#layout-spliter) - [Snippets](#snippets) - [Color Schemes](#color-schemes) - [ASM syntax](#asm-syntax) - [Status bar](#status-bar) - [Misc](#misc) -

## Installation

`git clone` this repo in `%Sublime text location%/Packages/Juloo-Sublime-Package`<br />
or download it manually.

If you want to update the package, use `git pull origin master`.

## Content

### 42 Header

Insert and update the **42 header**.

Commands:
* `Insert the 42 Header` insert the header at the top of the file
* `Update the 42 Header` update the header _(automatic by default)_

Support all languages.

If you want to disable 42 Header on save (enabled by default)<br />
Add this line into your `Settings - User`:

```js
	// Disable 42 Header on save
	"juloo_42_header": false
```

The plugin use the environ variable to find your pseudo ($USER).<br />
If you want to use an other name<br />
Add this line into your `Settings - User`:

```js
	"pseudo": "your name"
```

### Shell Insert

Add `Insert Shell command output` command

The command is executed using `bash`

Before executing the command, the pwd is set to the current dir
and some variables are set:

```shell
	"$FILE" # The current file name
	"$LINE" # The current line number
	"$COLUMN" # The current column number
	"$TEXT" # The content of the selected region (or the whole line if the selection is empty)
```

Warning: If there is multiple selections, the command is executed for each cursors

Also add:
* `Insert Line number` Insert the line number
* `Insert Column number` Insert the column index

### Focus

Add `8` keys binding:
- **Switch** next/previous **group**
- **Switch** next/previous **view** in current group
- **Move** current **view** to the right/left
- **Move** current **view** to the next/previous group

> On Linux:
> - `ctrl+pageup/pagedown` Switch next/prev view in group
> - `ctrl+shift+pageup/pagedown` Switch next/prev group
> - `ctrl+alt+pageup/pagedown` Move view to the right/left
> - `ctrl+alt+shift+pageup/pagedown` Move view to the next/prev group

### Cursor

Allow to save and restore selections

* `ctrl+k`, `ctrl+s` Save current selections
* `ctrl+k`, `ctrl+r` Restore saved selections
* `ctrl+k`, `ctrl+backspace` Remove saved selections

### Jump

* `alt+up` Jump 6 lines up
* `alt+down` Jump 6 lines down
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

Add `Sort Includes` command.

### Color Highlight

Highlight colors in code. _(only when the cursor is over)_

![ColorHighlight](/images/color_highlight.png)

Contains somes commands to convert colors.

![ColorCommands](/images/color_commands.png)

Support many colors syntaxes: rgb/rgba/argb/hsl/hsla functions, CSS hex, int 24 or 32 bits (hexa) and array of float (java/js/C++/python/...).

Color Highlight is disabled by default

```js
	// Enable Color Highlight
	"juloo_color_enabled": true
```

### Layout Spliter

Change easily the Sublime Text layout

![LayoutSpliter](/images/layout_spliter.gif)

Shortcuts:

* `ctrl+k, ctrl+d` Split vertical
* `ctrl+k, ctrl+shift+d` Split horizontal
* `ctrl+k, ctrl+m` Merge

Commands:

![LayoutCommands](/images/layout_commands.png)

* `Split vertical` (Split the current view vertically into 2 equal parts)
* `Split horizontal` (Split the current view horizontally into 2 equal parts)
* `Merge` (Merge 2 splitted views into 1)
* `Reset` (Reset the layout: 1 view)

### Cpp

Commands:
* `.hpp` Create a Coplien form class header
* `.cpp` Create a Coplien form class

### Snippets

Contains **10** snippets:

* `main` C main function
* `func` C function
* `while` While loop
* `static` C static var/function
* `t_` C typedef
* `s_` C struct (with typedef)
* `e_` C enum (with typedef)
* `#h` H file protection
* `/*` Comment (Norme)
* `** =` Comment separator (full line of '=')
* `*/` Extend the comment
* `printf` Printf and fflush

Write a snippet trigger and press **tab**. Press **tab** again to switch field.

### Color Schemes

Contains **3** color schemes:

* `Juloo2` A _dark_ color scheme
* `Juloo3` A _light_ color scheme
* `Juloo4` A _black_ color scheme

You can switch color schemes using the `Preferences / Color Scheme` menu.

### ASM Syntax

Contains syntax highlight for **ASM** language.

### Status bar

When the cursor is on a color, the status bar say it:

![StatusColors](/images/status_colors.png)

Also when you accidentally change the font size, the status bar say it: _(for 3 secs)_

![StatusFont](/images/status_font.png)

### Misc

#### C Header protection

Command:
* `.h` Insert header protection

#### Open in browser

Contains a command that open the current file in a browser.

If the file isn't _HTML_, the OS chooses which program opens that file.

![Openbro](/images/misc_openbro.png)

#### Config

Contains somes configurations to improve Sublime Text.

`configs/Preferences.sublime-settings` constains a default configuration.

#### Scope

The current _scope_ can be show in the status bar. _(disabled by default)_

![ShowScope](/images/status_scope.png)

Add this line into your configuration file to enable it:

```js
	// Enable Scope
	"juloo_show_scope": true
```

The _scope_ is used to build color schemes.
