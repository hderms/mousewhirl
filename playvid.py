import cv
import cProfile
import operator
 


def convert_to_cvrect(rect):
    #assumes that these are non-rotated rectangles (all lines are perpendicular to axes of graph)
    pt1 = rect[0]
    pt2 = rect[1]
    pt3 = tuple([pt1[0], pt2[1]])
    pt4 = tuple([pt2[0], pt1[1]])
    regular = [pt1, pt2, pt3, pt4]
    minimum_pt = reduce(lambda a, b: a if a[0] <= b[0] and a[1] <= b[1]  else b, regular ) 
    maximum_pt = reduce(lambda a,b: a if a[0] >= b[0] and a[1] >= b[1] else b, regular)
    width = maximum_pt[0] - minimum_pt[0]
    height = maximum_pt[1] - minimum_pt[1]
    return (minimum_pt[0], minimum_pt[1], width, height)

class rectangleFinder(object):


    #definition of class that is used to find ROIs for copying out the cages
    
    def __init__(self, frameImg,numberOfRects, dilate_erode_reps = None,box_dragger = None, compute_hough= None, mouse_click_handler = None):
        self.baseImg = cv.CreateImage(cv.GetSize(frameImg), frameImg.depth, 3)
        cv.Copy(frameImg, self.baseImg) 
        self.frameImg = frameImg
        self.rectColor = cv.Scalar(1,255,1,1)
        self.message = "Debug"
        self.statusText = None
        self.previousCode = None
        self.rects = []
        self.font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1.0, 1.0)
        if box_dragger:
            self.box_dragger = box_dragger
            self.previousXY= None
            self.boxPoints = []    
        else:
            self.box_dragger = None
        if mouse_click_handler:
            cv.SetMouseCallback("Main Window", self.handle_mouseclick, None)
        #holds tuples of box dimensions
        cv.ShowImage("Main Window", self.frameImg)
        self._keyboard_handler(cv.WaitKey(0))    
        if compute_hough:
            self.houghImg = True 
            
    def compute_hough(self, frameImg):
        pass
    
    def find_roi(self, houghImg):
        pass
    
    def handle_mouseclick(self, event, x, y, flags, param):
        if self.box_dragger and event == cv.CV_EVENT_LBUTTONDOWN: 
            if self.previousXY:
                self.rects.append(((x,y), self.previousXY))
                self.previousXY = None
                        
            else:
                self.previousXY = (x,y)
            
            self.update_frame()
            
    def draw_rectangles(self):
        for rect in self.rects:
            cv.Rectangle(self.frameImg, rect[0], rect[1], self.rectColor)
            
    def update_frame(self):
        cv.Copy(self.baseImg, self.frameImg)
        self.draw_rectangles()
        self.draw_text()
        cv.ShowImage("Main Window", self.frameImg)

        self._keyboard_handler(cv.WaitKey())            
        
    def draw_text(self):
        if self.statusText:
            if self.statusTimeout > 0:
                self._put_text(self.statusText)
                self.statusTimeout -= 1
            elif self.statusTimeout == 0 :
                self.statusText = None    
                
    def _keyboard_handler(self,code):
        if code == 65288:
            print "delete"    
            self.statusText = "deleted"
            self.statusTimeout =  1
            if self.rects:
                self.rects.pop()
            else:
                self.statusText = "Can't delete empty rectangle"
        elif code == 10:
            print "enter"
            if self.previousCode == 10:
                print "done"
                return self.rects 
            else:
                print "not done"
                self.statusText = "if finished press enter again"
                self.previousCode = 10
            self.statusTimeout = 1
        elif code == 27:
            print "quit"
            exit()
        else:
            print code
            self.update_frame()
            return
        self.previousCode = code
        self.update_frame()
    def _put_text(self,text):
        cv.PutText(self.frameImg, text, (30,40),self.font, cv.Scalar(5,255,5,5))
def mainloop(nFrames, vidFile, roiImagesAndWindows, roiPrevFrame, roiDifference,roiGrayImg, roiBitImg, frameImg, waitPerFrameInMillisec, features = None, featureImg = None):
    log = []
    for f in xrange( nFrames ):
        if f == 1000:
            break
        features2 = []
        frameImg = cv.QueryFrame( vidFile )
        for num, x in enumerate(roiImagesAndWindows):
            cv.ConvertImage(frameImg, featureImg, cv.IPL_DEPTH_8U)
            cv.SetImageROI(frameImg,x[0])
            cv.Copy(x[1], roiPrevFrame[num])
            cv.Copy(frameImg, x[1])
            cv.AbsDiff(x[1], roiPrevFrame[num], roiDifference[num])
            cv.CvtColor(roiDifference[num], roiGrayImg[num], cv.CV_BGR2GRAY)
            cv.Threshold(roiGrayImg[num], roiBitImg[num], 10,255, cv.CV_THRESH_BINARY)
            cv.ShowImage(x[2], roiBitImg[num])
            count = cv.CountNonZero(roiBitImg[num])
            log.append("%s count of %s is %s percent of frame" % (x[2], count, count/reduce(operator.__mul__, cv.GetSize(roiBitImg[num])) ))
            if features and featureImg:
				for tup in features:
					cv.Circle(featureImg, tuple([int(x) for x in tup]), 4, cv.RGB(17,100,255))			
				cv.ShowImage("Good Features", featureImg)
				
            cv.ResetImageROI(frameImg)
    
        cv.ShowImage("Main Window",frameImg)
            #wait for the appropriate time so fps is proper when displaying doubt this takes into account the time it takes to write to screen 
        cv.WaitKey( waitPerFrameInMillisec  )
    print "\n".join(log)
    cv.DestroyWindow( "Main Window" )       
