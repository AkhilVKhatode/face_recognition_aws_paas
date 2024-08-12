#__copyright__   = "Copyright 2024, VISA Lab"
#__license__     = "MIT"

import os
import ffmpeg
import boto3
import subprocess
import math

config = {
    "AWS_ACCESS_KEY_ID": "your-access-key-id",
    "AWS_SECRET_ACCESS_KEY": "your-secret-access-key",
    "STAGE_1_BUCKET": "your-stage-bucket",
}

session = boto3.Session(
    region_name="us-east-1",
    aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"]
)
s3 = session.client("s3")

def handler(event, context):
	bucket_id_input = event['Records'][0]['s3']['bucket']['name']
	video_file_obj = event['Records'][0]['s3']['object']['key']
	video_file_name = '/tmp/' + os.path.basename(video_file_obj)

	s3.download_file(bucket_id_input, video_file_obj, video_file_name)
	local_out_dir = video_splitting_cmdline(video_file_name)

	for root, dirs, files in os.walk(local_out_dir):
		for file in files:
			file_to_upload_path = os.path.join(root, file)
			s3.upload_file(file_to_upload_path, config["STAGE_1_BUCKET"], os.path.basename(local_out_dir) + '/' + file)
	subprocess.run(['rm', '-rf', local_out_dir])

def video_splitting_cmdline(video_filename):
    filename = os.path.basename(video_filename)
    outdir = os.path.splitext(filename)[0]
    outdir = os.path.join("/tmp",outdir)
    output_dir = outdir
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    split_cmd = '/usr/bin/ffmpeg -ss 0 -r 1 -i ' +video_filename+ ' -vf fps=1/0.1 -start_number 0 -vframes 10 ' + outdir + "/" + 'output_%02d.jpg -y'
    try:
        subprocess.check_call(split_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.returncode)
        print(e.output)

    fps_cmd = 'ffmpeg -i ' + video_filename + ' 2>&1 | sed -n "s/.*, \\(.*\\) fp.*/\\1/p"'
    fps = subprocess.check_output(fps_cmd, shell=True).decode("utf-8").rstrip("\n")
    fps = math.ceil(float(fps))
    return outdir