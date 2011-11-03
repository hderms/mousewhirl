import cv
import cProfile
import operator
import mousegui

def draw_features(image, features,size = 4, color = cv.RGB(17,100,255) ): 
    for tup in good_features_to_track:
        cv.Circle(tempframeImg, tuple([int(x) for x in tup]), 4, cv.RGB(17,100,255))  
        
def process_nonzero_count_log(nonzeroCountLog, filename = None):
    print "\n".join(nonzeroCountLog)
    if filename:
        '''TODO: handle filesaving'''
        pass
    
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

def mainloop(nFrames, vidFile, roiImagesAndWindows, roiPrevFrame, roiDifference,roiGrayImg, roiBitImg, frameImg, waitPerFrameInMillisec, features = None, featureImg = None):
    nonzeroCountLog = []
    
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
            nonzeroCountLog.append("%s count of %s is %s percent of frame" % (x[2], count, count/reduce(operator.__mul__, cv.GetSize(roiBitImg[num])) ))
            if features and featureImg:
                draw_features(featureImg,features)
                cv.ShowImage("Good Features", featureImg)
                
            cv.ResetImageROI(frameImg)
            
        cv.ShowImage("Main Window",frameImg)
        #wait for the appropriate time so fps is proper when displaying doubt this takes into account the time it takes to write to screen 
        cv.WaitKey( waitPerFrameInMillisec  )
        
    process_nonzero_count_log(nonzeroCountLog)
    cv.DestroyWindow( "Main Window" )    

if __name__=="__main__":
    """monolithic main conditional for testing purposes
    """
    
    #open videos
    vidfilehandle = raw_input("Enter the path of the video. Just press enter for default:\n")
    vidFile = cv.CaptureFromFile( vidfilehandle or '/home/tarpsocks/mice_videos/mousewhirl/vid.avi' )
    
    
    #define constants:
    numRects = 3
    
    #define video information
    nFrames = int(  cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FRAME_COUNT ) )
    fps = cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FPS )
    waitPerFrameInMillisec = int( 1/fps * 1000/1 )
    width = int(cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FRAME_HEIGHT))
    
    
    
    frameImg = cv.QueryFrame( vidFile )
    
    #setting up data structures: windows
    cv.NamedWindow("Main Window")
    
    #setting up data structures: mousewhirl defined data structures
    ourROIFinder = mousegui.rectangleFinder(frameImg, numRects, dilate_erode_reps = True, box_dragger = True, compute_hough = True, mouse_click_handler = True)
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

    cv.SetMouseCallback("Main Window", lambda x, y, z, u, t: None, None)
    
    tempframeImg = cv.CreateImage(cv.GetSize(frameImg), cv.IPL_DEPTH_8U, 1)
    cv.ConvertImage(frameImg, tempframeImg, cv.IPL_DEPTH_8U)
    goodfeatures = cv.CreateImage(cv.GetSize(frameImg), cv.IPL_DEPTH_32F, 1)
    goodfeatures_temp = cv.CreateImage(cv.GetSize(frameImg), cv.IPL_DEPTH_32F, 1)
    good_features_to_track = cv.GoodFeaturesToTrack(tempframeImg, goodfeatures, goodfeatures_temp, 100, 0.01, 0.01)
    
    cv.ShowImage("Good Features", tempframeImg)
    draw_features(tempframeImg, good_features_to_track)
    mainloop(nFrames, vidFile, roiImagesAndWindows, roiPrevFrame, roiDifference,roiGrayImg, roiBitImg, frameImg, waitPerFrameInMillisec, features = good_features_to_track, featureImg = tempframeImg)



    
