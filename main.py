#!/usr/bin/python

import os
import sys
import videos
import httplib2

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


CLIENT_SECRETS_FILE = "client_id.json"
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl" # Appended .force-ssl
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_READ_WRITE_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))

def list_captions(youtube, video_id):
    captions = youtube.captions().list(part="id,snippet", videoId=video_id).execute()
    return captions['items']

def download_captions(youtube, caption_id, fmt="srt"):
    """
    Downloads a caption. Possible values for fmt:
    sbv - SubViewer subtitle.
    scc - Scenarist Closed Caption format.
    srt - SubRip subtitle.
    ttml - Timed Text Markup Language caption.
    vtt - Web Video Text Tracks caption.
    """
    try:
        return youtube.captions().download(id=caption_id, tfmt=fmt).execute()
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

if __name__ == "__main__":
    argparser.add_argument("--videoid", default=videos.JUGGLE,
                           help="ID of video to like.")
    args = argparser.parse_args()

    youtube = get_authenticated_service(args)
    try:
        captions = list_captions(youtube, args.videoid)

        if not captions:
            print("This video has no captions")

        for caption in captions:
            captions = download_captions(youtube, caption['id'])
            if not captions:
                continue
            filename = "%s_%s.srt" % (args.videoid, caption['id'])
            with open(filename, 'w') as f:
                f.write(captions.decode('utf-8'))
            print("Downloaded %s caption with id %s to %s" %
                  (caption['snippet']['trackKind'], caption['id'], filename))

    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
