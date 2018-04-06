import sqlite3

conn = sqlite3.connect('musicaly_database.db')

print("         Welcome To Musicly")

class playlists:

    def viewPlaylists(self):                #needs sho3'l
        cursor = conn.execute("select name, count(song.song_key) from playlist, song, song_playlist \
                      where song.song_key = song_playlist.song_key\
                      and playlist.playlist_key = song_playlist.playlist_key")
        conn.commit()
        print("Playlists:")
        for row in cursor:
            print("playlist name: ", row[0])
            print("songs count: ", row[1])

    def viewAplaylist(self, playlistName):      #3ayzeen neb3at name
        playname = " "
        description = " "
        cursor = conn.execute("select playlist.name, playlist.description \
                      from song, playlist, song_playlist \
                      where song.song_key = song_playlist.song_key \
                      and playlist.playlist_key = song_playlist.playlist_key\
                      and playlist.name = ?", (playlistName,))
        conn.commit()
        for row in cursor:
            playname = row[0]
            description = row[1]
        print(playname, " \n ", description, "\n")

        cursor = conn.execute("select song.song_name, song.song_length \
                      from song, playlist, song_playlist \
                      where song.song_key = song_playlist.song_key \
                      and playlist.playlist_key = song_playlist.playlist_key\
                      and playlist.name = ?", (playlistName,))

        conn.commit()
        for row in cursor:
                print("-", row[0], "    Duration: ", row[1])

    def sortPlaylists(self, playlistName, sort):
        if sort == "artist":
            cursor = conn.execute("select artist.name As artist,song.song_name\
                      from playlist join song join song_playlist join artist\
                      where  song.song_key=song_playlist.song_key \
                      and song_playlist.playlist_key= playlist.playlist_key \
                      and artist.artist_key=song.artist_key and playlist.name = ?\
                      group by song.song_name\
                      order by artist.name", (playlistName,))

        elif sort == "genre":
            cursor = conn.execute("select song.genre,song.song_name\
                      from playlist join song join song_playlist\
                      where  song.song_key=song_playlist.song_key\
                      and song_playlist.playlist_key= playlist.playlist_key\
                      and playlist.name = ?\
                      group by song.song_name\
                      order by song.genre", (playlistName,))

        elif sort == "album":
            cursor = conn.execute("select album.album_name,song.song_name\
                        from playlist join song join song_playlist join album\
                        where song.song_key=song_playlist.song_key\
                        and song_playlist.playlist_key= playlist.playlist_key\
                        and album.album_key=song.album_key and playlist.name = ?\
                        group by song.song_name\
                        order by album.album_name", (playlistName,))

        elif sort == "release date":
            cursor = conn.execute("select song.release_date,song.song_name, playlist.name\
                        from playlist join song join song_playlist\
                        where  song.song_key=song_playlist.song_key\
                        and song_playlist.playlist_key= playlist.playlist_key\
                        and playlist.name = ?\
                        group by song.song_name\
                        order by song.release_date", (playlistName,))
        conn.commit()
        for row in cursor:
                print(row[0], row[1])

    def AddNewplaylist(self, playlistName, description):
        conn.execute("insert into playlist(description,name)values (?,?)", (description, playlistName))
        conn.commit()

    def addNewSongToPlaylist(self, playlistName, songName):
        cursor = conn.execute('''insert into song_playlist values
                             ((select song.song_key from song where song_name = ?),
                             (select playlist.playlist_key from playlist where name = ?))''', (songName, playlistName))
        conn.commit()
        if cursor.rowcount == 0:
            print("mafeesh insertion. \n")

        else:
            print("songs inserted.")

    def removeSong(self, playlistName, songName, size):
        for i in range(0, size):
            cursor = conn.execute("delete from song_playlist\
                         where song_playlist.song_key = (select song.song_key from song where song_name = ?)\
                          and song_playlist.playlist_key = (select playlist.playlist_key from playlist \
                          where playlist.name = ?)", (songName[i], playlistName))
        conn.commit()
        if cursor.rowcount == 0:
            print("something wrong happened. \n")
        else:
            print("deleted successfully! \n")

    def deletePlaylist(self, playlistName):
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.execute("delete from playlist where playlist.name = ?", (playlistName,))
        conn.commit()
        if cursor.rowcount == 0:
            print("error! \n")
        else:
            print("playlist deleted successfully! \n")

