"""
This code starts a script that listens for RFID tags UID's
If a UID is entered we scan our music_uid_config.csv file to see if their is a track
or playlist that matches the UID.  If the UID wasn't recenlty (e.g. 10 seconds)
added then we go ahead and play the associated track.
"""

# import RPi.GPIO as GPIO
from pn532 import *
import csv
import spotipy_login_util as spotipy_util


# Read our uid to music map in
with open("music_uid_config.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=";")
    uid_music_dict = {
        rows[0]: {"uri": rows[1], "description": rows[2]} for rows in reader
    }


def hex_uid_to_string(uid=None):
    return str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3])


def get_spotify_uri(uid=""):
    return uid_music_dict[hex_uid_to_string(uid)]["uri"]


def get_spotify_description(uid=""):
    return uid_music_dict[hex_uid_to_string(uid)]["description"]


def play_spotify_music(uri="spotify:track:1QPRmX2e3EZWskuOe5QqxM"):
    sp = spotipy_util.get_spotipy_obj()
    print("Playing on Device", spotipy_util.SPOTIFY_DEVICE_ID)
    device_id = spotipy_util.SPOTIFY_DEVICE_ID

    # play if its a track based uri
    if "track" in uri:
        sp.start_playback(
            uris=[uri],
            device_id=device_id,
        )
    else:  # assume its a playlist or artist. This needs a context_uri
        sp.start_playback(
            context_uri=uri,
            device_id=device_id,
        )


if __name__ == "__main__":

    # pn532 = PN532_SPI(debug=False, reset=20, cs=4)
    # pn532 = PN532_I2C(debug=False, reset=20, req=16)
    pn532 = PN532_UART(debug=False, reset=20)

    ic, ver, rev, support = pn532.get_firmware_version()
    print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

    # Configure PN532 to communicate with MiFare cards
    pn532.SAM_configuration()

    # Track the alst UID we looked at
    PRIOR_UID = ""

    print("Waiting for RFID/NFC card...")
    while True:
        # Check if a card is available to read
        try:
            uid = pn532.read_passive_target(timeout=0.5)

            # Try again if no card is available.
            if uid is None:
                continue

            # Check if the UID is the last UID Recorded
            # If it is don't do anything as we are already playing music
            if uid == PRIOR_UID:
                continue

            # Set Prior UID to be current UID
            PRIOR_UID = uid

            # Print Valid Card
            print("Found card with UID:", [hex(i) for i in uid], hex_uid_to_string(uid))

            # This looks up the uid of rfid is on our dict file that maps a uid to a spotify uri
            print("playing: ", get_spotify_description(uid))
            play_spotify_music(uri=get_spotify_uri(uid))
        except Exception as e:
            print(e)
            continue
        # finally:
        #     GPIO.cleanup()
