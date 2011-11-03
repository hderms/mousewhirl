import cv
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
        
        
    
