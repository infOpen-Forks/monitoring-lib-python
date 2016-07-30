"""
This module manage rejected connection arguments
"""

from argparse import ArgumentParser


class RejectedConnectionParser(ArgumentParser):
    """
    Manage rejected connection thresholds argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Thresholds')

        # Argument settings
        group.add_argument(
            '--warn-rejected-connection',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', int),
            default=kwargs.get('default', 25),
            help=kwargs.get('help', 'Rejected connection warning threshold'),
            required=kwargs.get('required', False))

        # Argument settings
        group.add_argument(
            '--crit-rejected-connection',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', int),
            default=kwargs.get('default', 50),
            help=kwargs.get('help', 'Rejected connection critical threshold'),
            required=kwargs.get('required', False))
