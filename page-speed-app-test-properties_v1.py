import requests
import json
import datetime
import pandas as pd
import numpy as np

# here's a how it works:
# 1. wrap up a callback object for api
# 2. request a response
# 3. filter & transform data in final form
# 4. decode response's content and parse into json, then turn json to dict objects and then dicts into a list of dicts
# 5. turn dict objects into dataframe
# 6. display data on cli for verification, optionally

# pagespeed api to call
API_URL = 'https://www.googleapis.com/pagespeedonline/v2/runPagespeed?' 
# user credentials
api_key = 'yourapikeygoeshere'

# call properties aka list of urls from a csv file here
properties = pd.read_csv('filename.csv')
properties = properties['URL']
def main():  
  insightstrategy = 'desktop' #insight strategy can only be either 'desktop' or 'mobile'
  dataList = [] #empty list
  timestamp = str(datetime.datetime.now()).split(' ')
  print "Pagespeed api initiated on", timestamp[0]
  for input_url in properties[:10]: #limited to 10 for test purposes
    print "Now fetching PageSpeed Insights for {} with strategy set to {}".format(input_url, insightstrategy)
    try:
      requestUrl = runPageSpeed(input_url, api_key, API_URL, insightstrategy)
      response = requests.get(requestUrl)
      responseContent = response.content # get the actual content of the request made to the runPagespeed method
      # optionally: to check the header of your request. important in helping understand the kind of incoming request
      # headerContent = response.headers
      responseContent = json.loads(responseContent) # print responseContent
      dataList.append(response_cleanup(responseContent, insightstrategy, input_url, timestamp))
    except Exception as e:
      print "Exception incurred: ", e, input_url
  final_dataframe = pd.DataFrame(dataList)
  final_dataframe.to_csv('pagespeed-scores-report-'+insightstrategy+timestamp[0]+'.csv', encoding='utf-8')
  print "New report generated and saved"
  

# executing runPagespeed api 
def runPageSpeed(input_url, api_key, API_URL, insightstrategy):
  query = [
    'url=' + input_url,'filter_third_party_resources=true',
    'key='+api_key, 'strategy='+insightstrategy]
   #check appropriate python join function
  src = API_URL + '&'.join(query)
  return src

# take incoming pagespeed response's content in json and clean it up into a list of dictionaries
def response_cleanup(responseContent, insightstrategy, input_url, timestamp):
  # now slice up pagespeed data to capture relevant data of your choice
  pageTitle, ruleGroups, pageStats, pageId, responseCode = responseContent['title'], responseContent['ruleGroups']['SPEED']['score'], responseContent['pageStats'], responseContent['id'], responseContent['responseCode']
  output_data_format = {'pageTitle': pageTitle, 
                        'pageId': pageId, 
                        'httpResponseCode': responseCode, 
                        'googlePageSpeedScore': ruleGroups,
                        'insightStrategyType': insightstrategy, 
                        'site': input_url, 
                        'DOY': timestamp[0], 
                        'timeOfDay': timestamp[1]}
  for items in pageStats:
    get_key_val = {items: pageStats[items]}
    output_data_format.update(get_key_val)
  return output_data_format



if __name__ == '__main__':
  main()


# sample documentation
#
# for testing with a sample of 100 data
# for items in properties[:100]:
#   print "this is item", items
