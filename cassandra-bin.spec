%include	/usr/lib/rpm/macros.java
# TODO: Fix .init  cassandra status does not work now.

Summary:	Cassandra database binary package.
Summary(pl.UTF-8):	Baza danych Cassandra wersja binarna
Name:		cassandra-bin
%define     shname cassandra
Version:	0.7.0
%define     rccode rc3
Release:	0.%{rccode}.0.1
License:	ASF
Group:		Applications/Databases
Source0:	http://mirror.nyi.net/apache//cassandra/%{version}/apache-cassandra-%{version}-%{rccode}-bin.tar.gz
# Source0-md5:	8e5cfc07178cd57e05ef81cad18ef170
Source1:    cassandra.in.sh
Source2:    %{shname}.init
URL:		http://cassandra.apache.org/
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cassandra brings together the distributed systems technologies from Dynamo
and the data model from Google's BigTable. Like Dynamo, Cassandra is
eventually consistent. Like BigTable, Cassandra provides a ColumnFamily-based
data model richer than typical key/value systems.

%description -l pl.UTF-8
TODO

%prep
%setup -q -n apache-cassandra-%{version}-%{rccode}

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{shname}/
mkdir -p $RPM_BUILD_ROOT/usr/share/%{shname}
# /usr/share/%{shname}/conf -> /etc/%{shname}/ - We do not want that , lets be ale to use many instances of cassandra like we do with postgresql
# TODO: /usr/share/%{shname}/conf -> /var/lib/cassandra/conf
# TODO: root:cassandra conf/*
# mkdir -p $RPM_BUILD_ROOT/usr/share/%{shname}/conf
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d/
cp -p %{SOURCE1}  $RPM_BUILD_ROOT/usr/share/%{shname}
# cp -p contrib/redhat/%{name} $RPM_BUILD_ROOT/etc/rc.d/init.d/
cp -p lib/*.jar $RPM_BUILD_ROOT/usr/share/%{shname}
mkdir -p $RPM_BUILD_ROOT/usr/sbin
cp -p bin/cassandra $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp -p bin/cassandra-cli $RPM_BUILD_ROOT/usr/bin
cp -p bin/nodetool $RPM_BUILD_ROOT/usr/bin
cp -p bin/clustertool $RPM_BUILD_ROOT/usr/bin
cp -p bin/json2sstable $RPM_BUILD_ROOT/usr/bin
cp -p bin/sstable2json $RPM_BUILD_ROOT/usr/bin
cp -p bin/schematool $RPM_BUILD_ROOT/usr/bin
cp -p bin/config-converter $RPM_BUILD_ROOT/usr/bin
cp -p bin/sstablekeys $RPM_BUILD_ROOT/usr/bin
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/cassandra
mkdir -p $RPM_BUILD_ROOT/var/lib/%{shname}/commitlog
mkdir -p $RPM_BUILD_ROOT/var/lib/%{shname}/data
mkdir -p $RPM_BUILD_ROOT/var/lib/%{shname}/saved_caches
mkdir -p $RPM_BUILD_ROOT/var/lib/%{shname}/conf
cp -p conf/log4j-server.properties $RPM_BUILD_ROOT/var/lib/%{shname}/conf
cp -p conf/cassandra.yaml $RPM_BUILD_ROOT/var/lib/%{shname}/conf
cp -p conf/cassandra-env.sh $RPM_BUILD_ROOT/var/lib/%{shname}/conf
cp -p conf/access.properties $RPM_BUILD_ROOT/var/lib/%{shname}/conf
cp -p conf/passwd.properties $RPM_BUILD_ROOT/var/lib/%{shname}/conf
cp -p conf/cassandra-topology.properties $RPM_BUILD_ROOT/var/lib/%{shname}/conf
cp -p conf/README.txt $RPM_BUILD_ROOT/var/lib/%{shname}/conf
mkdir -p $RPM_BUILD_ROOT/var/run/%{shname}
mkdir -p $RPM_BUILD_ROOT/var/log/%{shname}


%clean
rm -rf $RPM_BUILD_ROOT

%pre
# TODO:
%groupadd -g 259 -r cassandra
%useradd -M -o -r -u 259 -d /var/lib/%{shname} -s /bin/sh -g cassandra -c "Cassandra Server" cassandra

# TODO:
%preun
if [ "$1" = "0" ]; then
    %service cassandra stop
    /sbin/chkconfig --del cassandra
fi

# %post upstart
# %upstart_post cassandra

# %postun upstart
# %upstart_postun cassandra



%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.txt NEWS.txt NOTICE.txt
%attr(754,root,root) /etc/rc.d/init.d/cassandra
%attr(755,root,root) %{_bindir}/cassandra-cli
%attr(755,root,root) %{_bindir}/nodetool
%attr(755,root,root) %{_bindir}/clustertool
%attr(755,root,root) %{_bindir}/json2sstable
%attr(755,root,root) %{_bindir}/sstable2json
%attr(755,root,root) %{_bindir}/schematool
%attr(755,root,root) %{_bindir}/config-converter
%attr(755,root,root) %{_bindir}/sstablekeys
%attr(755,root,root) %{_sbindir}/cassandra
# %attr(755,root,root) /etc/rc.d/init.d/%{name}
# %attr(754,root,root) /etc/rc.d/init.d/postgresql
# %attr(755,root,root) 
/usr/share/%{shname}
%attr(750,cassandra,cassandra) %dir /var/lib/%{shname}
%attr(750,root,cassandra) %dir /var/lib/%{shname}/conf
%attr(640,root,cassandra) /var/lib/%{shname}/conf/*.yaml
%attr(640,root,cassandra) /var/lib/%{shname}/conf/*.txt
%attr(640,root,cassandra) /var/lib/%{shname}/conf/*.properties
%attr(755,root,cassandra) /var/lib/%{shname}/conf/*.sh
%attr(750,cassandra,cassandra) %dir /var/run/%{shname}
%attr(750,cassandra,cassandra) %dir /var/log/%{shname}
