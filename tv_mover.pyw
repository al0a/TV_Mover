from debian.changelog import change
import os
import re
import requests
import argparse
import time
import glob

# Consts
show_reg = '(.{1,100})(?:\.| )S(\d{2})E(\d{2}).{1,200}\.(?:avi|mp4|mkv|m4v)$'
dl_path = 'E:/Downloads/'
mv_path = 'F:/XBMC/TV Shows/'
atv_list = [['10.0.0.5:8080', 'your_user', 'your_password']]


# Helper functions
def _handle_show(old_path, new_path):
    changed = False
    if not os.path.lexists(new_path):
        try:
            os.renames(old_path, new_path)
            changed = True
            print '[OK]'
        except:
            print '[Lock]'
            pass
    else:
        try:
            print '[Dup]'
            os.remove(old_path)
        except:
            pass
    return changed


def _update_xbmc(*atv_list):
    for atv in atv_list:
        url = 'http://%s/jsonrpc?request={ "jsonrpc": "2.0", "method": "VideoLibrary.Scan", "id": "tv_mover"}' % atv[0]
        req = requests.get(url, auth=(atv[1], atv[2]))
        if 'OK' not in req.text:
            url = 'http://%s/xbmcCmds/xbmcHttp?command=ExecBuiltIn&parameter=XBMC.UpdateLibrary(video)' % atv[0]
            req = requests.get(url, auth=(atv[1], atv[2]))
        print 'UpdateLibrary %s %s' % atv[0], ('OK' if ('OK' in req.text) else 'ERROR')


def _remove_torrent_files():
    list = glob.glob("%s*.torrent" % dl_path)
    for f in list:
        try:
            os.remove(f)
        except OSError:
            pass


# Main
def _main(dry, update):
    change_detected = False
    for root, folders, files in os.walk(dl_path):
        for file in files:
            file_name = file
            ro = re.match(show_reg, file_name)
            if ro:
                show = ro.group(1).replace('.', ' ')
                season = ro.group(2)
                episode = ro.group(3)
                if show and season and episode:
                    old_path = os.path.join(root, file)
                    new_path = '%s%s/Season %s/%s' % mv_path, show, season, file_name
                    print 'Moving: %s ---> %s%s/Season %s/' % file_name, mv_path, show, season,
                    if dry == 0:
                        if not change_detected:
                            change_detected = _handle_show(old_path, new_path)
                    else:
                        print '[Dry]'
    _remove_torrent_files()
    if update or change_detected:
        _update_xbmc(*atv_list)
    else:
        print 'No library changes detected.'
    time.sleep(3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Move TV Show files to the correct location and update XBMC libraries.')
    parser.add_argument('--dry', dest='dry', action='store_const', const=1, default=0, help='Shows predicted outcome, does not make changes to the files')
    parser.add_argument('--update', dest='update', action='store_const', const=1, default=0, help='Updates library regardless of the scan result')
    parser.add_argument('--utor', dest='utor', action="store", type=int, default=None, help='Torrent file status when triggering from uTorrent')
    res = parser.parse_args()

    if (not res.utor) or (res.utor == 11):
        _main(res.dry, res.update)
