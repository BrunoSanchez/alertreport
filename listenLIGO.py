# Python standard library imports
import tempfile
import shutil
import sys
import glob

# Third-party imports
import gcn
import gcn.handlers
import gcn.notice_types as ntc
import requests
import healpy as hp
import numpy as np


def sendAlertEmail(voexml_filename):
    import smtplib
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.utils import formatdate, COMMASPACE
    import os

    fromaddr = 'myuser@myserver.com'
    alertRecipients = ['recip01@gmail.com', 'recip02@gmail.com', 'recip03@gmail.com']

    msg = MIMEMultipart()
    msg['Subject'] = "LIGO or Fermi alert"
    msg['From'] = fromaddr
    msg['To'] = COMMASPACE.join(alertRecipients)
    msg['Date'] = formatdate(localtime=True)

    msg_text = "Received a VOEvent (attached) from the GCN-LIGO alert system or Fermi. I can't tell which is which right now.\nSent from NovaIATE machine.\n"
    msg.attach(MIMEText(msg_text))

    with open(voexml_filename, "rb") as voefile:
        msg.attach(MIMEApplication(
            voefile.read(),
            Content_Disposition='attachment; filename="%s"' % os.path.basename(voexml_filename),
            Name=os.path.basename(voexml_filename)
        ))

    # Credentials (if needed)
    username = 'myuser'
    password = 'XXXXXXXXXXX'

    # The actual mail send
    server = smtplib.SMTP('smtp.myserver.com')
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, alertRecipients, msg.as_string())
    server.quit()


#def get_skymap(root):
#    """
#    Look up URL of sky map in VOEvent XML document,
#    download sky map, and parse FITS file.
#    """
#    # Read out URL of sky map.
#    # This will be something like
#    # https://gracedb.ligo.org/apibasic/events/M131141/files/bayestar.fits.gz
#    skymap_url = root.find(
#        "./What/Param[@name='SKYMAP_URL_FITS_BASIC']").attrib['value']
#    print "The Sky Map URL: " + skymap_url
#    # Send HTTP request for sky map
#    response = requests.get(skymap_url, stream=True, auth=('mario.diaz@LIGO.ORG', 'yZKg8m93yGL78UkqjSzt'))
#    # Raise an exception unless the download succeeded (HTTP 200 OK)
#    response.raise_for_status()
#    print response.raw
#    print ("Attempting to write fits")
#    #shutil.copyfileobj(reponse.raw, open('example.fits.gz', 'wb'))
#    #print("Did it write it? Check now.")
#    # Create a temporary file to store the downloaded FITS file
#    with tempfile.NamedTemporaryFile() as tmpfile:
#        # Save the FITS file to the temporary file
#        print("Saving fits to temparary file")
#        shutil.copyfileobj(response.raw, tmpfile)
#        tmpfile.flush()
#        # Uncomment to save FITS payload to file
#        print("Saving fits file to example.fits.gz")
#        shutil.copyfileobj(reponse.raw, open('example.fits.gz', 'wb'))
#        print("Did it write it? Check now.")
#        # Read HEALPix data from the temporary file
#        skymap, header = hp.read_map(tmpfile.name, h=True, verbose=False)
#        header = dict(header)
#    # Done!
#    return skymap, header
#    #return None, None

# Function to call every time a GCN is received.
# Run only for notices of type LVC_INITIAL or LVC_UPDATE.
@gcn.handlers.include_notice_types(
    ntc.LVC_PRELIMINARY,
    ntc.LVC_INITIAL,
    ntc.LVC_UPDATE,
    ntc.LVC_COUNTERPART,
    ntc.FERMI_GBM_ALERT,
    ntc.FERMI_GBM_FLT_POS,
    ntc.FERMI_GBM_GND_POS,
    ntc.FERMI_GBM_LC,
    ntc.FERMI_GBM_GND_INTERNAL,
    ntc.FERMI_GBM_FIN_POS,
    ntc.FERMI_GBM_TRANS,
    ntc.FERMI_GBM_POS_TEST,
    ntc.FERMI_LAT_POS_INI,
    ntc.FERMI_LAT_POS_UPD,
    ntc.FERMI_LAT_POS_DIAG,
    ntc.FERMI_LAT_TRANS,
    ntc.FERMI_LAT_POS_TEST,
    ntc.FERMI_LAT_MONITOR,
    ntc.FERMI_SC_SLEW,
    ntc.FERMI_LAT_GND,
    ntc.FERMI_LAT_OFFLINE,
    ntc.FERMI_POINTDIR)
def process_gcn(payload, root):
    # Print the alert
    #print('Got VOEvent:')
    #print(payload)
    # Uncomment to save VOEvent payload to file
    voevent_filename = 'VOEvent.xml'
    open(voevent_filename, 'w').write(payload)
    sendAlertEmail(voevent_filename)
    # Read out integer notice type (note: not doing anythin with this right now)
    #notice_type = int(root.find("./What/Param[@name='Packet_Type']").attrib['value'])
    # Read sky map
    #skymap, header = get_skymap(root)
    

if __name__ == "__main__":
    # Listen for GCNs until the program is interrupted
    # (killed or interrupted with control-C).
    print("gcn.listen(port=8096, handler=process_gcn)")
    gcn.listen(port=8096, handler=process_gcn)