class song:

    def viewSong(self, songName):
        cursor = conn.execute('''select song.song_name, song.song_length, song.release_date, song.genre,
                      artist.name, album.album_name, band.band_name
                      from song left join artist on song.artist_key = artist.artist_key
                      left join band on band.band_key = song.band_key 
                      left join album on album.album_key = song.album_key
                      where song.song_name = ?''', (songName,))
        conn.commit()
        for row in cursor:
            print("name: ", row[0])
            print("duration: ", row[1])
            print("release date: ", row[2])
            print("genre: ", row[3])
            print("artist: ", row[4])
            print("album: ", row[5])
            print("band: ", row[6])

    def addNewSongByArtist(self, albumName, songName, duration, genre, releaseDate, artistName):
        cursor = conn.execute('''insert into song(song_name,song_length,album_key,artist_key,genre,release_date)
                                values(?,?,(select album_key from album where album_name=?),
                                (select artist_key from artist where name=?),?,?)'''
                              , (songName, duration, albumName, artistName, genre, releaseDate))
        conn.commit()

    def addNewSongByBand(self, albumName, songName, duration, genre, releaseDate, bandName):
        cursor = conn.execute('''insert into song(song_name,song_length,album_key,band_key,genre,release_date)
                                                 values(?,?,(select album_key from album where album_name=?),
                                                 (select band_key from band where band_name=?),?,?)'''
                              , (songName, duration, albumName, bandName, genre, releaseDate))
        conn.commit()

    def viewAllSongs(self):
        cursor = conn.execute("select song_name, song_length from song")
        conn.commit()
        for row in cursor:
            print("-", row[0], "\tDuration: ", row[1])

    def deleteSong(self, songName):
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.execute("delete from song where song_name = ?", (songName,))
        conn.commit()
        if cursor.rowcount == 0:
            print("something wrong happened! ")
        else:
            print("song deleted successfully! ")

class artist:

    def addNewArtist(self, artistName):
        cursor = conn.execute('''select count(artist_key)
                                    from artist
                                    where name=?''', (artistName,))
        for row in cursor:
            if row[0] == 0:
                conn.execute("insert into artist (name) values (?)", (artistName,))
           # else:
             #   print("Artist already exists.")
        conn.commit()

    def deleteArtist(self, artistName):
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.execute("delete from artist where name = ?", (artistName,))
        conn.commit()
        if cursor.rowcount == 0:
            print("something went wrong ")
        else:
            print("Artist deleted successfully! ")

    def viewArtists(self):
        cursor = conn.execute("select name from artist")
        conn.commit()
        for row in cursor:
            print(row[0])

class band:

    def addNewBand(self, bandName, membersCount):
        cursor = conn.execute('''select count(band_key)
                                    from band
                                    where band_name=?''', (bandName,))
        for row in cursor:
            if row[0] == 0:
                conn.execute("insert into band (band_name, members_count) values (?, ?)", (bandName, membersCount))
        conn.commit()

    def deleteBand(self, bandName):
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.execute("delete from band where band_name = ?", (bandName,))
        conn.commit()
        if cursor.rowcount == 0:
            print("something went wrong ")
        else:
            print("Band deleted successfully! ")

    def viewBands(self):
        cursor = conn.execute("select band_name, members_count from band")
        conn.commit()
        for row in cursor:
            print("band name:", row[0], "   number of members:", row[1])

