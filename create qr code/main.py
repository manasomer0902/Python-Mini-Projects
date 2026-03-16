
# How to create qrcode from python

import qrcode
img = qrcode.make('https://www.youtube.com/watch?v=NDDL4OK0gTY')
img.save('myQRcode.png')
img.show()
