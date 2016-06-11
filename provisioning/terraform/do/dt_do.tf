# Configure the DO tf

variable "do_token" {
  description = "Your DO token"
  default = "NOPE"
}

provider "digitalocean" {
    token = "${var.do_token}"
}

# Create a new SSH key
resource "digitalocean_ssh_key" "vsemenov_mac_dt_key" {
    name = "Victors mac public django template key"
    public_key = "${file("./../mac_key.pub")}"
}

resource "digitalocean_droplet" "dt_web" {
    image = "centos-7-2-x64"
    name = "dtweb"
    region = "nyc3"
    size = "2gb"
    user_data = "${file("./../cloud_init.txt")}"
    ssh_keys = ["${digitalocean_ssh_key.vsemenov_mac_dt_key.id}"]
}