# pish

Raspberry Pi GUI automation via HTTP-delivered commands.

- Add command modules via Python plugins
- Whitelist client-list
- Access logging to stdout and access.log
- HTML-pages for browser control

## Standard plugins list

- VLC: Collection of common VLC media player operations

### Adding plugins

Server dynamically picks up and handles requests towards plugins marked as "active".

1. Create &lt;name>.py in **plugins/** directory, with a **handle(str)** function
2. Add &lt;name> to **active** in **settings.properties**
3. Add &lt;name> to **from plugins import ...** in **server.py**
4. (Optional) Add &lt;name>.html to **start_pages/** directory and a link to it in index.html
