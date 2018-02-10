import cv2
import numpy as np
import sys

def nothing(x):
    pass


def bboxes():
        filename = sys.argv[1]

        name='Boxer'
        cv2.namedWindow(name)
        # cv2.resizeWindow(name, 800,600)
        cv2.moveWindow(name, 100,960)
        img=cv2.imread(filename)
        #blr=cv2.blur(img, (5,5))

        cv2.createTrackbar('blur',name,0,5,nothing)
        cv2.createTrackbar('sig_space',name,0,120,nothing)
        cv2.createTrackbar('sig_color',name,0,120,nothing)
        cv2.createTrackbar('canny',name,0,100,nothing)

        #flags
        fancy=0
        org=0
        draw=0
        can=1

        #vars
        b=1
        ss=20
        sc=20
        t=50
        #index
        idx=0

        while(1):
            if fancy:
                blr=cv2.bilateralFilter(img,b,ss,sc)
            else:
                blr=cv2.blur(img,(b,b))

            if can:
                binary=cv2.Canny(blr,t,3*t)
            else:
                gray=cv2.cvtColor(blr, cv2.COLOR_BGR2GRAY)
                (t, binary) = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY_INV)

            m2, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if org:
                out=img.copy()
            else:
                out=cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

            if draw:
                c=contours[idx]
                cv2.drawContours(out, contours,-1, (0,255,0), 3)
                cv2.drawContours(out, [c],0, (0,0,255), 3)
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(out, (x, y), (x + w, y + h), (255, 200, 100),  2, 1)
                if len(c) >= 5:
                    ellipse = cv2.fitEllipse(c)
                    cv2.ellipse(out,ellipse,(0,255,255),2)
                # Rotated box
                # rect = cv.minAreaRect(cnt)
                # box = cv.boxPoints(rect)
                # box = np.int0(box)
                # cv.drawContours(img,[box],0,(0,0,255),2)
            cv2.imshow(name, out)

            k = cv2.waitKey(1) & 0xFF

            if k == ord('x'):
                break
            elif k == ord('b'):
                fancy^=1
                print("fancy blur: " + str(fancy))

            elif k == ord('v'):
                org^=1
                print("showing original img:" + str(org))

            elif k == ord('c'):
                draw^=1
                print("drawing contours: " + str(draw))

            elif k == ord('m'):
                can^=1
                print("canny vs threshold: " + str(can))

            elif k == ord('a'):
                idx=(idx+1)%len(contours)
                print("Drawing ROI #" + str(idx))



            b = 2*cv2.getTrackbarPos('blur',name)+1
            ss = cv2.getTrackbarPos('sig_space', name)
            sc = cv2.getTrackbarPos('sig_color', name)
            t = cv2.getTrackbarPos('canny', name)

#def main():

        cv2.destroyAllWindows()


if __name__ == '__main__':
    sys.exit(bboxes())
