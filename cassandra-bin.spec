# TODO: Fix of data/ cassandra created dirs/files privilages (now they are all readable)
# TODO: Consider adding
#		cassandra	-	memlock	unlimited
#   to /etc/security/limits.conf ?
# TODO: C java-jna is only valid with openjdk8-jre ?
#   cassandra running java from openjdk8-jre-8u66.b02-2.x86_64  fails with  java-jna-4.2.1-1.x86_64 but without clamis JNA to work in logs

%define	shname cassandra
Summary:	Cassandra database binary package
Summary(pl.UTF-8):	Binarna redystrybucja bazy danych Cassandra
Name:		cassandra-bin
Version:	4.1.3
Release:	4
License:	ASF
Group:		Applications/Databases
Source0:	https://dlcdn.apache.org/cassandra/%{version}/apache-cassandra-%{version}-bin.tar.gz
# Source0-md5:	f2f148d0c7af65375caedb074dde93d1
Source1:	cassandra.in.sh
Source3:	%{name}.tmpfiles
Source4:	%{shname}.service
Patch0:		%{name}-jamm_path_fix.patch
Patch3:		%{name}-pld-env.patch
URL:		http://cassandra.apache.org/
BuildRequires:	python-distribute
BuildRequires:	rpm-javaprov
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
Requires(post,preun,postun):	systemd-units >= 38
Requires:	jre >= 1.7
Requires:	python
Requires:	python-modules
Requires:	systemd-units >= 0.38
Provides:	group(cassandra)
Provides:	user(cassandra)
Conflicts:	java-jna
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
%patch -P 0 -p1
%patch -P 3 -p1
# Fix logging dir
%{__sed} -i -e 's#$CASSANDRA_HOME/logs#/var/log/cassandra#g' bin/cassandra

%build
# current version of cqlsh supports only python 2.
cd pylib
%py3_build %{?with_tests:test}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{shname},%{_bindir},%{_sbindir},%{_datadir}/%{shname}} \
	$RPM_BUILD_ROOT/var/{lib/%{shname}/{commitlog,conf,data,saved_caches},{log,run}/%{shname}} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir} $RPM_BUILD_ROOT/%{systemdunitdir}

cp -p %{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}/%{shname}.service

cp -p bin/{cqlsh*,*sstable*,*tool} $RPM_BUILD_ROOT%{_bindir}
cp -p bin/cassandra $RPM_BUILD_ROOT%{_sbindir}
cp -p %{SOURCE1} lib/*.jar $RPM_BUILD_ROOT%{_datadir}/%{shname}
# use bundled libs for python-cql - from cqlsh doc
# cp -p %{SOURCE1} lib/cql-internal-only-1.4.2.zip $RPM_BUILD_ROOT%{_datadir}/%{shname}
# cp -p %{SOURCE1} lib/thrift-python-internal-only-0.9.1.zip $RPM_BUILD_ROOT%{_datadir}/%{shname}
cp -p %{SOURCE1} lib/*.zip $RPM_BUILD_ROOT%{_datadir}/%{shname}
cp -p conf/{*.properties,*.yaml,*.xml,cassandra-env.sh,hotspot_compiler,README.txt} $RPM_BUILD_ROOT/var/lib/%{shname}/conf
install -d $RPM_BUILD_ROOT/var/lib/%{shname}/conf/triggers
cp -p conf/triggers/*.txt  $RPM_BUILD_ROOT/var/lib/%{shname}/conf/triggers
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{shname}.conf

cd pylib
%py3_install
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 259 -r cassandra
%useradd -M -o -r -u 259 -d /var/lib/%{shname} -s /bin/sh -g cassandra -c "Cassandra Server" cassandra

%post
%systemd_post %{shname}.service

%preun
%systemd_preun %{shname}.service

%postun
%systemd_reload
if [ "$1" = "0" ]; then
	%userremove cassandra
	%groupremove cassandra
fi

%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt NEWS.txt NOTICE.txt
%attr(755,root,root) %{_bindir}/cqlsh
%{_bindir}/cqlsh.py
%attr(755,root,root) %{_bindir}/nodetool
%attr(755,root,root) %{_bindir}/sstablescrub
%attr(755,root,root) %{_bindir}/sstableloader
%attr(755,root,root) %{_bindir}/sstableupgrade
%attr(755,root,root) %{_bindir}/sstableutil
%attr(755,root,root) %{_bindir}/sstableverify
%attr(755,root,root) %{_sbindir}/cassandra
%{_datadir}/%{shname}
%{systemdunitdir}/%{shname}.service
%{systemdtmpfilesdir}/%{shname}.conf
%attr(750,cassandra,cassandra) %dir /var/lib/%{shname}
%attr(750,root,cassandra) %dir /var/lib/%{shname}/conf
%attr(640,root,cassandra) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{shname}/conf/*.properties
%attr(755,root,cassandra) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{shname}/conf/*.sh
%attr(640,root,cassandra) /var/lib/%{shname}/conf/*.txt
%attr(640,root,cassandra) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{shname}/conf/*.yaml
%attr(640,root,cassandra) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{shname}/conf/*.xml
%attr(640,root,cassandra) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{shname}/conf/hotspot_compiler
%attr(750,cassandra,cassandra) %dir /var/lib/%{shname}/conf/triggers
%attr(640,root,cassandra) /var/lib/%{shname}/conf/triggers/*.txt

%attr(750,cassandra,cassandra) %dir /var/log/%{shname}
%attr(750,cassandra,cassandra) %dir /var/run/%{shname}
%{py3_sitedir}/cqlshlib
%{py3_sitedir}/cassandra_pylib-0.0.0-py*.egg-info
