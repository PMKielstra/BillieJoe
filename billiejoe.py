from dateutil.parser import parse
import tzlocal

from DataEntryIterator import DataEntryIterator

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

TIME_ZONE = tzlocal.get_localzone_name()

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
    new_time_zone = input(f'Using time zone {TIME_ZONE} -- press enter to accept or input new time zone here: ')
    if new_time_zone != '':
        TIME_ZONE = new_time_zone

    semester_begins = input(f'Semester begins on: ')
    semester_ends = input(f'Semester ends on: ')

    start_date = parse(semester_begins + ' ' + TIME_ZONE)
    end_date = parse(semester_ends + ' ' + TIME_ZONE)

    events = list(DataEntryIterator(start_date, end_date, TIME_ZONE))    

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