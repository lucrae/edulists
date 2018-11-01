import click
import secrets

def register(app):

    @app.cli.group()
    def security():
        """Access security and config information"""
        pass

    @security.command('config')
    def display_config():
        """Display configuration variables"""

        details = app.config
        print(f'Config variables for "{app.name}":')
        for detail in details:
            print(f'\t {detail}: {details[detail]}')

    @security.command('genhex')
    @click.argument('length')
    def generate_hex_token(length):
        """Randomly generate a hex token"""

        token = secrets.token_hex(int(length) // 2)
        print(token)