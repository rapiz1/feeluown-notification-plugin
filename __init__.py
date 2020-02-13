from fuocore.models import reverse
from fuocore import aio
from feeluown.fuoexec import add_hook, rm_hook
from gi.repository import Notify, GdkPixbuf

__alias__ = 'Desktop Notification'
__version__ = '0.0.1'
__desc__ = 'Show the metadata(song, artists, cover) of songs by desktop notifications'

notifier = None 

class Notifier:
  def __init__(self, app):
    self._app = app
    self._notification = Notify.Notification.new('','','')
    Notify.init("FeelUOwn")

  async def popup(self, song):
    if song is None:
      return
    title = song.title_display
    artists_name = song.artists_name_display
    album = song.album

    data = await self._app.img_mgr.get(album.cover, reverse(album, '/cover'))
    loader = GdkPixbuf.PixbufLoader.new()
    loader.write(data)
    loader.close()
    gdk_image = loader.get_pixbuf()
    self._notification.update(title, artists_name)
    self._notification.set_image_from_pixbuf(gdk_image)
    self._notification.show()

  def caller(self, song):
    aio.create_task(self.popup(song))

def enable(app):
  notifier = Notifier(app)
  add_hook('app.player.playlist.song_changed', notifier.caller)

def disable(app):
  rm_hook('app.player.playlist.song_changed', notifier.caller)
