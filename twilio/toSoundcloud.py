from soundcloud import Client
from secrets import soundcloudSecrets

# Create a new client that uses the user credentials oauth flow
client = Client(  client_id = soundcloudSecrets['APP_ID'],
                  client_secret = soundcloudSecrets['APP_SECRET'],
                  username = soundcloudSecrets['USERNAME'],
                  password = soundcloudSecrets['PASSWORD'])

def postSoundcloud(barbershopID, audioPath):
  track = client.post('/tracks', track={
                        'title': "BARBERSHOP'D " + str(barbershopID),
                        'sharing': 'public',
                        'asset_data': open(audioPath, 'rb')
                        })
  soundcloudURL = track.permalink_url
  return soundcloudURL

if __name__ == '__main__':
  postSoundcloud("TESTID", "../audioOutput.wav")
