from uiautomator import device as d
from awsRekognition import image_validation
from time import sleep
from datetime import datetime
import switcher
import os
import json

blocked_words = []
liked = 0
notLiked = 0
skipped = 0
imageCount = 0


def getBlockedWords():
    with open("blocked words.txt", "r") as f:
        return json.loads(f.read())


def printInfo():
    print("Number of posts liked:", liked)
    print("Number of posts not liked:", notLiked)
    print("Number of times skipped:", skipped)


def likeAndRetreat():
    global liked
    d(resourceId="com.instagram.android:id/row_feed_button_like").wait.exists(
        timeout=10000
    )
    d(resourceId="com.instagram.android:id/row_feed_button_like").click()
    liked += 1
    sleep(1)
    d.press.back()
    sleep(3)


def retreatAndDismiss():
    global notLiked
    d.press.back()
    d(textContains="You did not put a").wait.exists(timeout=30000)
    d.click(0, 500)
    notLiked += 1


def perform_action():

    global imageCount

    if d(scrollable=True).exists:
        d(scrollable=True).fling()

    for word in blocked_words:

        a = (
            d(descriptionContains=word).exists
            if word == "Reels"
            else d(textContains=word).exists
        )
        if a:
            print("Blocked word detected:", word)
            retreatAndDismiss()
            return

    if d(scrollable=True).exists:
        d(scrollable=True).fling.vert.backward()

    image_file_name = "image.png"
    d.screenshot(image_file_name)
    imageCount += 1
    like = image_validation(image_file_name, imageCount % 2)

    if like:
        likeAndRetreat()
    else:
        retreatAndDismiss()

    os.remove(image_file_name)


def skip():
    global skipped
    d(resourceId="neutrino.plus:id/skip_button").wait.exists(timeout=30000)
    d(resourceId="neutrino.plus:id/skip_button").click()
    skipped += 1


def start():

    d(resourceId="neutrino.plus:id/floatActionButton").click()

    for i in range(1000):

        d(textContains="This order doesn't").wait.exists(timeout=3000)

        if (
            d(textContains="You have skipped").exists
            or d(textContains="Come back in").exists
        ):
            return

        if (
            d(textContains="This order doesn't").exists
            or d(textContains="You did not put a").exists
            or d(textContains="Too many time").exists
            or d(textContains="Fraud").exists
        ):
            d.click(0, 500)

        d(resourceId="neutrino.plus:id/like_button", enabled=True).wait.exists(
            timeout=1000
        )

        print(
            "\n" + str(i + 1),
            ":",
            d(resourceId="neutrino.plus:id/like_button", enabled=True).exists,
        )

        if d(resourceId="neutrino.plus:id/like_button", enabled=True).exists:
            d(resourceId="neutrino.plus:id/like_button", enabled=True).click()
            d(resourceId="com.instagram.android:id/feed_more_button_stub").wait.exists(
                timeout=10000
            )
            if(d(resourceId="com.instagram.android:id/feed_more_button_stub").exists):
                perform_action()
            else:
                retreatAndDismiss()
        else:
            skip()


def main():

    global blocked_words, liked, notLiked, skipped

    try:
        blocked_words = getBlockedWords()
        d(text="Neutrino+", className="android.widget.TextView").click()
        d(resourceId="neutrino.plus:id/floatActionButton").wait.exists(timeout=60000)

        currentAccount = (
            "tuplestudio" if d(text="@tuplestudio").exists else "bookmosphere"
        )

        if d(resourceId="neutrino.plus:id/dailyBonusTextView",clickable=True).exists:
            d(resourceId="neutrino.plus:id/dailyBonusTextView",clickable=True).click()

        print("\nCurrent Account:", currentAccount)
        startTime = datetime.now()
        start()
        print("\n\nCurrent Account:", currentAccount)
        printInfo()
        print("Start:", startTime)
        print("End:", datetime.now())

        liked = 0
        notLiked = 0
        skipped = 0

        if currentAccount == "tuplestudio":
            switcher.switchAccount("bookmosphere")
        else:
            switcher.switchAccount("tuplestudio")

        currentAccount = (
            "tuplestudio" if d(text="@tuplestudio").exists else "bookmosphere"
        )

        print("\n\nCurrent Account:", currentAccount)
        startTime = datetime.now()
        start()
        print("\n\nCurrent Account:", currentAccount)
        printInfo()
        print("Start:", startTime)
        print("End:", datetime.now())

        liked = 0
        notLiked = 0
        skipped = 0

        if currentAccount == "tuplestudio":
            switcher.switchAccount("bookmosphere")
        else:
            switcher.switchAccount("tuplestudio")

        switcher.clearRecent()

    except Exception as exception:
        print("\nException occured in main:", type(exception).__name__)
        print("\n\nCurrent Account:", currentAccount)
        printInfo()
        print("Start:", startTime)
        print("End:", datetime.now())
        switcher.clearRecent()
        liked = 0
        notLiked = 0
        skipped = 0
        main()


if __name__ == "__main__":
    main()