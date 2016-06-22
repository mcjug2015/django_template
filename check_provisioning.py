# Get the url from terraform, curl the welcome page, make sure login element is there
import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("provisioning_type", help="specify do or aws, and that provisioning will be checked")


TERRAFORM_COMMAND_BASE = "/var/lib/jenkins/tools/org.jenkinsci.plugins.terraform.TerraformInstallation/terraform/terraform"
CURL_COMMAND_BASE = "/usr/bin/curl"


class AbstractProvisioningChecker(object):
    ''' implement this to check provisioning '''
    
    def get_state_file_path(self):
        ''' get the tfstate file path '''
        raise NotImplementedError("abstract method, must implement to use")
    
    def get_grep_term(self):
        ''' get the grep term '''
        raise NotImplementedError("abstract method, must implement to use")
    
    def get_url(self):
        ''' grab the url from terraform show '''
        prov_info = subprocess.check_output([TERRAFORM_COMMAND_BASE, "show",
                                             self.get_state_file_path()])
    
        for item in prov_info.split('\n'):
            if item.strip().startswith(self.get_grep_term()):
                the_url = item.strip().replace(self.get_grep_term(), '')
        
        the_url = "https://%s/welcome/" % the_url
        return the_url

    def check_url(self, site_url):
        ''' check the url '''
        check_results = subprocess.check_output([CURL_COMMAND_BASE, '--insecure', site_url])
        if "You must login to use this site" not in check_results:
            raise ValueError("Site does not seem to be up, curl output:%s", check_results)

    def check_provisioning(self):
        ''' make sure the site is provisioned in aws '''
        the_url = self.get_url()
        self.check_url(the_url)


class AwsProvisioningChecker(AbstractProvisioningChecker):
    ''' checks aws provisioning '''
    
    def get_state_file_path(self):
        ''' get the tfstate file path '''
        return "/var/lib/jenkins/workspace/dt_aws/provisioning/terraform/aws/terraform.tfstate"
    
    def get_grep_term(self):
        ''' get the grep term '''
        return "public_dns = "


if __name__ == "__main__":
    args = parser.parse_args()
    if args.provisioning_type == 'aws':
        AwsProvisioningChecker().check_provisioning()
    elif args.provisioning_type == 'do':
        print "NOT READY YET"
    else:
        raise ValueError("Must provide a valid provisioning type!")
