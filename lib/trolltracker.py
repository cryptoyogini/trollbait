import twython
import xetrapal
def hasmarker(text,markerlist):
	for marker in markerlist:
       if marker in text.lower():
           return marker




class XpalTrollTracker(twython.TwythonStreamer):
    def __init__(self,ofile,markerlist,logger,*args, **kwargs):
        super(XpalTwitterStreamer,self).__init__(*args, **kwargs)
        self.ofile=ofile
        self.buffer=[]
        self.logger=logger
    def flush_buffer(self):
        ofilejson=[]
        if os.path.exists(self.ofile):
            with open(self.ofile,"r") as f:
                ofilejson=json.loads(f.read())
        ofilejson+=self.buffer
        with open(self.ofile,"w") as f:
            f.write(json.dumps(ofilejson))
        self.buffer=[]
    def on_success(self, data):
		self.logger.info(data['full_text'])
        #self.logger.info("Caught troll with marker " + marker)
        self.buffer.append(data)
        if len(self.buffer)>10:
            self.flush_buffer()
    def on_error(self, status_code, data):
        print(status_code)

def get_troll_tracker(config,ofilename=None,logger=xetrapal.astra.baselogger):
    
    if ofilename==None:
        ts=datetime.now()
        ofilename="/tmp/TwythonStreamer-"+ts.strftime("%Y%b%d-%H%M%S"+".json")
    logger.info("Trying to get a twython streamer to work with twitter streams")
    app_key=config.get("Twython",'app_key')
    app_secret=config.get("Twython",'app_secret')
    oauth_token=config.get("Twython",'oauth_token')
    oauth_token_secret=config.get("Twython",'oauth_token_secret')
    try:
        t=XpalTrollTracker(ofilename,logger,app_key,app_secret,oauth_token,oauth_token_secret)
        logger.info("Streamer logging at "  + colored.stylize(t.ofile,colored.fg("yellow")))
        return t
    except Exception as e:
		logger.error("Could not get twython streamer because %s" %repr(e))
		return None
