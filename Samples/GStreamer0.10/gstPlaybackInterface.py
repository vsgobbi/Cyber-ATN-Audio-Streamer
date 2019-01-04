import os
import gst, gtk, gobject

class PlaybackInterface:

	PLAY_IMAGE = gtk.image_new_from_stock(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_BUTTON)
	PAUSE_IMAGE = gtk.image_new_from_stock(gtk.STOCK_MEDIA_PAUSE, gtk.ICON_SIZE_BUTTON)

	def __init__(self):
		self.main_window = gtk.Window()
		self.video_area = gtk.DrawingArea()
		self.play_button = gtk.Button()
		self.info_label = gtk.Label("Not playing")
		self.slider = gtk.HScale()

		self.button_box = gtk.HBox()	
		self.button_box.pack_start(self.play_button, False)
		self.button_box.pack_start(self.info_label, True, True)
		
		self.main_vbox = gtk.VBox(spacing=6)
		self.main_vbox.pack_start(self.video_area, True, True)
		self.main_vbox.pack_start(self.slider, False)
		self.main_vbox.pack_start(self.button_box, False)
		
		self.main_window.add(self.main_vbox)
		self.main_window.connect('destroy', self.on_destroy)
		
		self.video_area.connect('realize', self.on_video_area_realized)
		
		self.play_button.set_image(self.PLAY_IMAGE)
		self.play_button.connect('clicked', self.on_play)

		self.slider.set_range(0, 100)
		self.slider.set_increments(1, 10)
		self.slider.connect('value-changed', self.on_slider_change)
		
		self.main_window.set_border_width(6)
		self.main_window.set_size_request(600, 400)
		
		self.playbin = gst.element_factory_make('playbin2')
		
		#current_dir = os.path.abspath('.')
		current_dir = os.path.abspath('/opt/crat/core/home/sounds/ATC')		
		self.playbin.set_property('uri', 'file://' + os.path.join(current_dir, '301.mp3'))
		#self.playbin.set_property('uri', 'file://' + os.path.join(current_dir, 'Hurricane_Connie_1955.ogg'))
		self.sink = gst.element_factory_make('xvimagesink')
		self.sink.set_property('force-aspect-ratio', True)
		self.playbin.set_property('video-sink', self.sink)

		self.bus = self.playbin.get_bus()
		self.bus.add_signal_watch()

		self.bus.connect("message::eos", self.on_finish)
		
		self.is_playing = False

		self.main_window.show_all()

	def on_finish(self, bus, message):
		self.playbin.set_state(gst.STATE_PAUSED)
		self.play_button.set_image(self.PLAY_IMAGE)
		self.info_label.set_label("Not playing")
		self.is_playing = False
		self.playbin.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, 0)
		self.slider.set_value(0)
		
	def on_destroy(self, window):
		# NULL state allows the pipeline to release resources
		self.playbin.set_state(gst.STATE_NULL)
		self.is_playing = False
		gtk.main_quit()
		
	def on_play(self, button):
		if not self.is_playing:
			self.play_button.set_image(self.PAUSE_IMAGE)
			self.info_label.set_label("Playing")
			self.is_playing = True

			self.playbin.set_state(gst.STATE_PLAYING)
			gobject.timeout_add(100, self.update_slider)

		else:
			self.play_button.set_image(self.PLAY_IMAGE)
			self.info_label.set_label("Paused")
			self.is_playing = False

			self.playbin.set_state(gst.STATE_PAUSED)
		
	def on_slider_change(self, slider):
		seek_time_secs = slider.get_value()
		self.playbin.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_KEY_UNIT, seek_time_secs * gst.SECOND)
		
	def on_video_area_realized(self, video_area):
		self.sink.set_xwindow_id(self.video_area.window.xid)
		
	def update_slider(self):
		if not self.is_playing:
			return False # cancel timeout
		
		try:
			nanosecs, format = self.playbin.query_position(gst.FORMAT_TIME)
			duration_nanosecs, format = self.playbin.query_duration(gst.FORMAT_TIME)
			
			# block seek handler so we don't seek when we set_value()
			self.slider.handler_block_by_func(self.on_slider_change)
			
			self.slider.set_range(0, float(duration_nanosecs) / gst.SECOND)
			self.slider.set_value(float(nanosecs) / gst.SECOND)
			
			self.slider.handler_unblock_by_func(self.on_slider_change)
			
		except gst.QueryError:
			# pipeline must not be ready and does not know position
			pass
			
		return True # continue calling every 30 milliseconds
		

if __name__ == "__main__":
	PlaybackInterface()
	gtk.main()

