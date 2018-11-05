#!/usr/bin/python
#
# Copyright 2017 Graham Pugh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from autopkglib import Processor, ProcessorError

import subprocess
import os.path
import json
import requests

# Set the webhook_url to the one provided by Teams when you create the webhook

__all__ = ["TeamsWebhook"]

class TeamsWebhook(Processor):
    description = ("Posts to Teams via webhook as result of Munki run. "
                    "Takes elements from " "https://gist.github.com/devStepsize/b1b795309a217d24566dcc0ad136f784"
                    "and "
                    "https://github.com/autopkg/nmcspadden-recipes/blob/master/PostProcessors/Yo.py"
                    "Nearly all of this is lifted from https://github.com/grahampugh/recipes/blob/master/PostProcessors/slacker.py")
    input_variables = {
        "policy_category": {
            "required": False,
            "description": ("Policy Category.")
        },
        "category": {
            "required": False,
            "description": ("Package Category.")
        },
        "prod_name": {
            "required": False,
            "description": ("PROD_NAME")
        },
        "webhook_url": {
            "required": False,
            "description": ("Teams webhook.")
        },
        "munki_changed_objects": {
            "required": False,
            "description": ("Dictionary of added or changed values.")
    	}
    }
    output_variables = {
    }

    __doc__ = description

    def main(self):
        policy_category = self.env.get("policy_category")
        category = self.env.get("category")
        prod_name = self.env.get("prod_name")
        webhook_url = self.env.get("webhook_url")
        munki_changed_objects = self.env.get("munki_changed_objects")

        if munki_changed_objects:
            print "Title: %s" % prod_name
            print "Category: %s" % category
 #           print "Policy Category: %s" % policy_category
            teams_text = "*New Item added to Munki:*\nURL: %s\nTitle:  *%s*" % (prod_name, category)

            teams_data = {'text': teams_text}

            response = requests.post(webhook_url, json=teams_data)
            if response.status_code != 200:
                raise ValueError(
                                'Request to Teams returned an error %s, the response is:\n%s'
                                % (response.status_code, response.text)
                                )


if __name__ == "__main__":
    processor = TeamsWebhook()
    processor.execute_shell()
