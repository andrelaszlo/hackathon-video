Downloads the subtitles for a youtube video.

Usage example:

Make sure to generate a OAuth client id and save it to `client_id.json`. You can [generate them here](https://console.developers.google.com/apis/credentials).

```
$ ./main.py --videoid CDj9gkIe5iY
Downloaded standard caption with id nhCEVogYWHoJpWMoXYBmr7VKWqzq7LbF to CDj9gkIe5iY_nhCEVogYWHoJpWMoXYBmr7VKWqzq7LbF.srt
$ head CDj9gkIe5iY_nhCEVogYWHoJpWMoXYBmr7VKWqzq7LbF.srt
1
00:00:00,000 --> 00:00:02,280
[Intro music]

2
00:00:11,480 --> 00:00:13,700
Welcome to the Hydraulic Press Channel!

3
00:00:13,920 --> 00:00:19,020
```

There are two major problems though.

Number one, many (most?) videos don't have captions:

```
$ ./main.py --videoid t-V8m9xTYQE
This video has no captions
```

Number two, most captions are not accessible by default:

```
$ ./main.py --videoid 1BDF9AbLgUw
An HTTP error 403 occurred:
b'The permissions associated with the request are not sufficient to download the caption track. The request might not be properly authorized, or the video order might not have enabled third-party contributions for this caption.'
```


To download a subtitle from a video that you don't own, the video needs to allow community contributions. It's off by default:

> Community contributions
>
> [] Allow viewers to contribute translated titles, descriptions, and subtitles/CC 
