# snoopy-xr
Installing snoopy on IOS-XR to log all exec messages

This is a fairly simple exercise.
We're gonna learn from https://xrdocs.github.io/application-hosting/tutorials/2016-06-17-xr-toolbox-part-5-running-a-native-wrl7-app/  and download the WRL7 vagrant box advertised to help build snoopy from scratch for WRL7 running as a distribution on IOS-XR.

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

scp this RPM onto an IOS-XR router's bash prompt








