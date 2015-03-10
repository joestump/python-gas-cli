import pprint
import os
import glob
import sys
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

    FILES_LIST_URL = "https://script.google.com/feeds/download/export?id=%s&format=json"
    UPLOAD_URL = "https://www.googleapis.com/upload/drive/v2/files/%s"

    EXTS = {
        'gs': 'server_js',
        'html': 'html',
    }

    TYPES = {v: k for k, v in EXTS.items()}

    def handle(self, args, opts):
        if not opts.file_id:
            raise CommandError("A file ID is required.")

        http = self.get_client(opts)

        print "Looking up existing GAS project (id=%s) files..." % opts.file_id
        existing_files = self.get_existing_files(opts)
        for key, obj in existing_files.iteritems():
            print " - Found %s (id=%s, type=%s)" % (key, obj['id'], obj['type'])
        print "%s files found.\n" % (len(existing_files))

        self.upload_build(opts, existing_files)

    def upload_build(self, opts, existing_files):
        print "Inspecting build %s..." % opts.build_path
        files_to_upload = [f  for f in glob.glob('%s/*' % opts.build_path) if
            f.split('.')[-1] in self.EXTS.keys()]

        files_payload = {
            "files": []
        }

        for file_path in files_to_upload:
            key = os.path.basename(file_path)
            file_name, ext = key.split('.')
            try:
                file_type = self.EXTS[ext]
            except KeyError:
                continue

            try:
                file_to_upload = {
                    'id': existing_files[key]['id']
                }
                print " - Replace %s (id=%s) with %s." % (key,
                    existing_files[key]['id'], key)
            except KeyError:
                print " - New file %s found." % key
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

        sys.stdout.write("Uploading %s files... " % len(files_payload['files']))
        sys.stdout.flush()
        (resp, content) = self.get_client(opts).request(
            self.UPLOAD_URL % opts.file_id, "PUT",
            body=json.dumps(files_payload),
            headers={'Content-Type': 'application/vnd.google-apps.script+json'})
        if int(resp['status']) == 200:
            print "Done."
        else:
            print "Error (%s)." % resp['status']

    def get_existing_files(self, opts):
        (resp, content) = self.get_client(opts).request(
            self.FILES_LIST_URL % opts.file_id, "GET")
        existing_files = json.loads(content)
        files_found = {}
        for obj in existing_files['files']:
            if obj['type'] == 'server_js':
                ext = 'gs'
            elif obj['type'] == 'html':
                ext = 'html'
            else:
                continue

            key = '%s.%s' % (obj['name'], ext)
            files_found[key] = obj

        return files_found
