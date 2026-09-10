import easyocr

reader = easyocr.Reader(['en'], gpu=False)
for name in ['police_cctv.mp4', 'municipal_cctv.mp4', 'gsrtc_cctv.mp4', 'health_cctv.mp4', 'panchayat_cctv.mp4']:
    res = reader.readtext(f'crop_{name}.jpg')
    print(f'=== {name} ===')
    for b, t, c in res:
        print(f'  "{t}" (conf: {round(c, 2)})')
