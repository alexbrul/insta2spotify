# insta2spotify


Lets you get all the tracks from an instagram page into a spotify playlist

You need to get your own ARCCloud api key and account, and also add your own spotify details. I think you can use the spotify "app" I created, but not 100% sure. if not, remember to add redirect url (use localhost).  

Flow:
1. Downloads n videos from instagram
2. Extracts the mp3
3. Uploads to arcCloud (shazam copy but free if you request an api key)
4. searches for songname+ " " + artist on spotify, picks the first search result and adds to your spotify playlist


Things that can go wrong:
- It might not create all the folders correctly
- If the instagram page is remix heavy, it might not recognize the song or it could select wrong result in the search. 


