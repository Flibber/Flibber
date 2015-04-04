# 1: Change the variables here and navigate to the URL, the page you are redirected to will have your CODE appended to the URI
# https://api.instagram.com/oauth/authorize/?client_id=<CLIENT_ID_HERE>&redirect_uri=<REDIRECT_URI_HERE>&response_type=code&display=touch&scope=likes+relationships
#
# 2: Change the variables here and navigate to this URL, get the ACCESS_TOKEN from the response
# https://api.instagram.com/oauth/access_token?client_id=<CLIENT_ID_HERE>&client_secret=<CLIENT_SECRET_HERE>&redirect_uri=<REDIRECT_URI_HERE>&code=<CODE_HERE>&grant_type=authorization_code

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
