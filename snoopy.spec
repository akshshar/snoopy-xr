Name:		snoopy
Version:	2.4.6
Release:        XR_6.2.2	
Summary:	User monitoring and command logging
Group:		Applications/Monitoring
License:	GPL
URL:		https://github.com/a2o/%{name}
Source0:	http://10.30.110.215:9090/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  autoconf, automake, git, gcc, libtool, make, socat

%description
Snoopy is a tiny library that logs all executed commands (+ arguments) on your system.

%prep
%setup -q 
%build
%configure --enable-everything
%{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR=%{buildroot}
echo '%{_prefix}/$LIB/lib%{name}.so' >> %{buildroot}%{_sysconfdir}/ld.so.preload
for i in enable disable;
do
  %{__mv} -f %{buildroot}%{_sbindir}/%{name}-${i} \
             %{buildroot}%{_sbindir}/%{name}-${i}.%{_arch}
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README.md contrib
%doc doc/*.md doc/internals/*.md
%config(noreplace) %{_sysconfdir}/ld.so.preload
%config(noreplace) %{_sysconfdir}/%{name}.ini
%{_bindir}/%{name}-*
%{_libdir}/lib%{name}.*
%{_sbindir}/%{name}-*

%changelog
* Sun Feb 26 2017 Taylor Kimball <taylor@linuxhq.org> - 2.4.6-1
- Updated to version 2.4.6.

* Thu Apr 21 2016 Taylor Kimball <taylor@linuxhq.org> - 2.4.5-1 
- Updated to version 2.4.5.

* Wed Feb 03 2016 Taylor Kimball <taylor@linuxhq.org> - 2.4.4-1
- Updated to version 2.4.4.

* Fri Sep 11 2015 Taylor Kimball <taylor@linuxhq.org> - 20150911gitbe2df69-1
- Update commit to be2df69 

* Thu Sep 10 2015 Taylor Kimball <taylor@linuxhq.org> - 20150824git51914ec-3
- Remove Werror compilation flag for el5 

* Wed Sep 09 2015 Taylor Kimball <taylor@linuxhq.org> - 20150824git51914ec-2
- Add support for multilib

* Mon Aug 24 2015 Taylor Kimball <taylor@linuxhq.org> - 20150824git51914ec-1  
- Spec file refactor with latest update

* Sat Feb 28 2015 Taylor Kimball <taylor@linuxhq.org> - 2.2.6-1
- Initial spec.
