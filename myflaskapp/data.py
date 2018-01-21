# simple way to pass data to the application
# create a python file that either generates, reads, scrapes data and import it into main application script

def Articles():
    articles = [
        {
            'id': 1,
            'title': 'article one',
            'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            'author': 'Monty Python',
            'create_date': '21-01-2018'
        },
        {
            'id': 2,
            'title': 'article two',
            'body': 'Spam ham and eggs.',
            'author': 'Jim Jims',
            'create_date': '21-01-2018'
        },
        {
            'id': 3,
            'title': 'article three',
            'body': 'Spam ham and eggs.',
            'author': 'Jim Jims',
            'create_date': '21-01-2018'
        }
    ]

    return articles
