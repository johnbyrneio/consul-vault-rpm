# RPM Spec for Consul Agent for Vault Storage

Build RPM for Consul Agent for Vault Storage

In a Vault deployment where you want to use one Consul agent for service discovery and a second agent for Consul storage,
you will need to run the second agent on non-default ports. This RPM deploys a second Consul agent with its own configuration
and data directories and configures the service to run on non-default ports.

Basically a clone of https://github.com/tomhillable/consul-rpm repurposed for Vault storage Consul agent

Tries to follow the [packaging guidelines](https://fedoraproject.org/wiki/Packaging:Guidelines) from Fedora.

* Binary: `/usr/bin/consul-vault`
* Config: `/etc/consul-vault.d/`
* Shared state: `/var/lib/consul-vault/`
* Sysconfig: `/etc/sysconfig/consul-vault`

# Using

Create the RPMs using one of the techniques outlined in the Build section below.

## Pre-built packages

Pre-built packages are maintained via the [Fedora Copr](https://copr.fedoraproject.org/coprs/) system. For more information, please see the [duritong/consul](https://copr.fedoraproject.org/coprs/duritong/consul/) repository on Copr.

# Build

There are a number of ways to build the `consul` RPM:
* Manual
* Vagrant
* Docker

Each method ultimately does the same thing - pick the one that is most comfortable for you.

### Version

The version number is hardcoded into the SPEC, however should you so choose, it can be set explicitly by passing an argument to `rpmbuild` directly:

```
$ rpmbuild --define "_version 1.7.1"
```

## Manual

Build the RPM as a non-root user from your home directory:

* Check out this repo. Seriously - check it out. Nice.
    ```
    git clone <this_repo_url>
    ```

* Install `rpmdevtools` and `mock`.
    ```
    sudo yum install rpmdevtools mock
    ```

* Set up your `rpmbuild` directory tree.
    ```
    rpmdev-setuptree
    ```

* Link the spec file and sources.
    ```
    ln -s $HOME/consul-rpm/SPECS/consul-vault.spec $HOME/rpmbuild/SPECS/
    find $HOME/consul-rpm/SOURCES -type f -exec ln -s {} $HOME/rpmbuild/SOURCES/ \;
    ```

* Download remote source files.
    ```
    spectool -g -R rpmbuild/SPECS/consul-vault.spec
    ```

* Spectool may fail if your distribution has an older version of cURL (CentOS
  6.x, for example) - if so, use Wget instead.
    ```
    VER=`grep Version rpmbuild/SPECS/consul-vault.spec | awk '{print $2}'`
    URL='https://dl.bintray.com/mitchellh/consul'
    wget $URL/consul_${VER}_linux_amd64.zip -O $HOME/rpmbuild/SOURCES/consul_${VER}_linux_amd64.zip
    wget $URL/consul_${VER}_web_ui.zip -O $HOME/rpmbuild/SOURCES/consul_${VER}_web_ui.zip
    ```

* Build the RPM.
    ```
    rpmbuild -ba rpmbuild/SPECS/consul-vault.spec
    ```

## Vagrant

If you have Vagrant installed:

* Edit `Vagrantfile` to point to your favourite box (Bento CentOS7 in this example).
    ```
    config.vm.box = "http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_centos-7.0_chef-provisionerless.box"
    ```

* Vagrant up! The RPMs will be copied to working directory after provisioning.
    ```
    vagrant up
    ```

## Docker

If you prefer building it with Docker:

* Build the Docker image. Note that you must amend the `Dockerfile` header if you want a specific OS build (default is `centos7`).
    ```
    docker build -t consul-vault:build .
    ```

* Run the build.
    ```
    docker run -v $HOME/consul-vault-rpms:/RPMS consul-vault:build
    ```

* Retrieve the built RPMs from `$HOME/consul-vault-rpms`.

# Result

One RPM:
- consul server/agent

# Run

* Install the RPM.
* Put config files in `/etc/consul-vault.d/`.
* Change command line arguments to consul in `/etc/sysconfig/consul-vault`.
  * Add `-bootstrap` **only** if this is the first server and instance.
* Start the service and tail the logs `systemctl start consul-vault.service` and `journalctl -f`.
  * To enable at reboot `systemctl enable consul-vault.service`.
* Consul may complain about the `GOMAXPROCS` setting. This is safe to ignore;
  however, the warning can be supressed by uncommenting the appropriate line in
  `/etc/sysconfig/consul-vault`.

## Config

Config files are loaded in lexicographical order from the `config-dir`. Some
sample configs are provided.

# More info

See the [consul.io](http://www.consul.io) website.
