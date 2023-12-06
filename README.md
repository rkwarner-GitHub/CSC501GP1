# CSC501GP1
group project 1


TO run install all packages:
pip install -r requirements.txt

Then run python xmltojson.py:
    plz put .xml files into the "datascience.stackexchange.com/" ahead of running I don't have a script to download the files

Then run using as an example:
python query_json.py --newquery=True --load=False --answer=True --tag=machine-learning


argument definitions into argpars:
('--tag', type=str, help='tags to search stackexchange database for')
('--newquery', type=boolean_string, default=False, help='set to true to run new query')
('--load', type=boolean_string, default=False, help='load from save file')
('--answer', type=boolean_string, default=True, help='choose True to get questions or False for actions')



