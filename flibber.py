try:
    import time
    import random
    import re
    import pycurl
    import hmac
    import urllib
    import urllib2
    import simplejson
    import sys
    import calendar
    import options
    from hashlib import sha256
    try:
        from io import BytesIO
    except ImportError:
        from StringIO import StringIO as BytesIO

    # If you change these delays, you will exceed the Instagram API rate-limit
    # Or, the bot will be running slower than necessary
    LIKE_DELAY = 36
    REL_DELAY = 60
    API_DELAY = 0

    # DO NOT CHANGE ANYTHING BELOW THIS POINT

    NO_FOLLOW = 0
    FOLLOWS = 1

    likedDict = {}
    headers = {}
    dataDict = ""
    count = 0
    response = "500"

    totalFollows = 0
    totalUnfollows = 0
    totalAPICalls = 0
    totalLikes = 0
    totalErrors = 0

    globErrorMessage = ""
    errorLevel = 0

    class tCol:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    def currentTime():
        theTime = calendar.timegm(time.gmtime())
        return theTime

    lastLike = currentTime() - LIKE_DELAY
    lastRel = currentTime() - REL_DELAY
    lastAPI = currentTime() - API_DELAY

    userArray = []
    likeArray = []
    APIArray = []
    followArray = []
    followedArray = []

    relArray = []
    picArray = []

    def msg(message, prefix="FLIB", level="OKGREEN"):
        print ("[" + getattr(tCol, level) + prefix + tCol.ENDC + "] " +
               getattr(tCol, level) + message + tCol.ENDC)

    def execPause(length):
        msg('Paused for ' + tCol.FAIL + str(length) +
            tCol.WARNING + ' seconds...', "TIME", "WARNING")
        time.sleep(length)

    if options.ACCESS_TOKEN == "changeme" or options.CLIENT_ID == "changeme":
        print msg("You must change all variables which equal 'changeme'",
                  "FAIL", "FAIL")
        sys.exit(1)
    elif options.CLIENT_SECRET == "changeme" or options.IP == "changeme":
        print msg("You must change all variables which equal 'changeme'",
                  "FAIL", "FAIL")
        sys.exit(1)

    def headerFunction(header_line):
        if ':' not in header_line:
            return
        name, value = header_line.split(':', 1)
        name = name.strip()
        value = value.strip()
        name = name.lower()
        headers[name] = value

    def reqURL(url, post="", proto="GET", reqType="API"):
        global count, dataDict, response, globErrorMessage
        global API_DELAY, LIKE_DELAY, REL_DELAY
        global totalAPICalls, totalErrors, errorLevel

        bytesIO = BytesIO()
        pc = pycurl.Curl()

        signature = hmac.new(
            options.CLIENT_SECRET, options.IP, sha256).hexdigest()
        header = '|'.join([options.IP, signature])
        header = ["X-Insta-Forwarded-For: " + header]

        post_data = {'options.ACCESS_TOKEN': options.ACCESS_TOKEN,
                     'options.CLIENT_ID': options.CLIENT_ID}
        post_data.update(post)
        postfields = urllib.urlencode(post_data)

        if proto == "POST":
            pc.setopt(pc.CUSTOMREQUEST, 'POST')
            pc.setopt(pc.POSTFIELDS, postfields)
        else:
            getURL = url
            url = url + "?" + postfields
            pc.setopt(pc.CUSTOMREQUEST, 'GET')

        pc.setopt(pc.URL, str(url))
        pc.setopt(pc.WRITEFUNCTION, bytesIO.write)
        pc.setopt(pc.HEADERFUNCTION, headerFunction)
        pc.setopt(pycurl.HTTPHEADER, header)

        count = count + 1

        timeDifference = currentTime() - lastAPI
        if timeDifference < API_DELAY:
            execPause(API_DELAY - timeDifference)
        if len(APIArray) > 0:
            while APIArray[0] <= currentTime() - 3600:
                del APIArray[0]
            if len(relArray) >= 4999:
                waitTime = currentTime() - APIArray[0] - 3600
                execPause(waitTime)

        try:
            totalAPICalls = totalAPICalls + 1
            pc.perform()
            response = str(pc.getinfo(pc.HTTP_CODE))
            pc.close()

            encoding = None
            if 'content-type' in headers:
                content_type = headers['content-type'].lower()
                match = re.search('charset=(\S+)', content_type)
                if match:
                    encoding = match.group(1)
            if encoding is None:
                encoding = 'iso-8859-1'

            body = bytesIO.getvalue()

            dataDict = simplejson.loads(body)
            msg(tCol.BOLD + 'Request #' + str(count), "NUM#", "HEADER")
            msg('Remaining API calls: ' + tCol.FAIL +
                headers['x-ratelimit-remaining'] + '/' +
                headers['x-ratelimit-limit'] + tCol.ENDC, "RATE", "OKBLUE")
        except Exception as e:
            dataDict = ""
            response = "500"
            error_message = e
            errorLevel = errorLevel + 1
            if errorLevel > 3:
                msg("Error level exceeded, check options.",
                    "ERRO", "FAIL")
                sys.exit(1)

        errorLevel = 0

        if proto == "POST":
            msg(url, "RURL", "OKBLUE")
        else:
            msg(getURL, "RURL", "OKBLUE")

        msg(postfields, "FLDS", "OKBLUE")
        msg(proto, "HTTP", "OKBLUE")

        if response == "200":
            msg(response, "CODE")
            APIArray.append(currentTime())
        elif response == "500":
            totalErrors = totalErrors + 1
            globErrorMessage = str(error_message)
            if globErrorMessage == "(23, 'Failed writing header')":
                print ""
                msg(tCol.BOLD + "Keyboard Interrupt!", "INPT", "FAIL")
                sys.exit(1)
            msg(str(error_message), "ERRO", "FAIL")
        elif response != "200":
            totalErrors = totalErrors + 1
            error_message = dataDict["meta"]["error_message"]
            error_type = dataDict["meta"]["error_type"]
            msg(response, "CODE", "FAIL")
            msg(error_type, "TYPE", "FAIL")
            msg(error_message, "FAIL", "FAIL")
            if response == "400" and error_type == "OAuthAccessTokenException":
                sys.exit(1)
            if response == "429":
                rates = [int(s) for s in error_message.split() if s.isdigit()]
                msg('Rate exceeded: ' + tCol.FAIL + str(rates[0]) + '/' + str(
                    rates[1]) + tCol.WARNING + ' in the last hour.',
                    "RATE", "WARNING")
                if reqType == "Like":
                    LIKE_DELAY = LIKE_DELAY + 1
                    rateArray = likeArray
                    rateLen = 99
                elif reqType == "Relation":
                    REL_DELAY = REL_DELAY + 1
                    rateArray = relArray
                    rateLen = 99
                else:
                    API_DELAY = API_DELAY + 1
                    rateArray = APIArray
                    rateLen = 4999
                rateDiff = rateLen - len(rateArray)
                if rateDiff > 0:
                    while len(rateArray) < rateLen:
                        rateArray.append(currentTime())
                rateArray[0] = currentTime() - 3900
                waitTime = 0
                waitTime = currentTime() - rateArray[0] - 3600
                execPause(waitTime)
                reqURL(url, post, proto, reqType)

        return dataDict

    def getUsers(next_cursor=None, num_users=0, stage=0):
        global userArray
        if stage == 0:
            userURL = options.INSTAGRAM_API + "users/self/follows"
            arrayName = followArray
        elif stage == 1:
            userURL = options.INSTAGRAM_API + "users/self/followed-by"
            arrayName = followedArray
        else:
            userArray = list(set(followArray) - set(followedArray))
            msg(tCol.FAIL + tCol.BOLD + str(num_users) + tCol.ENDC +
                tCol.WARNING +
                " users added to interaction blacklist", "USER", "WARNING")
            return

        if next_cursor is not None:
            post = {'cursor': next_cursor}
        else:
            post = {}

        data = reqURL(userURL, post)
        if response != "200":
            if globErrorMessage == "(23, 'Failed writing header')":
                sys.exit(1)
            msg("Retrying request...", "RTRY", "WARNING")
            getUsers(next_cursor, num_users, stage)
            return

        dataPage = data["pagination"]

        next_cursor = None
        if dataPage:
            next_cursor = data["pagination"]["next_cursor"]
        for user in data["data"]:
            for k, v in user.iteritems():
                if k == "id":
                    userID = v
                    arrayName.append(userID)
                    num_users = num_users + 1

        if next_cursor is None:
            stage = stage + 1
        getUsers(next_cursor, num_users, stage)

    def getFollowing(next_cursor=None, num_users=0):
        global userArray
        userURL = options.INSTAGRAM_API + "users/self/follows"

        if next_cursor is not None:
            post = {'cursor': next_cursor}
        else:
            post = {}

        data = reqURL(userURL, post)
        if response != "200":
            if globErrorMessage == "(23, 'Failed writing header')":
                sys.exit(1)
            msg("Retrying request...", "RTRY", "WARNING")
            getFollowing(next_cursor, num_users)
            return

        dataPage = data["pagination"]

        next_cursor = None
        if dataPage:
            next_cursor = data["pagination"]["next_cursor"]
        for user in data["data"]:
            for k, v in user.iteritems():
                if k == "id":
                    userID = v
                    followArray.append(userID)
                    num_users = num_users + 1

        if next_cursor is None:
            userArray = list(set(followArray))
            msg(tCol.FAIL + tCol.BOLD + str(num_users) + tCol.ENDC +
                tCol.WARNING +
                " users added to interaction blacklist", "USER", "WARNING")
            return
        getFollowing(next_cursor, num_users)

    def getPics(next_max_like_id=None, num_likes=0):
        likeURL = options.INSTAGRAM_API + "users/self/media/liked"

        if next_max_like_id is not None:
            post = {'max_like_id': next_max_like_id}
        else:
            post = {}

        data = reqURL(likeURL, post)
        if response != "200":
            if globErrorMessage == "(23, 'Failed writing header')":
                sys.exit(1)
            msg("Retrying request...", "RTRY", "WARNING")
            getPics(next_max_like_id, num_likes)
            return

        dataPage = data["pagination"]

        next_max_like_id = None
        if dataPage:
            next_max_like_id = data["pagination"]["next_max_like_id"]

        for image in data["data"]:
            for k, v in image.iteritems():
                if k == "id":
                    imageID = v
                    picArray.append(imageID)
                    num_likes = num_likes + 1

        if next_max_like_id is not None:
            getPics(next_max_like_id, num_likes)
        else:
            msg(tCol.FAIL + tCol.BOLD + str(num_likes) + tCol.ENDC +
                tCol.WARNING +
                " pictures added to interaction blacklist", "LIKE", "WARNING")

    # Like `pictureID`
    def likePicture(pictureID):
        if pictureID in picArray:
            msg("You already like picture " +
                tCol.WARNING + pictureID, "LIKE", "FAIL")
            return
        global totalLikes
        global lastLike
        likeURL = options.INSTAGRAM_API + "media/%s/likes" % (pictureID)
        msg("Liking picture " + pictureID, "LIKE")
        timeDifference = currentTime() - lastLike
        if timeDifference < LIKE_DELAY:
            execPause(LIKE_DELAY - timeDifference)
        if len(likeArray) > 0:
            while likeArray[0] <= currentTime() - 3600:
                del likeArray[0]
            if len(likeArray) >= 99:
                waitTime = currentTime() - likeArray[0] - 3600
                if waitTime > 0:
                    execPause(waitTime)
        reqURL(likeURL, "", "POST", "Like")
        if response != "200":
            return
        lastLike = currentTime()
        likeArray.append(currentTime())
        totalLikes = totalLikes + 1

    # Follow or unfollow `userID`
    def modUser(userID, action):
        global lastRel
        userURL = options.INSTAGRAM_API + "users/%s" % (userID)
        modURL = userURL + "/relationship"
        data = reqURL(userURL)
        if response != "200":
            return
        try:
            followsCount = int(data['data']['counts']['follows'])
            followedByCount = int(data['data']['counts']['followed_by'])
        except Exception:
            msg("Failed to get follow counts. Skipping...", "FLLW", "FAIL")
            return
        post = {'action': action}
        if action == "follow":
            if userID in userArray:
                msg("You are already following user " +
                    tCol.WARNING + userID, "FLLW", "FAIL")
                return
            if followsCount < (followedByCount / 2):
                msg("User " + tCol.WARNING + userID + tCol.FAIL +
                    " is following less than half of their follower count.",
                    "FLLW", "FAIL")
                return
            verbAct = "Following"
            swap = 0
        elif action == "unfollow":
            if userID not in userArray:
                msg("You are not following user " +
                    tCol.WARNING + userID, "FLLW", "FAIL")
                return
            verbAct = "Unfollowing"
            swap = 1
        elif action == "block":
            verbAct = "Blocking"
            swap = 1
        timeDifference = currentTime() - lastRel
        if timeDifference < REL_DELAY:
            execPause(REL_DELAY - timeDifference)
        if len(relArray) > 0:
            while relArray[0] <= currentTime() - 3600:
                del relArray[0]
            if len(relArray) >= 99:
                waitTime = currentTime() - relArray[0] - 3600
                if waitTime > 0:
                    execPause(waitTime)
        msg(verbAct + " user " + userID, "RLAT")
        reqURL(modURL, post, "POST", "Relation")
        if response != "200":
            return
        if action == "follow":
            if userID not in userArray:
                userArray.append(userID)
        else:
            if userID in userArray:
                userArray.remove(userID)
        lastRel = currentTime()
        relArray.append(currentTime())
        if action != "block":
            getRelationship(userID, "outgoing", swap)

    # Return relationship to `userID`
    def getRelationship(userID, direction="incoming", swap=0):
        global totalFollows, totalUnfollows
        followURL = options.INSTAGRAM_API + "users/%s/relationship" % (userID)
        data = reqURL(followURL)
        if response != "200":
            return
        status = data["data"]
        incoming = status["incoming_status"]
        outgoing = status["outgoing_status"]

        if swap == 1:
            followLevel = "FAIL"
            noFollowLevel = "OKGREEN"
        else:
            followLevel = "OKGREEN"
            noFollowLevel = "FAIL"

        if direction == "outgoing":
            if outgoing == "follows":
                if swap == 0:
                    totalFollows = totalFollows + 1
                msg("You are following user " + userID, "GREL", followLevel)
                return FOLLOWS
            else:
                if swap == 1:
                    totalUnfollows = totalUnfollows + 1
                msg("You are not following user " + userID,
                    "GREL", noFollowLevel)
                return NO_FOLLOW
        else:
            if incoming != "followed_by":
                msg("User " + userID + " does not follow you",
                    "GREL", noFollowLevel)
                return NO_FOLLOW
            else:
                msg("User " + userID + " follows you", followLevel)
                return FOLLOWS

    # Unfollow users who are not following back
    def unfollowUsers(allUsers=False):
        num_unfollows = 0
        for userID in userArray:
            if allUsers is True:
                modUser(userID, "unfollow")
                num_unfollows = num_unfollows + 1
            elif allUsers is False:
                relationship = getRelationship(userID)
                if relationship == NO_FOLLOW:
                    modUser(userID, "unfollow")
                    num_unfollows = num_unfollows + 1
            secs = random.randint(1, options.MAX_SECS)
            time.sleep(secs)
        print num_unfollows
        if num_unfollows % 10 == 0:
            print "Unfollowed %s users " % num_unfollows
        msg("Number of users unfollowed is " + str(num_unfollows), "UNFL")
        options.ACTION = "LIKE_FOLLOW"
        begin()
        return num_unfollows

    def likeUsers(max_results, max_id, tag, likeCount, followCount):
        urlFindLike = options.INSTAGRAM_API + "tags/%s/media/recent" % (tag)
        post = {'max_id': max_id}
        data = reqURL(urlFindLike, post)
        if response != "200":
            return
        likeCount = 0
        followCount = 0
        for likeObj in data['data']:
            user = likeObj['user']
            userID = user['id']
            if userID not in userArray:
                try:
                    likeFollowCount = likeAndFollowUser(userID)
                    likeCount = likeCount + likeFollowCount
                except Exception:
                    return
                if (options.ACTION == "LIKE_FOLLOW"):
                    followCount = followCount + 1
                secs = random.randint(1, options.MAX_SECS)
                time.sleep(secs)
            if (likeCount % 10 == 0 and likeCount != 0):
                msg('Liked ' + str(likeCount) +
                    ' pictures from #' + tag, 'LIKE')
            if (options.ACTION == "LIKE_FOLLOW"):
                if (followCount % 10 == 0 and followCount != 0):
                    msg('Followed ' + str(followCount) +
                        ' users from #' + tag, 'FLLW')
                if (followCount == max_results):
                    break
            elif (options.ACTION == "LIKE"):
                if (likeCount == max_results):
                    break
        # if(likeCount != max_results):
        #    likeUsers(max_results, max_id, tag, likeCount, followCount)
        msg('Liked ' + str(likeCount) + ' pictures and followed ' +
            str(followCount) + ' users from tag #' + tag, 'options.TAGS')
        return

    # Like and follow users
    def likeAndFollowUser(userID, follow=True):
        numLikesFollows = 0
        userURL = options.INSTAGRAM_API + "users/%s" % (userID)
        urlUserMedia = userURL + "/media/recent"
        data = reqURL(userURL)
        if response != "200":
            return
        followsCount = data['data']['counts']['follows']
        followedByCount = data['data']['counts']['followed_by']
        if followsCount < (followedByCount / 2):
            msg("User " + tCol.WARNING + userID + tCol.FAIL +
                " is following less than half of their follower count.",
                "FLLW", "FAIL")
            return
        data = reqURL(urlUserMedia)
        if response != "200":
            return
        picsToLike = random.randint(1, 4)
        msg("Liking " + str(picsToLike) + " pictures for user " + str(userID))
        countPicViews = 0
        for picture in data['data']:
            if picture['id'] not in likeArray:
                likePicture(picture['id'])
                countPicViews = countPicViews + 1
                numLikesFollows = numLikesFollows + 1
                if(countPicViews == picsToLike):
                    break
        if follow:
            modUser(userID, "follow")
        return numLikesFollows

    def popFunction():
        urlPopular = options.INSTAGRAM_API + "media/popular"
        data = reqURL(urlPopular)
        if response != "200":
            return
        followCount = 0
        likeCount = 0
        for obj in data['data']:
            for comment in obj['likes']['data']:
                myid = comment['id']
                result = likeAndFollowUser(myid)
                if(result > 0):
                    followCount = followCount + 1
                likeCount = likeCount + 1
                if(followCount % 10 == 0):
                    msg("Followed " + str(followCount) +
                        " users", "followCount")
                seconds = random.randint(1, options.MAX_SECS)
                time.sleep(seconds)
                if (followCount == options.MAX_COUNT):
                    break
            if (followCount == options.MAX_COUNT):
                break
        msg("Followed " + str(followCount) + " users", "followCount")
        msg("Liked " + str(likeCount) + " pictures", "LIKE")

    def decider():
        if(options.ACTION == "LIKE" or options.ACTION == "LIKE_FOLLOW"):
            getUsers()
            getPics()
            for tag in options.TAGS:
                likeUsers(options.MAX_COUNT, 0, tag, 0, 0)
        elif(options.ACTION == "POPULAR"):
            getUsers()
            getPics()
            popFunction()
        elif(options.ACTION == "UNFOLLOW"):
            getUsers()
            unfollowUsers(False)
        elif(options.ACTION == "UNFOLLOW_ALL"):
            getFollowing()
            unfollowUsers(True)
        else:
            msg("Invalid ACTION specified", "ACTO", "FAIL")

    def begin():
        decider()
        begin()

    msg("----------------------", "FLIB", "HEADER")
    msg("  Welcome to Flibber  ", "FLIB", "HEADER")
    msg("  Chip (itschip.com)  ", "FLIB", "HEADER")
    msg("----------------------", "FLIB", "HEADER")

    begin()

except KeyboardInterrupt:
    print ""
    msg(tCol.BOLD + "Keyboard Interrupt!", "INPT", "FAIL")

except Exception as e:
    print ""
    msg(tCol.BOLD + str(e), "EXEP", "FAIL")

else:
    print ""
    msg(tCol.BOLD + "Unknown Error!", "ERRO", "FAIL")

finally:
    print ""
    msg(tCol.UNDERLINE + "Statistics from run:", "STAT", "WARNING")
    msg("Total Unfollows: " + tCol.BOLD + str(totalUnfollows), "STAT", "FAIL")
    msg("Total Follows: " + tCol.BOLD + str(totalFollows), "STAT", "OKGREEN")
    msg("Total Likes: " + tCol.BOLD + str(totalLikes), "STAT", "OKBLUE")
    msg("Total API Calls: " + tCol.BOLD + str(totalAPICalls), "STAT", "HEADER")
    print ""
