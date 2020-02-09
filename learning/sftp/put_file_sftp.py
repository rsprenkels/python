import pysftp
import netrc
import glob

FTP_SERVER = '77.64.250.147'
secrets = netrc.netrc()
username, account, password = secrets.authenticators(FTP_SERVER)

srv = pysftp.Connection(host=FTP_SERVER, username=username, password=password, log="./pysftp.log")

with srv.cd('incoming'):
    file_mask = 'tes*.txt'
    matching_files = glob.glob(file_mask)
    if matching_files:
        the_file = matching_files[0]
        print("transferring file: " + the_file)
    else:
        print("no matches for " + file_mask)
    # srv.put(file_mask)
    # data = srv.listdir()

srv.close()

