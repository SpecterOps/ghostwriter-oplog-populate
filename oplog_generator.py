import csv
import random

from faker import Faker

def generate_oplog(file_path, entries):
    """
    generate_oplog creates a Ghostwriter-compatible CSV containing a user-specified
    number of randomized entries, at a user-specified location.

    @param file_path - the location to create the CSV
    @param entries - the number of randomized entries to generate for the CSV
    """

    # Define the fields of the CSV
    fields = [
        'entry_identifier',
        'start_date',
        'end_date',
        'source_ip',
        'dest_ip',
        'tool',
        'user_context',
        'command',
        'description',
        'output',
        'comments',
        'operator_name',
        'extra_fields',
        'oplog_id',
        'tags'
    ]

    with open(file_path, 'a', newline='') as csv_file:
        oplog_writer = csv.DictWriter(csv_file, fieldnames=fields)
        oplog_writer.writeheader()

        generator = Faker()

        src = []
        dest = []
        # A dict of tools and corresponding possible commands/description/comment combinations
        tools = {
            'Cobalt Strike': [
                {
                    'command': 'shinject ' + str(random.randrange(1,32768)) + ' x64 ' + generator.file_path(depth=0, extension="bin",absolute=True),
                    'description': 'PID ' + str(random.randrange(1,32768)),
                    'comment': 'Attempting process injection'
                }, {
                    'command': 'sleep ' + str(random.randrange(0,100)),
                    'description': 'PID ' + str(random.randrange(1,32768)),
                    'comment': 'Sleeping a beacon'
                }, {
                    'command': 'inject-assembly '+ str(random.randrange(0,32768)) + ' ' + generator.file_path(depth=1, extension="exe",absolute=True),
                    'description': 'PID ' + str(random.randrange(1,32768)),
                    'comment': 'Injecting assembly into a process'
                }, {
                    'command': 'execute-assembly ' + generator.file_path(depth=1, extension="exe",absolute=True),
                    'description': 'PID ' + str(random.randrange(1,32768)),
                    'comment': 'Running a local .NET executable'
                }, {
                    'command': 'upload ' + generator.file_path(depth=random.randrange(1,4), absolute=True),
                    'description': 'PID ' + str(random.randrange(1,32768)),
                    'comment': 'Attempting a file upload'
                }, {
                    'command': 'cd ' + generator.file_path(depth=random.randrange(1,4), extension=[]),
                    'description': 'PID ' + str(random.randrange(1,32768)),
                    'comment': 'Navigating to a directory'
                }, {
                    'command': 'spawnto x64 ' + generator.file_path(depth=random.randrange(1,4)),
                    'description': 'PID ' + str(random.randrange(1,32768)),
                    'comment': 'Selecting executable for post-exploitation jobs'
                }, {
                    'command': 'spawn x64 HTTPS',
                    'description': 'PID ' + str(random.randrange(1,32768)),
                    'comment': 'Navigating to a directory'
                }, {
                    'command': 'pwd',
                    'description': 'PID ' + str(random.randrange(1,32768)),
                    'comment': 'Obtaining current working directory'
                }
            ],
            'OST': [
                {
                    'command': 'download ' + generator.file_path(depth=random.randrange(1,4)),
                    'description': 'PID: ' + str(random.randrange(1,32768)),
                    'comment': 'Downloading a file'
                }, {
                    'command': 'ls',
                    'description': 'PID: ' + str(random.randrange(1,32768)),
                    'comment': 'Listing files and directories'                    
                }, {
                    'command': 'sleep ' + str(random.randrange(0,100)),
                    'description': 'PID: ' + str(random.randrange(1,32768)),
                    'comment': 'Sleeping a beacon'
                }, {
                    'command': 'cd ' + generator.file_path(depth=random.randrange(1,4), extension=[]),
                    'description': 'PID: ' + str(random.randrange(1,32768)),
                    'comment': 'Navigating to a directory'
                }, {
                    'command': 'bbot -t ' + generator.domain_name() + '-m nmap',
                    'description': 'PID: ' + str(random.randrange(1,32768)),
                    'comment': 'Using BBOT port scan'
                }, {
                    'command': 'bbot -t ' + generator.domain_name() + '-f safe -ef passive',
                    'description': 'PID: ' + str(random.randrange(1,32768)),
                    'comment': 'Using BBOT safe and passive modules'
                }, {
                    'command': 'python3 CloudScraper.py -u ' + generator.domain_name() + ' >> ' + generator.file_path(depth=random.randrange(1,4), extension="txt", absolute=True),
                    'description': 'PID: ' + str(random.randrange(1,32768)),
                    'comment': 'Navigating to a directory'
                }
            ],
            'Poseidon': [ 
                {
                    'command': 'pty whoami',
                    'description': 'PID ' + str(random.randrange(1,32768)) + ', Callback ' + str(random.randrange(1,100)),
                    'comment': 'Obtaining user context'
                }, {
                    'command': 'pty kubectl get namespaces',
                    'description': 'PID ' + str(random.randrange(1,32768)) + ', Callback ' + str(random.randrange(1,100)),
                    'comment': 'Conducting container discovery'
                }, {
                    'command': 'pty ./kubectl can-i create pod',
                    'description': 'PID ' + str(random.randrange(1,32768)) + ', Callback ' + str(random.randrange(1,100)),
                    'comment': 'Conducting container discovery'
                }, {
                    'command': 'pty ./kubectl get secrets',
                    'description': 'PID ' + str(random.randrange(1,32768)) + ', Callback ' + str(random.randrange(1,100)),
                    'comment': 'Conducting container discovery'
                }, {
                    'command': 'pty ./kubectl get pods',
                    'description': 'PID ' + str(random.randrange(1,32768)) + ', Callback ' + str(random.randrange(1,100)),
                    'comment': 'Conducting container discovery'
                }, {
                    'command': 'pty ./kubectl get namespaces -n cluster',
                    'description': 'PID ' + str(random.randrange(1,32768)) + ', Callback ' + str(random.randrange(1,100)),
                    'comment': 'Conducting container discovery'
                }, {
                    'command': 'pty curl',
                    'description': 'PID ' + str(random.randrange(1,32768)) + ', Callback ' + str(random.randrange(1,100)),
                    'comment': 'Attempting to use cURL'
                }, {
                    'command': 'upload {"file_id":"' + generator.uuid4() + '","remote_path"' + generator.file_path() + '","overwrite":false}',
                    'description': 'PID ' + str(random.randrange(1,32768)) + ', Callback ' + str(random.randrange(1,100)),
                    'comment': 'Attempting to upload a file'
                }, {
                    'command': 'socks {"action":"start","port":' + str(generator.port_number(is_user=True)) + '}',
                    'description': 'PID ' + str(random.randrange(1,32768)) + ', Callback ' + str(random.randrange(1,100)),
                    'comment': 'Attempting to start a SOCKS proxy'
                }, {
                    'command': 'sleep ' + str(random.randrange(0,100)),
                    'description': 'PID ' + str(random.randrange(1,32768)) + ', Callback ' + str(random.randrange(1,100)),
                    'comment': 'Sleeping a beacon'
                }, {
                    'command': 'getenv',
                    'description': 'PID ' + str(random.randrange(1,32768)) + ', Callback ' + str(random.randrange(1,100)),
                    'comment': 'Attempting to get environment variables'
                }
            ]
        }
        user_context = []
        output = ["Success", "Failed"]
        operators = []

        # Randomize src, dest, user_context, and operators
        for _ in range(random.randrange(2,10)):
            src.append(generator.ipv4())
        for _ in range(random.randrange(2,10)):
            dest.append(generator.ipv4())
        for _ in range(random.randrange(2,10)):
            user_context.append(generator.ascii_company_email())
        for _ in range(random.randrange(2,4)):
            operators.append(generator.name())

        # Randomize project start date and end date
        project_start_datetime = generator.date_time_between(start_date='-1y')
        project_end_datetime = generator.date_time_between(start_date=project_start_datetime)

        # Write the randomized entries to the CSV
        for entry_index in range(entries):
            start_date = generator.date_time_between(start_date=project_start_datetime)
            source_ip = random.choice(src)
            dest_ip = random.choice(dest)
            tool = random.choice(list(tools.keys()))
            command_dict = random.choice(tools[tool])
            oplog_writer.writerow({
                'entry_identifier': entry_index,
                'start_date': start_date,
                'end_date': generator.date_time_between(
                    start_date=start_date,
                    end_date=project_end_datetime
                ),
                'source_ip': source_ip,
                'dest_ip': dest_ip,
                'tool': tool,
                'user_context': random.choice(user_context),
                'command': command_dict['command'],
                'description': command_dict['description'],
                'output': random.choice(output),
                'comments': command_dict['comment'],
                'operator_name': random.choice(operators),
                'extra_fields': "",
                'oplog_id': "",
                'tags': ""
            })