class album:


    def viewAlbum(self, albumName):
        print(albumName)
        cursor = conn.execute('''select count(song.song_name)
               from album join song where
               album.album_key = song.album_key and album.album_name = ?''', (albumName,))
        conn.commit()
        for row in cursor:
            print("Songs count: ", row[0])

        cursor=conn.execute('''select song.song_name
        from album join song
        where album.album_key=song.album_key and album.album_name=?''', (albumName,))
        conn.commit()
        for row in cursor:
            print(row[0])

    def newAlbumByArtist(self, albumName, songName, duration, genre, releaseDate, artistName):
        a1 = artist()
        a1.addNewArtist(artistName)


        cursor = conn.execute('''insert into album (album_name,artist_key)values(?,
                        (select artist_key from artist where name=? ))''', (albumName,artistName))
        cursor = conn.execute('''insert into song(song_name,song_length,album_key,artist_key,genre,release_date)
                        values(?,?,(select album_key from album where album_name=?),
                        (select artist_key from artist where name=?),?,?)'''
                         , (songName, duration, albumName, artistName, genre, releaseDate))
        conn.commit()

    def newAlbumByBand(self, albumName, songName, duration, genre, releaseDate, bandName, members):
        b1 = band()
        b1.addNewBand(bandName,members)
        conn.execute('''insert into album (album_name, band_key)values(?,
                        (select band_key from band where band_name=?))''', (albumName,bandName))
        cursor = conn.execute('''insert into song(song_name,song_length,album_key,band_key,genre,release_date)
                                         values(?,?,(select album_key from album where album_name=?),
                                         (select band_key from band where band_name=?),?,?)'''
                                         , (songName, duration, albumName, bandName, genre, releaseDate))
        conn.commit()

    def deleteAlbum(self,albumName):#by delete el songs m3 el album kman
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.execute('''delete from album where album_name=? ''', (albumName,))
        conn.commit()
        if cursor.rowcount == 0:
            print("something went wrong ")
        else:
            print("Album deleted successfully! ")

