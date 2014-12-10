import sys,os,re
import pickle
import ScanPlate
import GetLatLon
import tempfile
import PIL
import pika
import redis

def imageType(filename):
    try:
        i=PIL.Image.open(filename)
        return i.format
    except IOError:
        return False

hostname= os.environ['RABBIT_HOST'] if 'RABBIT_HOST' in os.environ else '172.31.6.6'

redisByChecksum = redis.Redis(host='172.31.5.5', db=1)
redisByName = redis.Redis(host='172.31.5.5', db=2)
redisMD5ByLicense = redis.Redis(host='172.31.5.5', db=3)
redisNameByLicense = redis.Redis(host='172.31.5.5', db=4)

###
# Modify the basic worker outline you've been provided to take license tags returned by 
# OpenALPR and put them into the redisByChecksum and redisByName database. You should first 
# check if the license is already in the database -- don't just add it blindly. 
# You should also add the MD5 hash of the image to the redisByLicense database.
###


def photoInfo(pickled):
    #
    # You can print it out, but it is very long
    print "pickled item is ", len(pickled),"bytes"
    unpickled = pickle.loads(pickled)
    print "File name was", unpickled[0], "digest is ", unpickled[1]
    photoFile,photoName = tempfile.mkstemp("photo")
    os.write(photoFile, unpickled[2])
    os.close(photoFile)
    newPhotoName = photoName + '.' + imageType(photoName)
    os.rename(photoName, newPhotoName)
    print "Wrote it to ", newPhotoName
    plate = ScanPlate.getLikelyLicense( newPhotoName )
    geotag = GetLatLon.getLatLon( newPhotoName )
    if len(plate) > 0:
        pushToRedis(plate, geotag, unpickled[0], unpickled[1])
    os.remove(newPhotoName)

def pushToRedis(plate, geotag, photoName, md5):
    # Found a license plate at this point.
    # Remove preceeding '/tmp/'
    cleanName = re.sub('\/tmp\/', '', photoName)
    #
    ## Consider locking the db
    #
    if redisByChecksum.llen(md5) == 0:
        print 'Inserting', md5, 'into redisByChecksum and redisMD5ByLicense'
        for p in plate:
            redisByChecksum.lpush(md5, p[0])
            redisMD5ByLicense.lpush(p[0], md5)

    if redisByName.llen(cleanName) == 0:
        print 'Inserting', cleanName, 'into redisByName and redisNameByLicense'
        for p in plate:
            redisByName.lpush(cleanName, p[0])
            redisNameByLicense.lpush(p[0], cleanName)

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=hostname))
channel = connection.channel()

channel.exchange_declare(exchange='scanners',type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='scanners',queue=queue_name)

print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
    photoInfo(body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
