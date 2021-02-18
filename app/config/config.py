class Develop:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'YGT0HG6WrOj4xeofu/m4dxgKMcBV/7h4cdvErR+Giki3Bpk1QbRvWhaF6sXR07UDdwaRZWE8dco538ASox/pEFe0k5fSthlbFAgCAZtbk31or0p36yng6LCrXrobRJWwP5DE+TQ/nRMsx/Jpc9c2ATwOknBsFH3SrHLe8DunnoU='
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}' \
    #     .format(username='user',
    #             password='1234',
    #             host='127.0.0.1',
    #             port='15432',
    #             dbname='nrise_test')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'


Default = Develop