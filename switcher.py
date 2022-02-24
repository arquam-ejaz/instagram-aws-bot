from uiautomator import device as d
import json
from time import sleep


def getInstagramCredentials():
    with open("instagram credentials.txt", "r") as f:
        return json.loads(f.read())


def clearRecent():
    d.press.recent()
    d(scrollable=True).wait.exists(timeout=10000)
    d(scrollable=True).fling.horiz.toBeginning(max_swipes=3)
    d(text="CLEAR ALL").click()


def switchAccount(account):
    d.press.back()
    d(description="More options").wait.exists(timeout=3000)
    d(description="More options").click()
    d(text="Settings").click()
    d(scrollable=True).fling()
    d(text="Logout").click()
    d(resourceId="neutrino.plus:id/signInButton").click()
    d(index="1", className="android.widget.EditText").set_text(account)
    d(text="Password").sibling(index="1", className="android.widget.EditText").set_text(
        instagramCredentials[account]
    )
    d(text="Log In").click()
    sleep(7)
    d(resourceId="neutrino.plus:id/action_done").click()
    d(resourceId="neutrino.plus:id/floatActionButton").wait.exists(timeout=30000)
    clearRecent()
    d(text="Instagram", className="android.widget.TextView").click()
    d(description="Profile", longClickable=True).wait.exists(timeout=10000)
    d(description="Profile", longClickable=True).click()
    d(resourceId="com.instagram.android:id/title_view").click()
    d(text=account).click()
    sleep(5)
    clearRecent()
    d(text="Neutrino+", className="android.widget.TextView").click()
    d(resourceId="neutrino.plus:id/floatActionButton").wait.exists(timeout=30000)


instagramCredentials = getInstagramCredentials()
