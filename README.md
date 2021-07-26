# UWSGI Stresser

This is a UWSGI networking stress test.  It can test how well nginx
and uwsgi can return large data volumes over slow networks.

It was tested on Debian Stretch.

The instructions below assume you are root and in the top level of the
directory extracted from the tar.

## Installation

* Create the stress user to match the "uid =" line in stress.ini
    * `useradd -m -r -d /var/cache/stress -s /sbin/nologin stress`
* Copy the nginx config into nginx
    * `cp stress.conf /etc/nginx/sites-enabled/stress.conf`
* Test the nginx config
    * `nginx -t`
* Restart nginx
    * `systemctl restart nginx`
* Determine the IP address of this server and the network interface name
* Create a network emulation device **assuming** the name of your
  ethernet interface to use is `ens3`.  If not, update `ens3` below.
    * `tc qdisc add dev ens3 root netem`
* Create three aliases for varying the network performance
    * `alias FAST='tc qdisc change dev ens3 root netem rate 1000mbps'`
    * `alias MSLOW='tc qdisc change dev ens3 root netem rate 56kbps'`
    * `alias VSLOW='tc qdisc change dev ens3 root netem rate 9.6kbit'`
* Create the directory to hold the unix socket
    * `mkdir /run/stress`
    * `chown stress /run/stress`


## For each test
* Modify the `socket-timeout` value in `stress.ini`
* Slow down the network speed
    * `MSLOW`
* Run the API server
    * `/usr/bin/uwsgi --plugin syslog --plugin python37 --ini stress.ini`
* On another machine, fetch the data; change $IP to the IP address of the server
    * `time curl http://$IP/stress > /tmp/output
    * Maybe look at the last few lines of /tmp/outut to see it ends with `done`.
* Restore the network speed
    * `FAST`
* Kill the uwsgi process to stop this round