from pprint import pprint
import spotipy_login_util as spotipy_login

# Shows playing devices
sp = spotipy_login.get_spotipy_obj()
res = sp.devices()

pprint(res)
