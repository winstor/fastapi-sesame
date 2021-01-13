default = 'local'

connections = {
    'local': {
        'url': 'sqlite:///./app/db/sql_app.db',
        'kwargs': {
            "connect_args": {"check_same_thread": False}
        },
    },
    'workflow': {
        'url': 'sqlite:///./app/db/sql_workflow.db',
        'kwargs': {
            "connect_args": {"check_same_thread": False}
        }
    },
    'workflow1': {
        'url': 'sqlite:///./app/db/sql_workflow1.db',
        'kwargs': {
            "connect_args": {"check_same_thread": False}
        }
    },
    'workflow10': {
        'url': 'sqlite:///./app/db/sql_workflow10.db',
        'kwargs': {
            "connect_args": {"check_same_thread": False}
        }
    },
    'sesame': {
        'url': 'sqlite:///./app/db/sesame_database.db',
        'kwargs': {
            "connect_args": {"check_same_thread": False}
        }
    },
}
