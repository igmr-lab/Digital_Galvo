import numpy as np

from vortex import Range
from vortex.engine import Source
from vortex.scan import RasterScanConfig, FreeformScanConfig, FreeformScan, limits

scan_dimension=1
bidirectional=False
ascans_per_bscan= 512
bscans_per_volume= 512

swept_source=Source(100_000, 1376, 0.5)

rsc = RasterScanConfig()
rsc.bscan_extent = Range(-scan_dimension, scan_dimension)
rsc.volume_extent = Range(-scan_dimension, scan_dimension)
rsc.bscans_per_volume = bscans_per_volume
rsc.bidirectional_segments = bidirectional
rsc.bidirectional_volumes = bidirectional
rsc.limits = [limits.ScannerMax_Saturn_5B]*2
rsc.samples_per_second = swept_source.triggers_per_second

pattern = rsc.to_segments()

ffsc = FreeformScanConfig()
ffsc.pattern = pattern
ffsc.loop = True

scan = FreeformScan()
scan.initialize(ffsc)
data = scan.scan_buffer()

#Write the data points of the scan pattern into a txt file
d = open('EnginePattern_raster_amp1_res512.txt', 'w+')
print(*data, file = d)
d.close()
np.save('EnginePattern_raster_amp1_res512.npy', data)

datapoints = data
lin_length = len(datapoints)

SCALE_FACTOR = 15

#Original
def ang_to_pos(ang):
    if abs(ang) >= SCALE_FACTOR:
        raise Exception("Magnitude of Angle Exceeds Scale Factor")
    pos  = (ang  / SCALE_FACTOR) * 32768 + 32768
    pos = round(pos)
    return pos

def pos_to_ang(pos):
    if pos > 65535 or pos < 0:
        raise Exception("Value of Position Exceeds 2^16 - 1")
    ang = ((pos - 32768) / 32768) * SCALE_FACTOR
    return ang

f = open('EnginePattern_raster_amp1_res512_hexadecimal_downsample.txt', 'w+')
for j in range(0, 1):
    for i in range(0, len(datapoints)):
        pointX = datapoints[i][0]
        hexaX = hex(ang_to_pos(pointX))
        hexaX = hexaX[2:]
        pointY = datapoints[i][1]
        hexaY = hex(ang_to_pos(pointY))
        hexaY = hexaY[2:]
        if(i % 4 == 0):
            print(hexaX + hexaY, file = f)
            # print(i/4)
print((i+1) // 4 // 32)
f.close()
