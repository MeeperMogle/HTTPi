# HTTPi

Raspberry Pi (and more) GUI automation via HTTP-delivered commands.

- Add command modules via Python plugins
- Whitelist client-list
- Logging of access, to stdout and access.log
- HTML-pages for easy control via browser

**This software is a hobby project and in a development stage.
It comes with no warranties.**

## Known issues

- 

## Standard plugins
### OMX

- Video player

### MV

- Move the cursor, click, focus/min&maximise windows

### SH

- Not-really-gui things like checking files and starting programs

### VLC (under test)

- Common player operations


## Adding plugins

Server dynamically picks up and handles requests towards plugins marked as "active".

1. Create &lt;name>.py in **plugins/** directory, with a **handle(str)** function
2. Add &lt;name> to **active** in **settings.properties**
3. (Optional) Add &lt;name>.html to **start_pages/** directory and a link to it in index.html
