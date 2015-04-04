# https://api.instagram.com/oauth/authorize/?client_id=ceaadb365bec45a7b586c0c576667307&redirect_uri=https://starbs.net&response_type=code&display=touch&scope=likes+relationships
#
# curl -F 'client_id=ceaadb365bec45a7b586c0c576667307' -F 'client_secret=0d0d7cfb3bec4de5b4f04c308dc9bc9e' -F 'grant_type=authorization_code' -F 'redirect_uri=https://starbs.net' -F 'code=3cc14d84222540a194144c6b30097f53' https://api.instagram.com/oauth/access_token

INSTAGRAM_API = "https://api.instagram.com/v1/"
USER_AGENT = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'
ACCESS_TOKEN = "1771349103.ceaadb3.0e34181c8b2644a4bd5d761cfc7ebd58" # CHANGE THIS
CLIENT_ID = "ceaadb365bec45a7b586c0c576667307" # CHANGE THIS
CLIENT_SECRET = "0d0d7cfb3bec4de5b4f04c308dc9bc9e" # CHANGE THIS
IP = "178.62.84.134" # PUBLIC IP - CHANGE THIS
ACTION = "LIKE_FOLLOW"
MAX_COUNT = 10 # ACTIONS PER TAG - CHANGE IF YOU WANT
MAX_SECS = 3 # INCREASE IF YOUR ACCESS_TOKEN KEEPS GETTING REVOKED

TAGS = ["me", "selfie", "love"]
