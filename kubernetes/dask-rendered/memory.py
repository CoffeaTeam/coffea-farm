import ctypes
from distributed import Client
from distributed.utils import format_bytes


def getmallinfo():
    class MallInfo(ctypes.Structure):
        _fields_ = [(name, ctypes.c_int)
                    for name in ('arena', 'ordblks', 'smblks', 'hblks', 'hblkhd',
                                'usmblks', 'fsmblks', 'uordblks', 'fordblks',
                                'keepcost')]

    libc = ctypes.CDLL("libc.so.6")
    mallinfo = libc.mallinfo
    mallinfo.argtypes = []
    mallinfo.restype = MallInfo
    mi = mallinfo()
    otext = ''
    otext += ("Total non-mmapped bytes (arena):       %s\n" % format_bytes(mi.arena))
    otext += ("# of free chunks (ordblks):            %d\n" % (mi.ordblks))
    otext += ("# of free fastbin blocks (smblks):     %d\n" % (mi.smblks))
    otext += ("# of mapped regions (hblks):           %d\n" % (mi.hblks))
    otext += ("Bytes in mapped regions (hblkhd):      %s\n" % format_bytes(mi.hblkhd))
    otext += ("Max. total allocated space (usmblks):  %s\n" % format_bytes(mi.usmblks))
    otext += ("Free bytes held in fastbins (fsmblks): %s\n" % format_bytes(mi.fsmblks))
    otext += ("Total allocated space (uordblks):      %s\n" % format_bytes(mi.uordblks))
    otext += ("Total free space (fordblks):           %s\n" % format_bytes(mi.fordblks))
    otext += ("Topmost releasable block (keepcost):   %s\n" % format_bytes(mi.keepcost))
    return otext


client = Client('coffea-dask.fnal.gov:8786')
out = client.run(getmallinfo)
for k, v in out.items():
    print('-'*50)
    print(k)
    print(v)