if __name__=="__main__":
    """monolithic main conditional for testing purposes
    TODO: refactor into appropriate class
    """
    
    #open videos
    vidFile = cv.CaptureFromFile( '/home/tarpsocks/mice_videos/mousewhirl/vid.avi' )
    
    backgroundFile = cv.CaptureFromFile( '/home/tarpsocks/mice_videos/mousewhirl/background.avi' )
    
    #define constants:
    numRects = 3
    
    #define video information
    nFrames = int(  cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FRAME_COUNT ) )
    fps = cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FPS )
    waitPerFrameInMillisec = int( 1/fps * 1000/1 )
    width = int(cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FRAME_HEIGHT))
    
    background_fps = cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FPS)
    background_WaitPerFrameInMillisec = int(1/fps * 1000/1)
    
    
    
    frameImg = cv.QueryFrame( vidFile )
    background_img = cv.QueryFrame(backgroundFile)
    
    #fetch a few extra to make sure the frame is representative
    for x in xrange(3):
        background_img = cv.QueryFrame(backgroundFile)
    #setting up data structures: windows
    cv.NamedWindow("Main Window")
    
    #setting up data structures: mousewhirl defined data structures
    ourROIFinder = rectangleFinder(frameImg, numRects, dilate_erode_reps = True, box_dragger = True, compute_hough = True, mouse_click_handler = True)
    #report the chosen rectangles
    print "Our rectangle tuples chosen are as follows: %s" % ourROIFinder.rects
    
    cvRects = [convert_to_cvrect(rect) for rect in ourROIFinder.rects]
    roiImagesAndWindows = []
    roiPrevFrame = []
    roiDifference = []
    roiBitImg = []
    roiGrayImg = []
    window_count = 0
    frameImg = cv.QueryFrame( vidFile )
    print "total pixels is %s" %reduce(operator.__mul__, cv.GetSize(frameImg))
    for x in cvRects:
        cv.SetImageROI(frameImg, x)
        prev_frame = cv.CreateImage(cv.GetSize(frameImg), frameImg.depth, 3)
        newmg = cv.CreateImage(cv.GetSize(frameImg), frameImg.depth, 3)
        difference = cv.CreateImage(cv.GetSize(frameImg), frameImg.depth, 3)
        bitImg = cv.CreateImage(cv.GetSize(frameImg), frameImg.depth, 1)
        grayImg = cv.CreateImage(cv.GetSize(frameImg), frameImg.depth, 1)
        newWindow = cv.NamedWindow("ROI %s" % window_count)
        roiImagesAndWindows.append((x, newmg, "ROI %s" %window_count))
        cv.Copy(frameImg, prev_frame)
        cv.Copy(frameImg, newmg)
        roiPrevFrame.append(prev_frame)
        roiDifference.append(difference)
        roiGrayImg.append(grayImg)
        roiBitImg.append(bitImg)
        cv.ResetImageROI(frameImg)
        window_count += 1
        
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
    cv.SetMouseCallback("Main Window", lambda x, y, z, u, t: None, None)
    
    tempframeImg = cv.CreateImage(cv.GetSize(frameImg), cv.IPL_DEPTH_8U, 1)
    cv.ConvertImage(frameImg, tempframeImg, cv.IPL_DEPTH_8U)
    goodfeatures = cv.CreateImage(cv.GetSize(frameImg), cv.IPL_DEPTH_32F, 1)
    goodfeatures_temp = cv.CreateImage(cv.GetSize(frameImg), cv.IPL_DEPTH_32F, 1)
    good_features_to_track = cv.GoodFeaturesToTrack(tempframeImg, goodfeatures, goodfeatures_temp, 100, 0.01, 0.01)
    for tup in good_features_to_track:
        cv.Circle(tempframeImg, tuple([int(x) for x in tup]), 4, cv.RGB(17,100,255))
    cv.ShowImage("Good Features", tempframeImg)

    mainloop(nFrames, vidFile, roiImagesAndWindows, roiPrevFrame, roiDifference,roiGrayImg, roiBitImg, frameImg, waitPerFrameInMillisec, features = good_features_to_track, featureImg = tempframeImg)
""" 
      cv.AbsDiff( background_img, frameImg, differenceImg ) 
      cv.CvtColor(differenceImg,grayscale_frame, cv.CV_BGR2GRAY) 
      cv.Threshold(grayscale_frame,bitImg,15,255,cv.CV_THRESH_BINARY)
      cv.Erode(bitImg,bitImg, iterations=2)
      cv.Dilate(bitImg, bitImg, iterations=1)
    
      cv.ShowImage("Processed",bitImg)
      cv.CvtColor(bitImg, writtenImg, cv.CV_GRAY2BGR)
      cv.WriteFrame(video_writer, writtenImg)
      cv.WriteFrame(video_difference, differenceImg)
    """


    
