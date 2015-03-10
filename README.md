# Overview

This is a CLI utility for "deploying" Google Apps Script code. Normally Google Apps Scripts are updated using an in-browser editor. This tool allows you to use modern development tooling and then "deploy" code to the Google Apps Script file via the Google Drive API. It was originally developed to plug into a CI tool.

# Install

## Application

    $ pip install python-gas-cli

## Configure OAuth Client

1. Go to the [Google Developers Console](https://console.developers.google.com/) and create a new project.
2. Go to that project and then "APIs & auth > Credentials".
3. Under OAuth click the "Create new Client ID" button.
4. Under "Application Type" select "Installed application" and choose "Other" for "Installed Application Type". **NOTE:** Once created it will be labeled "Client ID for _native_ application".
5. Click the "Download JSON" button to fetch your "client secrets file". **IMPORTANT:** Save this file somewhere safe. It will be needed every time you call the `gas` application.

## Authorize `gas` Application

Run the following command. It should open a browser tab and push you through the OAuth flow.

    $ gas authorize -s /path/to/client_secrets.json -c /path/to/safe/place/for/credentials.json

**IMPORTANT:** Save the `credentials.json` file somewhere safe. It will also be needed, along with the client secrets file.

# Deploying

First grap the file ID of your Google Apps Script from the URL. 

![example](https://dl.dropboxusercontent.com/s/4hx5pkaywwvfk9j/2015-03-10%20at%202.53%20PM.png)

**TIP:** Create one Google Apps Script for each "environment" you'd like to "deploy" to. For instance have "My App Script - Production" and "My App Script - Staging". You can then use the unique file IDs to deploy to different "environments".

Once you have the file ID and a directory containing your "build", you can run the following command to "deploy" code to your Google Apps Script:

```
$ gas deploy -s /path/to/client_secrets.json -c /path/to/safe/place/for/credentials.json -b /path/to/build/ \
    -f 1Mm3KBmN0U_fXz3oLXiV38GvQhkBC0sdEsZhQ7hQoXDkROjM7KaokT4ts
Looking up existing GAS project (id=1Mm3KasdfU_fX12324iV38GxQxkxC0sdEsZhQ7hQoXDkROjM7KaokT4ts) files...
 - Found Preferences.html (id=3aedbb04-dbfd-463a-asdf-0fefh1fcaa43, type=html)
 - Found Code.gs (id=c166575f-11111-asdf-8451-220205c5cf8c, type=server_js)
2 files found.

Inspecting build /Users/jstump/dev/sprintly-spreadsheet/build/...
 - Replace Code.gs (id=1Mm3KasdfU_fX12324iV38GxQxkxC0sdEsZhQ7hQoXDkROjM7KaokT4ts) with Code.gs.
 - Replace Preferences.html (id=3aedbb04-dbfd-463a-asdf-0fefh1fcaa43) with Preferences.html.
Uploading 2 files... Done.
```
