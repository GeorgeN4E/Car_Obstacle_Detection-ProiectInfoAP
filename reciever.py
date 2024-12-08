import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

def main():
    # Initialize GStreamer
    Gst.init(None)

    # Create the pipeline
    pipeline = Gst.parse_launch(
        "udpsrc port=9000 caps=application/x-rtp,media=video,clock-rate=90000,encoding-name=H264 ! "
        "rtph264depay ! avdec_h264 ! videoconvert ! autovideosink"
    )

    # Start playing
    pipeline.set_state(Gst.State.PLAYING)

    # Run the main loop
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        print("Exiting...")

    # Stop the pipeline
   
