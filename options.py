# 1: Change the variables here and navigate to the URL, the page you are
# redirected to will have your CODE appended to the URI
#
# https://api.instagram.com/oauth/authorize/?client_id=<CLIENT_ID_HERE>&redirect_uri=<REDIRECT_URI_HERE>&response_type=code&display=touch&scope=likes+relationships
#
# 2: Run the program, it will execute correctly, but will give you the
# ACCESS_TOKEN on the first run which you should replace below
#

INSTAGRAM_API = "https://api.instagram.com/v1/"
USER_AGENT = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) \
AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 \
Mobile/8A293 Safari/6531.22.7'

CLIENT_ID = "<CLIENT_ID_HERE>"  # CHANGE THIS
CLIENT_SECRET = "<CLIENT_SECRET_HERE>"  # CHANGE THIS
IP = "8.8.8.8"  # PUBLIC IP - CHANGE THIS
REDIRECT_URI = "https://example.com"  # CHANGE THIS
ACCESS_TOKEN = "<ACCESS_TOKEN_HERE>"  # CHANGE AFTER FIRST RUN

ACTION = "LIKE_FOLLOW"  # CHANGE IF DESIRED
# LIKE (like photos based on TAGS below)
# LIKE_FOLLOW (like and follow users based on TAGS below)
# UNFOLLOW (unfollow users who are not following you)
# UNFOLLOW_ALL (unfollow all users)
# POPULAR (like photos and follow users based on popular tags)

MAX_COUNT = 10  # ACTIONS PER TAG - CHANGE IF YOU WANT
MAX_SECS = 3  # INCREASE IF YOUR ACCESS_TOKEN KEEPS GETTING REVOKED

TAGS = ["me", "selfie", "love"]
