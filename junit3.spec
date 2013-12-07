Summary:	Java regression test package
Name:		junit3
Version:	3.8.2
Release:	6
License:	CPL
Group:		Development/Java
Url:		http://www.junit.org/
Source0:	http://osdn.dl.sourceforge.net/junit/junit3.8.2.tar.bz2
Source1:	junit3.8.2-build.xml
Source2:	http://repo1.maven.org/maven2/junit/junit/3.8.2/junit-3.8.2.pom
BuildArch:	noarch
BuildRequires:	ant
BuildRequires:	java-rpmbuild >= 0:1.6
BuildRequires:	java-1.6.0-openjdk-devel

%description
JUnit is a regression testing framework written by Erich Gamma and Kent
Beck. It is used by the developer who implements unit tests in Java.
JUnit is Open Source Software, released under the IBM Public License and
hosted on SourceForge.

%package manual
Group:		Development/Java
Summary:	Manual for %{name}

%description manual
Documentation for %{name}.

%package javadoc
Group:		Development/Java
Summary:	Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package demo
Group:		Development/Java
Summary:	Demos for %{name}
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -qn junit%{version}
# extract sources
%{jar} xf src.jar
rm -f src.jar
cp %{SOURCE1} build.xml

%build
export JAVA_HOME=%{_prefix}/lib/jvm/java-1.6.0
ant dist

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 junit%{version}/junit.jar %{buildroot}%{_javadir}/junit-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
mv %buildroot%_javadir/junit.jar %buildroot%_javadir/junit3.jar
%add_to_maven_depmap junit3 junit3 %{version} JPP junit3
# pom 	 
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms 	 
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/maven2/poms/JPP-junit3.pom
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/junit3
cp -pr junit%{version}/javadoc/* %{buildroot}%{_javadocdir}/junit3
# demo
install -d -m 755 %{buildroot}%{_datadir}/junit3/demo/junit
cp -pr junit%{version}/junit/* %{buildroot}%{_datadir}/junit3/demo/junit

# fix end-of-line 	 
sed -i -e 's/\r\n/\n/g' README.html

for i in `find junit%{version}/doc -type f -name "*.htm*"`; do
	sed -i -e 's/\r\n/\n/g' $i
done 	 

for i in `find $RPM_BUILD_ROOT%{_datadir}/junit -type f -name "*.java"`; do
	sed} -i -e 's/\r\n/\n/g' $i
done

install -d -m 755 %{buildroot}%{_docdir}/junit3
cp -p README.html %{buildroot}%{_docdir}/junit3
cp -par doc/* %{buildroot}%{_docdir}/junit3

%post 	 
%update_maven_depmap 	 

%postun 	 
%update_maven_depmap 	 

%files
%{_javadir}/*
%doc %dir %{_docdir}/junit3
%doc %{_docdir}/junit3/README.html
%{_datadir}/maven2
%{_mavendepmapfragdir}

%files manual
%doc %{_docdir}/junit3
%exclude %{_docdir}/junit3/README.html

%files javadoc
%{_javadocdir}/junit3

%files demo
%{_datadir}/junit3

