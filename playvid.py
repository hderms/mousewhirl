import cv
#open videos
vidFile = cv.CaptureFromFile( '/home/tarpsocks/mice_videos/vid.avi' )

backgroundFile = cv.CaptureFromFile( '/home/tarpsocks/mice_videos/background.avi' )

#define constants
nFrames = int(  cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FRAME_COUNT ) )
fps = cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FPS )
waitPerFrameInMillisec = int( 1/fps * 1000/1 )
width = int(cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FRAME_WIDTH))
height = int(cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FRAME_HEIGHT))

background_fps = cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FPS)
background_WaitPerFrameInMillisec = int(1/fps * 1000/1)


print 'Num. Frames = ', nFrames
print 'Frame Rate = ', fps, ' frames per sec'

#definition of class that is used to find ROIs for copying out the cages
class rectangleFinder(object):
	def __init__(self, frameImg, dilate_erode_reps = None, compute_hough= None, mouse_click_handler = None):
		self.frameImg = frameImg
		self.message = "Debug"
		if compute_hough:
			self.rectangular_image = self.compute_hough(frameImg)
		if mouse_click_handler:
			cv.SetMouseCallback("Main Window", self.handle_mouseclick, None)
	def compute_hough(self, frameImg):
		pass
	def find_roi(self, houghImg):
		pass
	def handle_mouseclick(self, event, x, y, flags, param):
		print self.message
		print x, y
	
#preliminary fetching of images

frameImg = cv.QueryFrame( vidFile )
background_img = cv.QueryFrame(backgroundFile)

#fetch a few extra to make sure the frame is representative
for x in xrange(3):
	background_img = cv.QueryFrame(backgroundFile)
#setting up data structures: windows
cv.NamedWindow("Main Window")
#setting up data structures: mousewhirl defined data structures
ourROIFinder = rectangleFinder(frameImg, dilate_erode_reps = True, compute_hough = True, mouse_click_handler = True)

#setting up data structures: image buffers
blurred_frame = cv.CreateImage(cv.GetSize(frameImg), cv.IPL_DEPTH_8U, 3)
grayscale_frame = cv.CreateImage(cv.GetSize(blurred_frame), frameImg.depth, 1)
bitImg = cv.CreateImage(cv.GetSize(frameImg), frameImg.depth, 1)
differenceImg = cv.CreateImage(cv.GetSize(frameImg), frameImg.depth, 3)
writtenImg = cv.CreateImage(cv.GetSize(frameImg), frameImg.depth, 3)
#setting up data structures: video writers
video_writer = cv.CreateVideoWriter("bitImage.avi", cv.CV_FOURCC('I', '4', '2', '0'), fps, cv.GetSize(frameImg), 1)
video_difference = cv.CreateVideoWriter("difference.avi", cv.CV_FOURCC('I','4','2', '0'), fps, cv.GetSize(frameImg),1)
#prematurely halt after 1000 frames for testing purposes.
for f in xrange( nFrames ):
  if f == 1000:
     break

  frameImg = cv.QueryFrame( vidFile )
  
  cv.ShowImage( "Main Window",  frameImg )
  #wait for the appropriate time so fps is proper when displaying doubt this takes into account the time it takes to write to screen 
  cv.WaitKey( waitPerFrameInMillisec  )
   
  cv.AbsDiff( background_img, frameImg, differenceImg ) 
  cv.CvtColor(differenceImg,grayscale_frame, cv.CV_BGR2GRAY) 
  cv.Threshold(grayscale_frame,bitImg,15,255,cv.CV_THRESH_BINARY)
  cv.Erode(bitImg,bitImg, iterations=2)
  cv.Dilate(bitImg, bitImg, iterations=1)

  cv.ShowImage("Processed",bitImg)
  cv.CvtColor(bitImg, writtenImg, cv.CV_GRAY2BGR)
  cv.WriteFrame(video_writer, writtenImg)
  cv.WriteFrame(video_difference, differenceImg)
# When playing is done, delete the window
#  NOTE: this step is not strictly necessary, 
#         when the script terminates it will close all windows it owns anyways
cv.ReleaseVideoWriter(video_writer)
cv.DestroyWindow( "Main Window" )
