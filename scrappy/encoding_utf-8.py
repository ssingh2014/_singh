
#========================================================================================================================
# ENCODING "utf-8" characters -- Data encoding issue
#========================================================================================================================


def parse(self, response):
  resp_text = unicode(response.body.decode(response.encoding)).encode('utf-8')

  json_data = json.loads(resp_text) # no more errors!

