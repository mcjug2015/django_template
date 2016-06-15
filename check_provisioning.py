# Get the url from terraform, curl the welcome page, make sure login element is there
import subprocess


TERRAFORM_COMMAND_BASE = "/var/lib/jenkins/tools/org.jenkinsci.plugins.terraform.TerraformInstallation/terraform/terraform"
CURL_COMMAND_BASE = "/usr/bin/curl"
GREP_TERM = "public_dns = "
STATE_FILE_PATH = "/var/lib/jenkins/workspace/dt_aws/provisioning/terraform/aws/terraform.tfstate"


def get_url():
    ''' grab the url from terraform show '''
    prov_info = subprocess.check_output([TERRAFORM_COMMAND_BASE, "show",
                                         STATE_FILE_PATH])

    for item in prov_info.split('\n'):
        if item.strip().startswith(GREP_TERM):
            the_url = item.strip().replace(GREP_TERM, '')
    
    the_url = "https://%s/welcome/" % the_url
    return the_url


def check_url(site_url):
    ''' check the url '''
    check_results = subprocess.check_output([CURL_COMMAND_BASE, '--insecure', site_url])
    if "You must login to use this site" not in check_results:
        raise ValueError("Site does not seem to be up, curl output:%s", check_results)


def check_aws():
    ''' make sure the site is provisioned in aws '''
    the_url = get_url()
    check_url(the_url)


if __name__ == "__main__":
    check_aws()
