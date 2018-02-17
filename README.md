# HTTPi

Raspberry Pi (and more) GUI automation via HTTP-delivered commands.

- Add command modules via Python plugins
- Whitelist client-list
- Logging of access, to stdout and access.log
- HTML-pages for easy control via browser

**This software is a hobby project and in a development stage.
It comes with no warranties.**

## Known issues

- Window-handling functions not working on Linux. This affects
    - MV window-related commands
    - VLC playback controls (starting videos still works)

## Standard plugins

### VLC

- VLC: Common player operations - also includes list of video files from several folders

### MV

- MV: Move the mouse pointer, click, focus/min&maximise windows

### SH

- SH: Not-really-gui things like checking files and starting programs

## Adding plugins

Server dynamically picks up and handles requests towards plugins marked as "active".

1. Create &lt;name>.py in **plugins/** directory, with a **handle(str)** function
2. Add &lt;name> to **active** in **settings.properties**
3. Add &lt;name> to **from plugins import ...** in **server.py**
4. (Optional) Add &lt;name>.html to **start_pages/** directory and a link to it in index.html
