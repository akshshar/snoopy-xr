# snoopy-xr
Installing snoopy on IOS-XR to log all exec messages

This is a fairly simple exercise.
We're gonna learn from https://xrdocs.github.io/application-hosting/tutorials/2016-06-17-xr-toolbox-part-5-running-a-native-wrl7-app/  and download the WRL7 vagrant box advertised to help build snoopy from scratch for WRL7 running as a distribution on IOS-XR.


## What is Snoopy?

You can learn more about snoopy here:  https://github.com/a2o/snoopy
It's a small library that basically logs all the executed commands (+ arguments) on your system and sends logs to /var/log/auth.log or equivalent locations based on the distro in use.




## Setup a WRL7 vagrant box environment

The WRL7 vagrant box is published on atlas at:  <https://app.vagrantup.com/ciscoxr/boxes/appdev-xr6.1.1>
To set up the vagrant environment:

```
mkdir xr-build
cd xr-build
vagrant init ciscoxr/appdev-xr6.1.1
vagrant up
```
In a short while, the vagrant box would come up with the following messages:

```
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
    default: No guest additions were detected on the base box for this VM! Guest
    default: additions are required for forwarded ports, shared folders, host only
    default: networking, and more. If SSH fails on this machine, please install
    default: the guest additions and repackage the box to continue.
    default: 
    default: This is not an error message; everything may continue to work properly,
    default: in which case you may ignore this message.

==> default: Machine 'default' has a post `vagrant up` message. This is a message
==> default: from the creator of the Vagrantfile, and not from Vagrant itself:
==> default: 
==> default: Welcome to the IOS XR Application Development (AppDev) VM that provides a WRL7 based native environment to build applications for IOS XR (Release 6.1.1) platforms. 
```

Cool, now ssh into the box and you're good to start:

```
vagrant ssh
```

## Building WRL7 RPM from Snoopy from source code

Fetch the sample snoopy RPM SPEC file from github

```
localhost:~$ git clone https://github.com/linuxhq/rpmbuild-snoopy.git rpmbuild
Cloning into 'rpmbuild'...
remote: Counting objects: 10, done.
remote: Total 10 (delta 0), reused 0 (delta 0), pack-reused 10
Unpacking objects: 100% (10/10), done.
Checking connectivity... done.
```

We'll edit the SPEC file to specify our own release structure at the top, something like this:

```
localhost:~$ cat rpmbuild/SPECS/snoopy.spec
Name:		snoopy
Version:	2.4.6
Release:        XR_6.2.2	
Summary:	User monitoring and command logging
Group:		Applications/Monitoring
License:	GPL
URL:		https://github.com/a2o/%{name}
Source0:	http://source.a2o.si/download/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  autoconf, automake, git, gcc, libtool, make, socat

######### SNIP OUTPUT ###########

```


Finally, issue an RPM build:

```
localhost:~$ sudo rpmbuild -ba rpmbuild/SPECS/snoopy.spec
sh: line 0: fg: no job control
Fetching(Source0): http://10.30.110.215:9090/snoopy-2.4.6.tar.gz
Executing(%prep): /bin/sh -e /var/tmp/rpm-tmp.59617
+ umask 022
+ cd /usr/lib64/rpm/../../src/rpm/BUILD
+ cd /usr/src/rpm/BUILD
+ rm -rf snoopy-2.4.6
+ /bin/tar -xf -
+ /bin/gzip -dc /usr/src/rpm/SOURCES/snoopy-2.4.6.tar.gz
+ STATUS=0
+ '[' 0 -ne 0 ']'
+ cd snoopy-2.4.6
+ exit 0
Executing(%build): /bin/sh -e /var/tmp/rpm-tmp.59617
+ umask 022
+ cd /usr/lib64/rpm/../../src/rpm/BUILD
+ cd snoopy-2.4.6
+ CFLAGS=-O2
+ export CFLAGS
+ CXXFLAGS=-O2
+ export CXXFLAGS
+ FFLAGS=-O2
+ export FFLAGS
+ ./configure --host=x86_64-wrs-linux-gnu --build=x86_64-wrs-linux-gnu --target=x86_64-wrs-linux --program-prefix= --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --sysconfdir=/usr/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib --libexecdir=/usr/libexec --localstatedir=/usr/var --sharedstatedir=/usr/com --mandir=/usr/share/man --infodir=/usr/share/info --enable-everything
checking for a BSD-compatible install... /usr/bin/install -c
checking whether build environment is sane... yes
checking for a thread-safe mkdir -p... /bin/mkdir -p
checking for gawk... gawk
checking whether make sets $(MAKE)... yes
checking whether make supports nested variables... yes
checking whether make supports nested variables... (cached) yes
checking for style of include used by make... GNU
checking for x86_64-wrs-linux-gnu-gcc... no
checking for gcc... gcc
checking whether the C compiler works... yes
checking for C compiler default output file name... a.out
checking for suffix of executables... 
checking whether we are cross compiling... no
checking for suffix of object files... o
checking whether we are using the GNU C compiler... yes
checking whether gcc accepts -g... yes
checking for gcc option to accept ISO C89... none needed
checking whether gcc understands -c and -o together... yes
checking dependency style of gcc... gcc3
checking for x86_64-wrs-linux-gnu-ar... no
checking for x86_64-wrs-linux-gnu-lib... no
checking for x86_64-wrs-linux-gnu-link... no
checking for ar... ar

######################## SNIP OUTPUT ############################
```


The build should be successful and you'll find your installable RPM at the location:

```
/usr/src/rpm/RPMS/x86_64/snoopy-2.4.6-XR_6.2.2.x86_64.rpm
```

