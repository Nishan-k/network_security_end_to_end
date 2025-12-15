import os


class S3sync:
    def sync_folder_to_s3(self, folder, aws_bucker_url):
        command_prompt = f"aws s3 sync {folder} {aws_bucker_url}"
        os.system(command_prompt)

    
    def sync_folder_from_s3(self, folder, aws_bucker_url):
        command_prompt = f"{aws_bucker_url} {folder}"
        os.system(command_prompt)
        