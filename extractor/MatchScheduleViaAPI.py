###############################################################################
# Match schedule retrieval for FIRST Robotics FRC using API new for 2015
# Laura Rhodes, March 10, 2015, based on earlier work by William Chargin
#
##############
# INVOCATION #
##############
# The program  can be invoked  from the command  line with two  arguments.
# The first argument is the year of the event,
# the second is the event code,
# the third  is the  name of a  file to  which the  results will  be exported.
# example: python MatchScheduleViaAPI.py 2015 CARM DS.txt
#
# The program can also be invoked without any arguments. In this case, the user
# will be prompted to input the commands directly.
#
##########
# OUTPUT #
##########
# The program exports  the results into a  given file with one match  per line.
# Each line consists of seven comma-separated  numbers. The first number is the
# number of the match in  question. The second  through fourth numbers  are the
# team numbers of  robots in positions  Red 1, Red 2, and Red 3,  respectively.
# The last three numbers are the same as the second through fourth, but for the
# blue team.
#
###############################################################################
import urllib2                 # to get the page HTML code
import urllib                  # to encode url data
import json                    # to parse JSON response
import sys                     # to get the arguments

from time import clock         # for determining how long it took

START_TIME = clock()

filePath = ''


def showUsage():
    print('MatchScheduleViaAPI.py')
    print('Usage: python MatchScheduleViaAPI.py [ <YEAR> , <EVENT>, <FILE> ]')
    print('where: ')
    print('  <YEAR>  is the numeric year of the event.')
    print('  <EVENT>  is the eventCode of the event.')
    print('  <FILE> is the name of a file to which the results will be saved.')
    print('If no arguments are provided, the user will be prompted.')

# The application requires two arguments: a URL and a file location.
if (len(sys.argv) != 4 and len(sys.argv) != 1):  # first is the script location
    # Bad number of arguments.
    showUsage()
    exit(1)
elif len(sys.argv) is 1:  # No arguments; prompt
    print('Match Schedule Formatter for FRC')
    print('Input arguments:')
    year = raw_input('Event Year   = ')
    event = raw_input('Event Code   = ')
    filePath = raw_input('Export file location = ')
else:
    year = sys.argv[1]
    event = sys.argv[2]
    filePath = sys.argv[3]

print('Program begun...')

print('Fetching match data from FIRST...')

values = {'tournamentLevel': 'qual'}
data = urllib.urlencode(values)

url = 'https://frc-api.usfirst.org/api/v1.0/schedule/'
url = url + year + '/' + event + '/'
url = url + '?' + data
req = urllib2.Request(url)

token = 'TGF1cmFSaG9kZXM6YWI4OWY2ODktMDIzNS00OGJlLTkyY2YtYTE2MTE3MWQ2ZjA1'
req.add_header('Authorization', 'Basic ' + token)
req.add_header('Accept', 'application/json')

response = urllib2.urlopen(req)

print('Parsing returned data from FIRST...')
thepage = response.read()  # interpret the response
matchList = json.loads(thepage)  # load the JSON data
matches = matchList['Schedule']  # get the list of matches
print('Match values parsed...')

# Now, we have to write the data to a CSV file.
matchfile = open(filePath, 'w')  # open for write
print('File opened successfully...')

for match in matches:
    matchStations = dict()
    matchData = [match['matchNumber']]
    for team in match['Teams']:
        matchStations[team['station']] = team['teamNumber']

    for s in ['Red1', 'Red2', 'Red3', 'Blue1', 'Blue2', 'Blue3']:
        matchData.append(matchStations[s])

    matchfile.write(','.join(map(str, matchData)))
    matchfile.write('\n')

matchfile.close()
print('Data written successfully...')
print('Done.')

END_TIME = clock()
TIME_TAKEN = END_TIME - START_TIME
print ('*** %d matches written to %s in %f seconds ***'
       % (len(matches), filePath, TIME_TAKEN))
