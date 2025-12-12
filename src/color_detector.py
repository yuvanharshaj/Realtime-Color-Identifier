import cv2
import numpy as np
import pandas as pd
from math import sqrt

# Load dataset
color_data = pd.read_csv("data/color_data.csv")

# ===== ΔE2000 Color Difference (High Accuracy Formula) =====
# Formula from CIE standard
def deltaE2000(Lab1, Lab2):
    L1, a1, b1 = Lab1
    L2, a2, b2 = Lab2

    avg_L = (L1 + L2) / 2.0
    C1 = sqrt(a1*a1 + b1*b1)
    C2 = sqrt(a2*a2 + b2*b2)
    avg_C = (C1 + C2) / 2.0

    G = 0.5 * (1 - sqrt((avg_C**7) / (avg_C**7 + 25**7)))
    a1p = (1 + G) * a1
    a2p = (1 + G) * a2

    C1p = sqrt(a1p*a1p + b1*b1)
    C2p = sqrt(a2p*a2p + b2*b2)
    avg_Cp = (C1p + C2p) / 2.0

    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360

    deltahp = h2p - h1p
    if deltahp > 180:
        deltahp -= 360
    elif deltahp < -180:
        deltahp += 360
    if C1p * C2p == 0:
        deltahp = 0

    deltaLp = L2 - L1
    deltaCp = C2p - C1p
    deltaHp = 2 * sqrt(C1p * C2p) * np.sin(np.radians(deltahp) / 2)

    avg_Lp = (L1 + L2) / 2.0
    avg_hp = (h1p + h2p) / 2.0
    if abs(h1p - h2p) > 180:
        avg_hp += 180
    if C1p * C2p == 0:
        avg_hp = h1p + h2p

    T = (1
         - 0.17 * np.cos(np.radians(avg_hp - 30))
         + 0.24 * np.cos(np.radians(2 * avg_hp))
         + 0.32 * np.cos(np.radians(3 * avg_hp + 6))
         - 0.20 * np.cos(np.radians(4 * avg_hp - 63)))

    Sl = 1 + (0.015 * (avg_Lp - 50) ** 2) / sqrt(20 + (avg_Lp - 50) ** 2)
    Sc = 1 + 0.045 * avg_Cp
    Sh = 1 + 0.015 * avg_Cp * T

    deltaTheta = 30 * np.exp(-((avg_hp - 275) / 25) ** 2)
    Rc = 2 * sqrt((avg_Cp**7) / (avg_Cp**7 + 25**7))
    Rt = -Rc * np.sin(np.radians(2 * deltaTheta))

    return sqrt(
        (deltaLp / Sl) ** 2 +
        (deltaCp / Sc) ** 2 +
        (deltaHp / Sh) ** 2 +
        Rt * (deltaCp / Sc) * (deltaHp / Sh)
    )


# Convert dataset to LAB
dataset_lab = []
for i in range(len(color_data)):
    bgr = np.uint8([[[color_data.iloc[i]["B"], color_data.iloc[i]["G"], color_data.iloc[i]["R"]]]])
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)[0][0]
    dataset_lab.append((color_data.iloc[i]["color_name"], lab))


# Find closest color using ΔE2000
def closest_color_name(lab_color):
    best = ("Unknown", float("inf"))
    for name, sample_lab in dataset_lab:
        dE = deltaE2000(lab_color, sample_lab)
        if dE < best[1]:
            best = (name, dE)
    return best[1], best[0]


def main():
    cap = cv2.VideoCapture(0)
    win = "Real-Time Color Detection"

    if not cap.isOpened():
        print("Camera error")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        cx, cy = w // 2, h // 2

        box = 8
        region = frame[cy-box:cy+box, cx-box:cx+box]

        avg_bgr = np.mean(region, axis=(0, 1)).astype(np.uint8)
        b, g, r = avg_bgr

        lab = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2LAB)[0][0]

        diff, cname = closest_color_name(lab)
        label = f"{cname}  ({r},{g},{b})"

        cv2.circle(frame, (25, 30), 10, (int(b), int(g), int(r)), -1)

        cv2.putText(frame, label, (50, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (255, 255, 255), 2)

        cv2.rectangle(frame, (cx-box, cy-box), (cx+box, cy+box),
                      (0, 255, 0), 1)

        # ===== FIXED WINDOW CLOSING =====
        try:
            cv2.imshow(win, frame)
        except:
            break

        key = cv2.waitKey(1)

        # If X button clicked, window disappears → break
        # Safe X-button close check
        try:
            if cv2.getWindowImageRect(win)[0] < 0:
                break
        except:
            break

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
