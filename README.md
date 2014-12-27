# Juloo-Sublime-Package

All my sublime plugins.

\- [Color Highlight](#color-highlight) - [Layout Spliter](#layout-spliter) - [Snippets](#snippets) - [Color Schemes](#color-schemes) - [Norme Checker](#norme-checker) - [Status bar](#status-bar) - [Misc](#misc) -

## Installation

`git clone` this repo in `%Sublime text location%/Packages/Juloo-Sublime-Package`<br />
or download it manually.

If you want to update the package, use `git pull origin master`.

## Content

### Color Highlight

Highlight colors in code. _(only when the cursor is over)_

![ColorHighlight](/images/color_highlight.png)

Contains somes commands to convert colors.

![ColorCommands](/images/color_commands.png)

Support many colors syntaxes: rgb/rgba/argb/hsl/hsla functions, CSS hex, int 24 or 32 bits (hexa) and array of float (java/js/C++/python/...).

### Layout Spliter

Change easily the Sublime Text layout

![LayoutSpliter](/images/layout_spliter.gif)

Split vertically or horizontally the layout with commands.

![LayoutCommands](/images/layout_commands.png)

Commands:

* `Split vertical` (Split the current view vertically into 2 equal parts)
* `Split horizontal` (Split the current view horizontally into 2 equal parts)
* `Merge` (Merge 2 splitted views into 1)
* `Reset` (Reset the layout: 1 view)

### Snippets

Contains **10** snippets:

* `main` C main function
* `func` C function
* `while` While loop
* `static` C static var/function
* `t_` C typedef
* `s_` C struct (with typedef)
* `#h` H file protection
* `/*` Comment (Norme)
* `*/` Extend the comment
* `printf` Printf and fflush

Write a snippet trigger and press **tab**. Press **tab** again to switch field.

### Color Schemes

Contains **2** color schemes:

* `Juloo2` A _dark_ color scheme
* `Juloo3` A _light_ color scheme

You can switch color schemes using the `Preferences / Color Scheme` menu.

### Norme Checker

Highlight norme errors.

Check and highlight norme errors after each saves only in `C` and `C++` files.<br />
_Errors are also print to the Sublime Text console._

Command:
* `Check the norme` Check the norme on any file

Checks:
* 5 functions per file
* 25 lines per function
* 4 params per function
* Multiple empty lines
* 80 chars per lines
* Invalid function name
* Bad include
* Function scope bad align
* Slash comment
* Trailing space
* Comma space
* Keyword space
* Operator space
* Comment formating
* 42 header

_More checks will be added in the future._

If you want to disable **Norme Checker** (enabled by default)<br />
Add this line into your `Settings - User`:

```js
	// Disable Norme Checker
	"juloo_norme_check": false
```

### Status bar

When the cursor is on a color, the status bar say it:

![StatusColors](/images/status_colors.png)

Also when you accidentally change the font size, the status bar say it: _(for 3 secs)_

![StatusFont](/images/status_font.png)

### Misc

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

## Old plugins

* [JulooColorHightlight](https://github.com/Julow/JulooColorHighlight)
* [JulooSnippets](https://github.com/Julow/Juloo-Snippets)
* [JulooColorSchemes](https://github.com/Julow/Juloo-Color-Schemes)
* [LayoutSpliter](https://github.com/Julow/LayoutSpliter)
