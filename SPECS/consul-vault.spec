%if 0%{?_version:1}
%define         _verstr      %{_version}
%else
%define         _verstr      1.7.1
%endif

Name:           consul-vault
Version:        %{_verstr}
Release:        1%{?dist}
Summary:        Consul agent for Vault storage

Group:          System Environment/Daemons
License:        MPLv2.0
URL:            http://www.consul.io
Source0:        https://releases.hashicorp.com/consul/%{version}/consul_%{version}_linux_amd64.zip
Source1:        %{name}.sysconfig
Source2:        %{name}.service
Source3:        %{name}.init
Source4:        %{name}.hcl
Source5:        %{name}.logrotate
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
BuildRequires:  systemd-units
Requires:       systemd
%else
Requires:       logrotate
%endif
Requires(pre): shadow-utils


%description
Consul agent for Vault storage

Consul provides several key features:
 - Key/Value Storage - A flexible key/value store enables storing dynamic configuration, feature flagging, coordination, leader election and more. The simple HTTP API makes it easy to use anywhere.

%prep
%setup -q -c

%install
mkdir -p %{buildroot}/%{_bindir}
cp consul %{buildroot}/%{_bindir}/consul-vault
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}.d
cp %{SOURCE4} %{buildroot}/%{_sysconfdir}/%{name}.d/consul-vault.hcl
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
mkdir -p %{buildroot}/%{_unitdir}
cp %{SOURCE2} %{buildroot}/%{_unitdir}/
%else
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d
cp %{SOURCE3} %{buildroot}/%{_initrddir}/consul-vault
cp %{SOURCE5} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}
%endif

%pre
getent group consul-vault >/dev/null || groupadd -r consul-vault
getent passwd consul-vault >/dev/null || \
    useradd -r -g consul-vault -d /var/lib/consul-vault -s /sbin/nologin \
    -c "consul.io user" consul-vault
exit 0

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%else
%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %attr(750, root, consul-vault) %{_sysconfdir}/%{name}.d
%attr(640, root, consul-vault) %{_sysconfdir}/%{name}.d/consul-vault.hcl
%dir %attr(750, consul-vault, consul-vault) %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%endif
%attr(755, root, root) %{_bindir}/consul-vault



%doc


%changelog
* Thu Apr 02 2020 John Byrne <john@johnbyrne.io> - 1.7.1-1
- Initial Release
