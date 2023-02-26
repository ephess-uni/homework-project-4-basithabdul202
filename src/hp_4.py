# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    n=[]
    
    for ba in old_dates:
        
        r = datetime.strptime(ba, "%Y-%m-%d").strftime('%d %b %Y')
        
        n.append(r)
        
    return n


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        
        raise TypeError()
    
    newLsit = []
    
    start_date = datetime.strptime(start, '%Y-%m-%d')
    
    for k in range(n):
        
        newLsit.append(start_date + timedelta(days=k))
        
    return newLsit


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    value1 = len(values)
    value2 = date_range(start_date, value1)
    value3 = list(zip(value2, values))
    return value3


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    headerList = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    
    lastefees = defaultdict(float)
    
    with open(infile, 'r') as f:
        fileData = DictReader(f, fieldnames=headerList)
        allLines = [line for line in fileData]

    allLines.pop(0)
       
    for single in allLines:
       
        p = single['patron_id']
        
        date_due = datetime.strptime(single['date_due'], "%m/%d/%Y")
        
        date_returned = datetime.strptime(single['date_returned'], "%m/%d/%Y")
        
        daysDue = (date_returned - date_due).days
        
        lastefees[p]+= 0.25 * daysDue if daysDue > 0 else 0.0
        
                
    finalIst = [
        {'patron_id': patron, 'late_fees': f'{fee:0.2f}'} for patron, fee in lastefees.items()
    ]
    with open(outfile, 'w') as fout:
        
        writer = DictWriter(fout,['patron_id', 'late_fees'])
        writer.writeheader()
        writer.writerows(finalIst)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
