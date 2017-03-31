import cv2
import numpy as np
def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img_blurred = cv2.GaussianBlur(img_gray, (3, 3), 0)


# wide = cv2.Canny(img_blurred, 10, 200)
# tight = cv2.Canny(img_blurred, 225, 250)
# auto = auto_canny(img_blurred)