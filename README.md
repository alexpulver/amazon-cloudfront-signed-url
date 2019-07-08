This is an example application for generating Amazon CloudFront signed URLs

The application expects two files in root directory of the project:
* `config.json` - Application configuration (see structure below)
* `private_key.pem` - Amazon CloudFront private key in PEM format. See [Specifying the AWS Accounts That Can Create Signed URLs and Signed Cookies (Trusted Signers)](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-trusted-signers.html) for instructions to creating a key pair

`config.json` structure:
```json
{
  "private_key_id": "PRIVATE_KEY_ID"
}
```