class homepage:

    def plists(self):
        home = homepage()
        p = playlists()
        p.viewPlaylists()
        print("\n1.View playlist  2.Add playlist  3.Delete playlist")
        choice = input("4.Add a new song to a playlist    5.view songs in a playlist by    6.Back to home:\n")
        while choice != '6':
            if choice == '1':
                play = input("Enter the name of the playlist: ")
                p.viewAplaylist(play)
            elif choice == '2':
                play = input("Enter the name of the playlist: ")
                des = input("Enter the description of the new playlist: ")
                p.AddNewplaylist(play, des)
            elif choice == '3':
                play = input("Enter the name of the playlist: ")
                p.deletePlaylist(play)
            elif choice == '4':
                play = input("Enter the name of the playlist: ")
                num = int(input("enter the number of songs you want to add: "))
                while num != 0:
                    songs = input("enter a song: ")
                    p.addNewSongToPlaylist(play, songs)
                    num = num - 1
            elif choice == '5':
                play = input("Enter the name of the playlist: ")
                sort = input("1.artist    2.genre    3.album     4.release date:\n")
                p.sortPlaylists(play, sort)
            print("\n1.View playlist  2.Add playlist  3.Delete playlist")
            choice = input("4.Add a new song to a playlist    5.view songs in a playlist by    6.Back to home:\n")

        home.Home()

    def art(self):
        home = homepage()
        choice = input("\n1.View artists  2.Add artist  3.Delete artist  4.Back to home:\n")
        a = artist()
        while choice != '4':
            if choice == '1':
                a.viewArtists()
            elif choice == '2':
                Artist = input("Enter the name of the new artist: ")
                a.addNewArtist(Artist)
            elif choice == '3':
                Artist = input("Enter the name of artist: ")
                a.deleteArtist(Artist)
            choice = input("\n1.View artists  2.Add artist  3.Delete artist  4.Back to home:\n")
        home.Home()

    def alb(self):
        home = homepage()
        print("\n1.View album  2.Add new album by a solo artist")
        choice = input("3.Add new album by a band  4.Delete an album  5.Back to home:\n")
        a=album()
        while choice != '5':
            if choice == '1':
                albumname = input("Enter the album's name: ")
                a.viewAlbum(albumname)
            elif choice == '2':
                albumname = input("Enter the album's name: ")
                artistname = input("Enter the artist's name: ")
                num = int(input("enter the number of songs you want to add: "))
                while num != 0:
                    songs = input("Enter a song: ")
                    dur = input("Enter its duration: ")
                    genre = input("Enter the song genre: ")
                    releasedate = input("Enter the release date: ")
                    num = num - 1
                    a.newAlbumByArtist(albumname, songs, dur, genre, releasedate, artistname)
            elif choice == '3':
                albumname = input("Enter the album's name: ")
                bandname = input("Enter the band's name: ")
                bandcount = input("Enter the number of members in the band: ")
                num = int(input("enter the number of songs you want to add: "))
                while num != 0:
                    songs = input("Enter a song: ")
                    dur = input("Enter its duration: ")
                    genre = input("Enter the song genre: ")
                    releasedate = input("Enter the release date: ")
                    num = num - 1
                    a.newAlbumByBand(albumname, songs, dur, genre, releasedate, bandname, bandcount)
            elif choice == '4':
                albumname = input("Enter the album's name: ")
                a.deleteAlbum(albumname)
            print("\n1.View album  2.Add new album by a solo artist")
            choice = input("3.Add new album by a band  4.Delete an album  5.Back to home:\n")
        home.Home()

    def band(self):
        home = homepage()
        choice = input("\n1.View bands  2.Add band  3.Delete band  4.Back to home:\n")
        b = band()
        while choice != '4':
            if choice == '1':
                b.viewBands()
            elif choice == '2':
                Band = input("Enter the name of the new band: ")
                b.addNewBand(Band)
            elif choice == '3':
                Band = input("Enter the name of band: ")
                b.deleteBand(Band)
            choice = input("\n1.View bands  2.Add band  3.Delete band  4.Back to home:\n")
        home.Home( )

    def lib(self):
        home = homepage()
        s=song()
        s.viewAllSongs()
        print("\n1.View song information  2.Add new song by an artist")
        choice = input("3.Add a new song by a band  4.delete song  5.Back to home:\n")
        while choice != '5':
            if choice == '1':
                songname = input("enter a song name: ")
                s.viewSong(songname)
            elif choice == '2':
                albumname = input("Enter the album's name: ")
                artistname = input("Enter the artist's name: ")
                num = int(input("enter the number of songs you want to add: "))
                while num != 0:
                    songs = input("Enter a song: ")
                    dur = input("Enter its duration: ")
                    genre = input("Enter the song genre: ")
                    releasedate = input("Enter the release date: ")
                    num = num - 1
                    s.addNewSongByArtist(albumname, songs, dur, genre, releasedate, artistname)
            elif choice == '3':
                albumname = input("Enter the album's name: ")
                bandname = input("Enter the band's name: ")
                num = int(input("enter the number of songs you want to add: "))
                while num != 0:
                    songs = input("Enter a song: ")
                    dur = input("Enter its duration: ")
                    genre = input("Enter the song genre: ")
                    releasedate = input("Enter the release date: ")
                    num = num - 1
                    s.addNewSongByBand(albumname, songs, dur, genre, releasedate, bandname)
            elif choice == '4':
                songname = input("enter a song name: ")
                s.deleteSong(songname)
            print("\n1.view song information  2.Add new song by an artist")
            choice = input("3.Add a new song by a band  4.delete song  5.Back to home:\n")
        home.Home()

    def Home(self):
        home = homepage()
        choice = input("\n1.Playlist   2.Artists   3.Albums   4.Bands   5.Library   6.Exit\n")
        if choice == '1':
            home.plists()
        elif choice == '2':
            home.art()
        elif choice == '3':
            home.alb()
        elif choice == '4':
            home.band()
        elif choice == '5':
            home.lib()
        elif choice == '6':
            conn.close()
            quit()

home = homepage()
home.Home()



