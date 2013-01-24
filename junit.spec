Name:		junit3
Version:	3.8.2
Release:	1
Summary:	Java regression test package
License:	CPL
Url:		http://www.junit.org/
Group:		Development/Java
Source0:	http://osdn.dl.sourceforge.net/junit/junit3.8.2.tar.bz2
Source1:	junit3.8.2-build.xml
Source2:	http://repo1.maven.org/maven2/junit/junit/3.8.2/junit-3.8.2.pom
BuildRequires:	ant
BuildRequires:	java-rpmbuild >= 0:1.6
BuildRequires:	java-1.6.0-openjdk-devel
BuildArch:      noarch

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
%setup -q -n junit%{version}
# extract sources
%{jar} xf src.jar
rm -f src.jar
cp %{SOURCE1} build.xml

%build
export JAVA_HOME=%_prefix/lib/jvm/java-1.6.0
ant dist

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 junit%{version}/junit.jar %{buildroot}%{_javadir}/junit-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
%add_to_maven_depmap junit junit %{version} JPP junit
# pom 	 
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms 	 
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/maven2/poms/JPP-junit.pom
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/junit
cp -pr junit%{version}/javadoc/* %{buildroot}%{_javadocdir}/junit
# demo
install -d -m 755 %{buildroot}%{_datadir}/junit/demo/junit
cp -pr junit%{version}/junit/* %{buildroot}%{_datadir}/junit/demo/junit

# fix end-of-line 	 
%{__perl} -pi -e 's/\r\n/\n/g' README.html

for i in `find junit%{version}/doc -type f -name "*.htm*"`; do
    %{__perl} -pi -e 's/\r\n/\n/g' $i
done 	 

for i in `find $RPM_BUILD_ROOT%{_datadir}/junit -type f -name "*.java"`; do
    %{__perl} -pi -e 's/\r\n/\n/g' $i
done

install -d -m 755 %{buildroot}%{_docdir}/junit
cp -p README.html %{buildroot}%{_docdir}/junit
cp -par doc/* %{buildroot}%{_docdir}/junit

%post 	 
%update_maven_depmap 	 

%postun 	 
%update_maven_depmap 	 

%files
%defattr(-,root,root,-)
%{_javadir}/*
%doc %dir %{_docdir}/junit
%doc %{_docdir}/junit/README.html
%{_datadir}/maven2
%{_mavendepmapfragdir}

%files manual
%defattr(-,root,root,-)
%doc %{_docdir}/junit
%exclude %{_docdir}/junit/README.html

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/junit

%files demo
%defattr(-,root,root,-)
%{_datadir}/junit


%changelog
* Sat May 14 2011 Oden Eriksson <oeriksson@mandriva.com> 3.8.2-8mdv2011.0
+ Revision: 674492
- rebuild

* Tue Apr 26 2011 Paulo Andrade <pcpa@mandriva.com.br> 3.8.2-7
+ Revision: 659395
- Revert previous change as now it builds with patched aot-compile-rpm

* Mon Apr 25 2011 Paulo Andrade <pcpa@mandriva.com.br> 3.8.2-6
+ Revision: 659060
- Update and rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:3.8.2-5.0.2mdv2009.1
+ Revision: 351316
- rebuild

* Mon Feb 18 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:3.8.2-5.0.1mdv2008.1
+ Revision: 171757
- add pom and depmap fragment

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:3.8.2-4.3.2mdv2008.1
+ Revision: 120954
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sun Dec 09 2007 Alexander Kurtakov <akurtakov@mandriva.org> 0:3.8.2-4.3.1mdv2008.1
+ Revision: 116688
- remove javadoc post/postun

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:3.8.2-1.4mdv2008.0
+ Revision: 87450
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Fri Sep 14 2007 Pascal Terjan <pterjan@mandriva.org> 0:3.8.2-1.3mdv2008.0
+ Revision: 85729
- Fix build and rebuild for new gcj


* Thu Mar 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 3.8.2-1.2mdv2007.1
+ Revision: 144260
- rebuild for 2007.1
- Import junit

* Sun Jul 23 2006 David Walluck <walluck@mandriva.org> 0:3.8.2-1.1mdv2007.0
- 3.8.2

* Fri Jun 02 2006 David Walluck <walluck@mandriva.org> 0:3.8.1-4.2mdv2006.0
- rebuild for libgcj.so.7
- aot compile

* Sun May 08 2005 David Walluck <walluck@mandriva.org> 0:3.8.1-4.1mdk
- release

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:3.8.1-4jpp
- Rebuild with ant-1.6.2

