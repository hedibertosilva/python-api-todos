"""
    JSON helper.
"""
import json


class JSON:
    """ Useful methods. """

    @staticmethod
    def read_file(path):
        """ Load JSON files. """
        try:
            with open(path, encoding="utf-8") as json_file:
                return json.load(json_file)
        except OSError:
            return "File not found."
        except json.JSONDecodeError:
            return "File is not in JSON format."
