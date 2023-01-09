from dateutil.parser import parse
import tzlocal
from pytz import timezone

from DataEntryIterator import DataEntryIterator

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def upload_events(events):
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=8080)
        
    try:
        service = build('calendar', 'v3', credentials=creds)
        batch = service.new_batch_http_request()
        for e in events:
            batch.add(service.events().insert(calendarId='primary', body=e))
        batch.execute()

    except HttpError as error:
        print('An error occurred: %s' % error)

def main():
    time_zone = tzlocal.get_localzone_name()

    new_time_zone = input(f'Using time zone {time_zone} -- press enter to accept or input new time zone here: ')
    if new_time_zone != '':
        time_zone = new_time_zone

    pytz_time_zone = timezone(time_zone)

    semester_begins = input(f'Semester begins on: ')
    semester_ends = input(f'Semester ends on: ')

    start_date = pytz_time_zone.localize(parse(semester_begins))
    end_date = pytz_time_zone.localize(parse(semester_ends))

    events = list(DataEntryIterator(start_date, end_date, time_zone))    

    print('\n')
    print(f'Semester begins {str(start_date.date())}')
    print(f'Semester ends {end_date.date()}')
    for e in events:
        print(f'{e.summary} at {e.location} on {e.billiejoe_rep_pattern}')
    print('\n')

    if input('Upload y/n? ').lower() == 'y':
        upload_events(events)
        print('Done!')
    else:
        print('Exiting without uploading.')

if __name__ == '__main__':
    main()