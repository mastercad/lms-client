#!/usr/bin/env python

from pylms import server

server = server.Server("localhost")
server.connect()

print("Connected Players: ")
print(server.get_players())

#player = server.get_player("d0:50:99:9e:1e:e3")
player = server.get_player("Windows10")

print("Player Name: "+player.get_name())
print("Player Rate: "+str(player.get_rate()))
print("Player Ref: "+player.get_ref())
print("Player UUID: "+player.get_uuid())

print(player.get_volume())

player.set_volume(60)

print(player.get_volume())

player.set_volume(50)

print(player.get_volume())

response = server.request("songinfo 0 100 track_id:94")
print(response)

response = server.request("trackstat getrating 1019")
print(response)

#player.next()
#player.prev()

#print("Track ID: "+player.get_track_id())
print("Track Title: "+player.get_track_title())
print("Track Current Title: "+player.get_track_current_title())
print("Track Artist: "+player.get_track_artist())
print("Track Genre: "+player.get_track_genre())
print("Track Path: "+player.get_track_path())

print("Tracks in current Playlist: "+str(player.playlist_get_info()))
print("Count of Tracks in current Playlist: "+str(player.playlist_track_count()))

print("Time Elapsed: "+str(player.get_time_elapsed()))

print("Track Duration: "+str(player.get_track_duration()))

print(player.update(1))
