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
Version:	2.0.11
Release:	1
License:	ASF
Group:		Applications/Databases
Source0:	ftp://ftp.task.gda.pl/pub/www/apache/dist/cassandra/%{version}/apache-cassandra-%{version}-bin.tar.gz
# Source0-md5:  f8021f9defcdd6957ff78de7c6d5308b
Source1:	cassandra.in.sh
Source2:	%{shname}.init
Source3:	%{name}.tmpfiles
Patch0:		%{name}-jamm_path_fix.patch
Patch1:		%{name}-cqlsh_path_fix.patch
URL:		http://cassandra.apache.org/
BuildRequires:  python-distribute
BuildRequires:	rpm-javaprov
BuildRequires:  rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires(post,preun):	/sbin/chkconfig
Requires:       python-modules
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
%patch1 -p1

%build
# current version of cqlsh supports only python 2.
cd pylib
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d/,%{_sysconfdir}/%{shname},%{_bindir},%{_sbindir},%{_datadir}/%{shname}} \
	$RPM_BUILD_ROOT/var/{lib/%{shname}/{commitlog,conf,data,saved_caches},{log,run}/%{shname}} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/cassandra

rm bin/*.bat
cp -p bin/{cqlsh,*sstable*,*tool,cassandra-cli} $RPM_BUILD_ROOT%{_bindir}
cp -p bin/cassandra $RPM_BUILD_ROOT%{_sbindir}
cp -p %{SOURCE1} lib/*.jar $RPM_BUILD_ROOT%{_datadir}/%{shname}
# use bundled libs for python-cql - from cqlsh doc
cp -p %{SOURCE1} lib/cql-internal-only-1.4.1.zip $RPM_BUILD_ROOT%{_datadir}/%{shname}
cp -p %{SOURCE1} lib/thrift-python-internal-only-0.9.1.zip $RPM_BUILD_ROOT%{_datadir}/%{shname}
cp -p conf/{*.properties,cassandra-env.sh,cassandra.yaml,README.txt} $RPM_BUILD_ROOT/var/lib/%{shname}/conf

install %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{shname}.conf

cd pylib
%{__python} setup.py \
        build --build-base build-2 \
        install --skip-build \
        --optimize=2 \
        --root=$RPM_BUILD_ROOT
cd ..

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
%doc CHANGES.txt LICENSE.txt NEWS.txt NOTICE.txt
%attr(754,root,root) /etc/rc.d/init.d/cassandra
%attr(755,root,root) %{_bindir}/cassandra-cli
%attr(755,root,root) %{_bindir}/cqlsh
%attr(755,root,root) %{_bindir}/nodetool
%attr(755,root,root) %{_bindir}/json2sstable
%attr(755,root,root) %{_bindir}/sstable2json
%attr(755,root,root) %{_bindir}/sstablescrub
%attr(755,root,root) %{_bindir}/sstablekeys
%attr(755,root,root) %{_bindir}/sstableloader
%attr(755,root,root) %{_bindir}/sstablesplit
%attr(755,root,root) %{_bindir}/sstableupgrade
%attr(755,root,root) %{_sbindir}/cassandra
%{_datadir}/%{shname}
%{systemdtmpfilesdir}/%{shname}.conf
%attr(750,cassandra,cassandra) %dir /var/lib/%{shname}
%attr(750,root,cassandra) %dir /var/lib/%{shname}/conf
%attr(640,root,cassandra) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{shname}/conf/*.properties
%attr(755,root,cassandra) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{shname}/conf/*.sh
%attr(640,root,cassandra) /var/lib/%{shname}/conf/*.txt
%attr(640,root,cassandra) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{shname}/conf/*.yaml
%attr(750,cassandra,cassandra) %dir /var/log/%{shname}
%attr(750,cassandra,cassandra) %dir /var/run/%{shname}
%{py_sitescriptdir}/cqlshlib
%if "%{py_ver}" > "2.4"
	%{py_sitescriptdir}/cassandra_pylib-0.0.0-py*.egg-info
%endif
