#!/usr/bin/python
# -*- coding: latin-1 -*-
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive
import datetime


def authenticate():
    gauth = GoogleAuth()
    scope = ['https://www.googleapis.com/auth/drive']
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('pydrive-acct.json', scope)
    # gauth.LoadClientConfigFile('../files/client_secrets.json')
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    return GoogleDrive(gauth)


def getFolderId(drive, parent, folderName):
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
    for f in file_list:
        if f['mimeType'] == 'application/vnd.google-apps.folder' and f['title'] == folderName:  # if folder
            return f['id']
    return None


def createFolder(drive, parent, folderName):
    folder_metadata = {"parents": [{"kind": "drive#fileLink", "id": parent}], 'title': folderName, 'mimeType': 'application/vnd.google-apps.folder'}
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    print('created folder ' + str(folder['id']))
    return folder['id']



