# 1: Change the variables here and navigate to the URL, the page you are
# redirected to will have your CODE appended to the URI
# https://api.instagram.com/oauth/authorize/?client_id=<CLIENT_ID_HERE>&redirect_uri=<REDIRECT_URI_HERE>&response_type=code&display=touch&scope=likes+relationships
#
# 2: Change the variables here and POST this URL (POSTman for Chrome), get the
# ACCESS_TOKEN from the response:
# https://api.instagram.com/oauth/access_token
# client_id=<CLIENT_ID_HERE>
# client_secret=<CLIENT_SECRET_HERE>
# redirect_uri=<REDIRECT_URI_HERE>
# code=<CODE_HERE>
# grant_type=authorization_code

INSTAGRAM_API = "https://api.instagram.com/v1/"
USER_AGENT = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) \
AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 \
Mobile/8A293 Safari/6531.22.7'

ACCESS_TOKEN = "ACCESS_TOKEN_HERE"  # CHANGE
CLIENT_ID = "<CLIENT_ID_HERE>"  # CHANGE THIS
CLIENT_SECRET = "<CLIENT_SECRET_HERE>"  # CHANGE THIS
IP = "8.8.8.8"  # PUBLIC IP - CHANGE THIS

ACTION = "LIKE_FOLLOW"
# LIKE (like photos based on TAGS below)
# LIKE_FOLLOW (like and follow users based on TAGS below)
# UNFOLLOW (unfollow users who are not following you)
# UNFOLLOW_ALL (unfollow all users)
# POPULAR (like photos and follow users based on popular tags)

MAX_COUNT = 10  # ACTIONS PER TAG - CHANGE IF YOU WANT
MAX_SECS = 3  # INCREASE IF YOUR ACCESS_TOKEN KEEPS GETTING REVOKED

TAGS = ["me", "selfie", "love"]
