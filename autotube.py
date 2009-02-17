#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, urllib, os
from xml.dom import minidom

# set your download location
video_dir = os.environ["HOME"]+"/music/videos"

print "AutoTube 0.5.2 \n"
os.chdir(video_dir)

def get_code(url):
    try:
        remoteSocket = urllib.urlopen(url)
        code = remoteSocket.read()
        remoteSocket.close()
        return code
    except IOError:
        return "Couldn't download " + url
    
def search_and_download(searchTerms):
    if os.path.exists(searchTerms + ".flv"):
        return "You already have " + searchTerms + ".flv"
    print "searching for " + searchTerms
    searchFile = open("tmpyoutube", "w")
    print "Connecting to YouTube..."
    searchFile.write(get_code("http://gdata.youtube.com/feeds/api/videos?vq=" + urllib.quote(searchTerms)))
    searchFile.close()
    print "Parsing..."
    searchDOM = minidom.parse("tmpyoutube")
    os.remove("tmpyoutube")
    try:
        videoID = searchDOM.getElementsByTagName('entry')[0].getElementsByTagName('id')[0].firstChild.data.split('/')[-1]
        youtubedl = os.system("/usr/bin/youtube-dl 'http://www.youtube.com/watch?v=" + videoID + "'")
        os.rename(videoID+".flv", searchTerms+".flv")
        return "Downloaded " + searchTerms + ".flv"
    except:
        return "Search for "+ searchTerms + " found nothing..."

if sys.argv[1] == 'search':
    searchTerms = sys.argv[2]
    search_and_download(searchTerms)
    
if sys.argv[1] == 'lastfm-recent':
    recentFile = open("tmplastfm", "w")
    print "Connecting to last.fm..."
    recentFile.write(get_code('http://ws.audioscrobbler.com/2.0/user/'+os.getlogin()+'/recenttracks.rss'))
    recentFile.close()
    lastDOM = minidom.parse("tmplastfm")
    os.remove("tmplastfm")
    songs = []
    for title in lastDOM.getElementsByTagName('item'):
        songs.append(title.getElementsByTagName('title')[0].firstChild.data.replace(u'\u2013 ', ''))
    print 'Your recent songs are:'
    for song in songs:
        print "- " + song.replace(u'\u2013', '-')
    print
    print "Now starting to download..."
    for song in songs:
        print search_and_download(song.replace(u'\u2013 ', ''))
    print "Done downloading your recent lastfm songs."
    

if sys.argv[1] == 'lastfm-top':
    topFile = open("tmplastfm", "w")
    print "Connecting to last.fm..."
    topFile.write(get_code('http://ws.audioscrobbler.com/1.0/user/'+os.getlogin()+'/toptracks.txt'))
    topFile.close()
    topFile = open("tmplastfm")
    songs = []
    for line in topFile:
        songs.append(line.split(',')[-1][:-1])
    topFile.close()
    os.remove("tmplastfm")
    print 'Your top songs are:'
    for song in songs:
        print "- " + song
    print
    print "Now starting to download..."
    for song in songs:
        print search_and_download(song.replace('– ', ''))
    print "Done downloading your top lastfm songs."

