import cv
import cProfile

 



def mainloop(nFrames, vidFile, roiImagesAndWindows, roiPrevFrame, roiDifference,roiGrayImg, roiBitImg, frameImg, waitPerFrameInMillisec):
  
    for f in xrange( nFrames ):
        if f == 1000:
            break

        frameImg = cv.QueryFrame( vidFile )
        cv.SetImageROI(frameImg,x[0])
        cv.Copy(x[1], roiPrevFrame[num])
        cv.Copy(frameImg, x[1])
        cv.AbsDiff(x[1], roiPrevFrame[num], roiDifference[num])
        cv.CvtColor(roiDifference[num], roiGrayImg[num], cv.CV_BGR2GRAY)
        cv.Threshold(roiGrayImg[num], roiBitImg[num], 10,255, cv.CV_THRESH_BINARY)
        cv.ShowImage(x[2], roiBitImg[num])
        cv.ResetImageROI(frameImg)
    
        cv.ShowImage("Main Window",frameImg)
        #wait for the appropriate time so fps is proper when displaying doubt this takes into account the time it takes to write to screen 
        cv.WaitKey( waitPerFrameInMillisec  )

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
    #report the chosen rectangles
    print "Our rectangle tuples chosen are as follows: %s" % ourROIFinder.rects
    
    window_count = 0
    frameImg = cv.QueryFrame( vidFile )
    print "frame depth = %s" % frameImg.depth
    for x in cvRects:

        goodfeatures = cv.CreateImage(cv.GetSize(frameImg), frameImg.depth, 3)
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
    mainloop(nFrames, vidFile, roiImagesAndWindows, roiPrevFrame, roiDifference,roiGrayImg, roiBitImg, frameImg, waitPerFrameInMillisec)
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


    
