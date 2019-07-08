import json
import os
from datetime import datetime, timedelta

import rsa
from botocore.signers import CloudFrontSigner
from chalice import Chalice


app = Chalice(app_name='caching-auth-api')


@app.route('/presigned-url')
def get_presigned_url() -> str:
    """
    Two query parameters are required:
    * url: Base URL for the file
    * resource: URL or stream name of the file

    This code uses botocore.signers.CloudFrontSigner to generate presigned URLs
    using a custom policy.

    See Amazon CloudFront documentation for more details on the signing process:
    https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-creating-signed-url-custom-policy.html

    Example using cURL:
    curl 'http://localhost:8000/presigned-url?url=https://www.example.com/images/image.jpg&resource=https://www.example.com/images/*'

    :return str: The signed URL
    """
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_file_path) as config_file:
        config = json.load(config_file)
    private_key_id = config['private_key_id']

    request = app.current_request
    url = request.query_params['url']
    resource = request.query_params['resource']

    expire_date = datetime.now() + timedelta(minutes=+5)

    cf_signer = CloudFrontSigner(private_key_id, rsa_signer)
    cf_policy = cf_signer.build_policy(resource=resource, date_less_than=expire_date)
    presigned_url = cf_signer.generate_presigned_url(url, policy=cf_policy)

    return presigned_url


def rsa_signer(message):
    private_key_path = os.path.join(os.path.dirname(__file__), 'private_key.pem')
    with open(private_key_path) as private_key_file:
        private_key = private_key_file.read()
    return rsa.sign(
        message,
        rsa.PrivateKey.load_pkcs1(private_key.encode('utf8')),
        'SHA-1')  # CloudFront requires SHA-1 hash
