# TODO: Fix .init cassandra status does not work now.
# TODO: Fix .init stop routine it is now subset of PLD default one
# TODO: Fix of data/ cassandra created dirs/files privilages (now they are all readable)
# TODO: Consider adding
#		cassandra	-	memlock	unlimited
#   to /etc/security/limits.conf ?

%define	shname cassandra
%include	/usr/lib/rpm/macros.java
Summary:	Cassandra database binary package
Summary(pl.UTF-8):	Binarna redystrybucja bazy danych Cassandra
Name:		cassandra-bin
Version:	0.8.8
Release:	1
License:	ASF
Group:		Applications/Databases
# http://www.apache.org/dyn/closer.cgi?path=/cassandra/0.8.7/apache-cassandra-0.8.7-bin.tar.gz
Source0:	http://ftp.tpnet.pl/vol/d1/apache//cassandra/%{version}/apache-cassandra-%{version}-bin.tar.gz
# Source0-md5:	d1469325b888ed5eed1a317f37af1963
Source1:	cassandra.in.sh
Source2:	%{shname}.init
Patch0:		%{name}-jamm_path_fix.patch
URL:		http://cassandra.apache.org/
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Suggests:	java-jna
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cassandra brings together the distributed systems technologies from
Dynamo and the data model from Google's BigTable. Like Dynamo,
Cassandra is eventually consistent. Like BigTable, Cassandra provides
a ColumnFamily-based data model richer than typical key/value systems.

%description -l pl.UTF-8
Cassandra łączy technologie systemów rozproszonych z Dynamo i model
danych z googlowskiego BigTable. Tak jak Dynamo, Cassandra jest
ostatecznie spójna. Tak jak BigTable daje do dyspozycji model danych
oparty na ColumnFamily, bogatszy niż typowe systemy klucza i wartości.

%prep
%setup -q -n apache-cassandra-%{version}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d/,%{_sysconfdir}/%{shname},%{_bindir},%{_sbindir},%{_datadir}/%{shname}} \
	$RPM_BUILD_ROOT/var/{lib/%{shname}/{commitlog,conf,data,saved_caches},{log,run}/%{shname}}

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/cassandra
cp -p bin/{*sstable*,*tool,cassandra-cli} $RPM_BUILD_ROOT%{_bindir}
cp -p bin/cassandra $RPM_BUILD_ROOT%{_sbindir}
cp -p %{SOURCE1} lib/*.jar $RPM_BUILD_ROOT%{_datadir}/%{shname}
cp -p conf/{*.properties,cassandra-env.sh,cassandra.yaml,README.txt} $RPM_BUILD_ROOT/var/lib/%{shname}/conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 259 -r cassandra
%useradd -M -o -r -u 259 -d /var/lib/%{shname} -s /bin/sh -g cassandra -c "Cassandra Server" cassandra

%post
/sbin/chkconfig --add cassandra
%service cassandra restart

%preun
if [ "$1" = "0" ]; then
	%service cassandra stop
	/sbin/chkconfig --del cassandra
fi

%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.txt NEWS.txt NOTICE.txt
%attr(754,root,root) /etc/rc.d/init.d/cassandra
%attr(755,root,root) %{_bindir}/cassandra-cli
%attr(755,root,root) %{_bindir}/nodetool
# %attr(755,root,root) %{_bindir}/clustertool
%attr(755,root,root) %{_bindir}/json2sstable
%attr(755,root,root) %{_bindir}/sstable2json
%attr(755,root,root) %{_bindir}/sstableloader
# %attr(755,root,root) %{_bindir}/schematool
# %attr(755,root,root) %{_bindir}/config-converter
%attr(755,root,root) %{_bindir}/sstablekeys
%attr(755,root,root) %{_sbindir}/cassandra
%{_datadir}/%{shname}
%attr(750,cassandra,cassandra) %dir /var/lib/%{shname}
%attr(750,root,cassandra) %dir /var/lib/%{shname}/conf
%attr(640,root,cassandra) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{shname}/conf/*.properties
%attr(755,root,cassandra) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{shname}/conf/*.sh
%attr(640,root,cassandra) /var/lib/%{shname}/conf/*.txt
%attr(640,root,cassandra) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{shname}/conf/*.yaml
%attr(750,cassandra,cassandra) %dir /var/log/%{shname}
%attr(750,cassandra,cassandra) %dir /var/run/%{shname}
