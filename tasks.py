# necessary imports

import pandas as pd
from tabulate import tabulate

# list of tasks represented as dictionaries -> list of dictionaries each containing the required attributes for a task
somtos_tasks = [
    {
        'id': 0,
        'description': 'Brush teeth',
        'duration': 30,
        'dependencies': [11]
    },
    {
        'id': 1,
        'description': 'CS110 @ 5AM',
        'duration': 120,
        'dependencies': [],
        'time': 5
    },
    {
        'id': 2,
        'description': 'Eat cereal',
        'duration': 30,
        'dependencies': [0]
    },
    {
        'id': 3,
        'description': 'CS111 PCW',
        'duration': 120,
        'dependencies': [2]
    },
    {
        'id': 4,
        'description': 'Read Times Article about disappeared',
        'duration': 60,
        'dependencies': [1, 3]
    },
    {
        'id': 5,
        'description': 'Prepare Lunch',
        'duration': 30,
        'dependencies': [1, 9]
    },
    {
        'id': 6,
        'description': 'Take bus to Memorial Park',
        'duration': 30,
        'dependencies': [8]
    },
    {
        'id': 7,
        'description': 'Memorial Park Tour @ 4pm',
        'duration': 150,
        'dependencies': [6],
        'time': 16
    },
    {
        'id': 8,
        'description': 'Eat Lunch',
        'duration': 30,
        'dependencies': [5]
    },
    {
        'id': 9,
        'description': 'CS111 @ 11am',
        'duration': 90,
        'dependencies': [3],
        'time': 11
    },
    {
        'id': 10,
        'description': 'Take a nap',
        'duration': 90,
        'dependencies': [3]
    },
    {
        'id': 11,
        'description': 'Wake up',
        'duration': 30,
        'dependencies': []
    }
]

# convert tasks above to pandas dataframe to see them in tabular form
df = pd.DataFrame(somtos_tasks)
# use the ids as dataframe's index
df.set_index('id', inplace=True)

# don't print for imports
if __name__ == '__main__':
    print("Table of Somto's Tasks for the day:")
    print(tabulate(df, headers='keys', tablefmt='pretty'))