## Installing snoopy RPM on IOS-XR 

scp this RPM onto an IOS-XR router's bash prompt and install using a yum localonly install:

```
[host:~]$ yum install localonly snoopy-2.4.6-XR_6.2.2.x86_64.rpm 
Loaded plugins: downloadonly, protect-packages, rpm-persistence
puppetlabs                                               | 2.9 kB     00:00     
puppetlabs/primary_db                                    |  20 kB     00:00     
Setting up Install Process
No package localonly available.
Examining snoopy-2.4.6-XR_6.2.2.x86_64.rpm: snoopy-2.4.6-XR_6.2.2.x86_64
Marking snoopy-2.4.6-XR_6.2.2.x86_64.rpm to be installed
Resolving Dependencies
--> Running transaction check
---> Package snoopy.x86_64 0:2.4.6-XR_6.2.2 will be installed
--> Finished Dependency Resolution

################  SNIP OUTPUT ############

```


### Enabling snoopy:

You can now enable snoopy on the system by executing the installed enable binary:

```
[host:~]$ snoopy-enable.x86_64 
SNOOPY: Removing from /etc/ld.so.preload: /usr/lib/libsnoopy.so
SNOOPY: Adding to /etc/ld.so.preload:     /usr/lib/libsnoopy.so
SNOOPY: Hint #1: Reboot your machine to load Snoopy system-wide.
SNOOPY: Hint #2: Check your log files for output.
SNOOPY: Enabled.
[host:~]$ 

```

To disable, just run snoopy-disable.x86_64 


## Testing snoopy on IOS-XR

This is can prove to be quite verbose depending on what sort of exec commands are executed. But let's try out a simple shell script:

```
[host:~]$ cat loop.sh 
#!/bin/bash

while true; do
    ip netns exec global-vrf ifconfig
    ip netns exec global-vrf ping 11.11.11.2 -c 2
    sleep 5
done
[host:~]$ 

```

We'll run this shell script in the background and see if snoopy picks up the actions it takes:

```
[host:~]$ ./loop.sh > /dev/null 2>&1 &
[1] 30437
[host:~]$ 
```

Checking the logs in `/var/log/auth.log`:

```
[host:~]$ tail -f /var/log/auth.log 
Oct 14 10:30:30 host snoopy[30451]: [uid:0 sid:29815 tty:/dev/pts/5 cwd:/misc/scratch filename:/usr/bin/wc]: wc -l /var/log/xr_audit_trail_logs/audit_29840
Oct 14 10:30:31 host snoopy[30453]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root filename:/sbin/ip]: ip netns exec global-vrf ifconfig
Oct 14 10:30:31 host snoopy[30454]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root filename:/sbin/ip]: ip netns exec global-vrf ping 11.11.11.2 -c 2
Oct 14 10:30:32 host snoopy[30455]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root filename:/bin/sleep]: sleep 5
Oct 14 10:30:35 host snoopy[30464]: [uid:0 sid:29815 tty:/dev/pts/5 cwd:/misc/scratch filename:/usr/bin/wc]: wc -l /var/log/xr_audit_trail_logs/audit_29840
Oct 14 10:30:37 host snoopy[30466]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root filename:/sbin/ip]: ip netns exec global-vrf ifconfig
Oct 14 10:30:37 host snoopy[30467]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root filename:/sbin/ip]: ip netns exec global-vrf ping 11.11.11.2 -c 2
Oct 14 10:30:38 host snoopy[30468]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root filename:/bin/sleep]: sleep 5
Oct 14 10:30:40 host snoopy[30470]: [uid:0 sid:29815 tty:/dev/pts/5 cwd:/misc/scratch filename:/usr/bin/wc]: wc -l /var/log/xr_audit_trail_logs/audit_29840
Oct 14 10:30:41 host snoopy[30472]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root filename:/usr/bin/tail]: tail -f /var/log/auth.log
Oct 14 10:30:43 host snoopy[30473]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root filename:/sbin/ip]: ip netns exec global-vrf ifconfig
Oct 14 10:30:43 host snoopy[30474]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root filename:/sbin/ip]: ip netns exec global-vrf ping 11.11.11.2 -c 2
Oct 14 10:30:44 host snoopy[30475]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root filename:/bin/sleep]: sleep 5
Oct 14 10:30:45 host snoopy[30477]: [uid:0 sid:29815 tty:/dev/pts/5 cwd:/misc/scratch filename:/usr/bin/wc]: wc -l /var/log/xr_audit_trail_logs/audit_29840
Oct 14 10:30:49 host snoopy[30479]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root filename:/sbin/ip]: ip netns exec global-vrf ifconfig
Oct 14 10:30:49 host snoopy[30480]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root filename:/sbin/ip]: ip netns exec global-vrf ping 11.11.11.2 -c 2
Oct 14 10:30:50 host snoopy[30481]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root filename:/bin/sleep]: sleep 5
Oct 14 10:30:50 host snoopy[30483]: [uid:0 sid:29815 tty:/dev/pts/5 cwd:/misc/scratch filename:/usr/bin/wc]: wc -l /var/log/xr_audit_trail_logs/audit_29840


```


Awesome. This will even capture logs for basic events like `cp` or `cat`:

```
Oct 14 10:31:53 host snoopy[30556]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root fii
lename:/bin/cp]: cp loop.sh new_loop.sh
Oct 14 10:31:57 host snoopy[30560]: [uid:0 sid:29857 tty:/dev/pts/7 cwd:/root fii
lename:/bin/cat]: cat /etc/passwd
```


## Disclaimer

This is purely a representation of how an auditing system can be set up for linux events in IOS-XR. Snoopy isn't intended to be used in production devices.
























