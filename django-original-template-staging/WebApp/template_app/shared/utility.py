import json
import hashlib
import re

from .initializers import init_vars


class Utilities():

    # Method to Create Run ID
    @classmethod
    def createRunId(self, data):
        run_input_id = ""

        # get model version and add to run id
        globals = init_vars.init_global_vars()
        model_version = globals['model_version']

        run_input_id = model_version

        # concatenate form values together and hash for key
        for key, value in sorted(data.items()):
            run_input_id = run_input_id + '|' + str(value)
        return run_input_id

    # Method to Create Hash Seed
    @classmethod
    def createHashKey(self, run_form_id):
        m = hashlib.md5(run_form_id.encode('utf-8')).hexdigest()
        return m

    # Method to update the JSON Field with the new Run ID
    @classmethod
    def updateJson(self, run_id, data):
        data.update({"RUN_ID": run_id})
        return data

    # Method to update the JSON Field with the new Run ID
    @classmethod
    def createOutput(self, runid, inputs, output):

        var0 = {"RunId": runid, "Simulation": "0"}
        var1 = {"RunId": runid, "Simulation": "1"}
        var2 = {"RunId": runid, "Simulation": "1"}
        for key, value in output.items():
            if '0' in key.lower():
                _key = re.sub('0', '', key)
                var0[_key] = value
            if '1' in key.lower():
                _key = re.sub('1', '', key)
                var1[_key] = value
            if '2' in key.lower():
                _key = re.sub('2', '', key)
                var2[_key] = value

        run_data = []
        run_data.append(var0)
        run_data.append(var1)
        run_data.append(var2)

        results = {"RunId": runid,
                   "inputs": json.dumps(inputs), "results": json.dumps(run_data)}
        return results
