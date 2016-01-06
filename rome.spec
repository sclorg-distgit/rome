%{?scl:%scl_package rome}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

Name:       %{?scl_prefix}rome
Version:    0.9
Release:    19%{?dist}
Summary:    RSS and Atom Utilities

Group:      Development/Libraries
License:    ASL 2.0
URL:        https://rome.dev.java.net/
# wget https://rome.dev.java.net/source/browse/*checkout*/rome/www/dist/rome-0.9-src.tar.gz?rev=1.1
Source0:    %{pkg_name}-%{version}-src.tar.gz
# wget http://download.eclipse.org/tools/orbit/downloads/drops/R20090825191606/bundles/com.sun.syndication_0.9.0.v200803061811.jar
# unzip com.sun.syndication_0.9.0.v200803061811.jar META-INF/MANIFEST.MF
# sed -i 's/\r//' META-INF/MANIFEST.MF
# # We won't have the same SHA-1 sums (class sometimes spills into # cl\nass)
# sed -i -e "/^Name/d" -e "/^SHA/d" -e "/^\ ass$/d" -e "/^$/d" META-INF/MANIFEST.MF
Source1:    MANIFEST.MF
Source2:    http://repo1.maven.org/maven2/%{pkg_name}/%{pkg_name}/%{version}/%{pkg_name}-%{version}.pom
BuildArch:  noarch

Patch0:     %{pkg_name}-%{version}-addosgimanifest.patch
# fix maven-surefire-plugin aId
Patch1:     %{pkg_name}-%{version}-pom.patch

BuildRequires:  java-devel >= 1:1.7.0
BuildRequires:  %{?scl_prefix_java_common}jpackage-utils
BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  %{?scl_prefix_java_common}jdom >= 1.1.2-3
Requires: %{?scl_prefix_java_common}jdom >= 1.1.2-3
%{?scl:Requires: %scl_runtime}

%description
ROME is an set of open source Java tools for parsing, generating and
publishing RSS and Atom feeds.

%package	javadoc
Summary:  Javadocs for %{pkg_name}
Group:    Documentation

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
find -name '*.jar' -o -name '*.class' -exec rm -f '{}' \;
mkdir -p target/lib
cp -p %{SOURCE1} .
%patch0
cp -p %{SOURCE2} pom.xml
%patch1

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
build-jar-repository -p target/lib jdom
ant -Dnoget=true dist
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p target/%{pkg_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}.jar

mkdir -p $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{pkg_name}.pom
%add_maven_depmap JPP-%{pkg_name}.pom %{pkg_name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}
cp -rp dist/docs/api/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}
%{?scl:EOF}

%files -f .mfiles
%{_javadir}/%{pkg_name}.jar
%{_mavenpomdir}/JPP-%{pkg_name}.pom

%files javadoc
%{_javadocdir}/%{pkg_name}

%changelog
* Mon May 11 2015 Mat Booth <mat.booth@redhat.com> - 0.9-19
- Resolves: rhbz#1219013 - Fails to build from source

* Tue May 27 2014 Mat Booth <mat.booth@redhat.com> - 0.9-18
- java-headless is not available on rhel6

* Tue May 27 2014 Alexander Kurtakov <akurtako@redhat.com> 0.9-17
- Fix javadoc subpackage requires.

* Mon May 26 2014 Sami Wagiaalla <swagiaal@redhat.com> 0.9-16
- Build for DTS 3.

* Fri Feb 21 2014 Alexander Kurtakov <akurtako@redhat.com> 0.9-15
- Require java-headless.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 gil cattaneo <puntogil@libero.it> 0.9-11
- Added maven POM

* Tue Apr 17 2012 Alexander Kurtakov <akurtako@redhat.com> 0.9-10
- Adapt to current guidelines.

* Fri Apr 13 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.9-9
- Use Java 7
- Use latest jdom

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0.9-6
- Fix build with latest jdom. (rhbz#565057)

* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0.9-5
- Update URL in instructions for getting MANIFEST.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 30 2009 Andrew Overholt <overholt@redhat.com> 0.9-3
- Fix javadoc Group (rhbz#492761).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 25 2008 Andrew Overholt <overholt@redhat.com> 0.9-1
- Initial Fedora version
