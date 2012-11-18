from soundcloud import Client

appID = "4b071ae3c5073b338c0c4fa908d8a172"
appSecret = "4aaa35e78ded3bee7e50cb17d93e3974"

# Create a new client that uses the user credentials oauth flow
client = Client(client_id=appID,
                           client_secret=appSecret,
                           username='danhgn@gmail.com',
                           password='haj8nalP')

# print the username of the authorized user
print client.get('/me').username

def postBarbershop(barbershopID, audioPath):

  track = client.post('/tracks', track={
      'title': "BARBERSHOP'D " + str(barbershopID),
      'sharing': 'public',
      'asset_data': open(audioPath, 'rb')
      })

  print track.title
  soundcloudURL = track.url

  print soundcloudURL

  return soundcloudURL

if __name__ == '__main__':
  postBarbershop("TESTID", "../audioOutput.wav")
