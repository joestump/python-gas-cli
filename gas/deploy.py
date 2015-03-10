import os
import glob
import json
from optparse import make_option
from gas.base import BaseCommand, CommandError


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-f', '--file-id', dest='file_id',
                    help='The file ID of the Google App Script.'),
        make_option('-b', '--build-path', dest='build_path',
                    help='Path to files to upload.'),
    )

    FILES_LIST_URL = "https://script.google.com/feeds/download/export?id=%s"
    UPLOAD_URL = "https://www.googleapis.com/upload/drive/v2/files/%s"

    def handle(self, args, opts):
        store = Storage('credentials.json')
        credentials = store.get()
        http = credentials.authorize(httplib2.Http())
        existing_files = self.get_existing_files()
        files_to_upload += glob.glob('%shtml/*.(html|gs)' % PATH)
        files_payload = {
            "files": []
        }
        for file_path in files_to_upload:
            key = os.path.basename(file_path)
            file_name, ext = key.split('.')
            if ext == 'html':
                file_type = 'html'
            elif ext == 'gs':
                file_type = 'server_js'
            else:
                continue

            try:
                file_to_upload = {
                    'id': existing_files[key]['id']
                }
                print "Found id=%s for key=%s." % (existing_files[key]['id'], key)
            except KeyError:
                print "No existing file found for %s." % key
                file_to_upload = {}

            with open(file_path) as fp:
                file_contents = fp.read()

            file_to_upload.update({
                'name': file_name,
                'type': file_type,
                'source': file_contents
            })

            files_payload['files'].append(file_to_upload)

        (resp, content) = http.request(self.UPLOAD_URL % options.file_id,
    "PUT", body=json.dumps(files_payload), headers={'Content-Type': 'application/vnd.google-apps.script+json'})

print
print resp['status']
#

    def get_existing_files(self, file_id):
        (resp_headers, content) = http.request(self., "GET")
        existing_files = json.loads(content)
        files_found = {}
        for obj in files['files']:
            if obj['type'] == 'server_js':
                ext = 'gs'
            elif obj['type'] == 'html':
                ext = 'html'
            else:
                continue

            key = '%s.%s' % (obj['name'], ext)
            files_count[key] = obj

        return files_found
