Name:            stockfish
Version:         14
Summary:         Powerful open-source chess engine
License:         GPLv3+
URL:             http://%{name}chess.org

%define istestbuild 0
%define runchecks 0

# Release: pkgrel[.extraver][.snapinfo].DIST[.minorbump]
%define minorbump .taw
%if ! %{istestbuild}
Release:         1%{?dist}%{minorbump}
%else
Release:         0.1.testing%{?dist}%{minorbump}
%endif

%global _vpath_srcdir src
%undefine __cmake_in_source_build

%define _source0_release_tag sf_%{version}
%define _source0_tree Stockfish-%{_source0_release_tag}
Source0:         https://github.com/official-stockfish/Stockfish/archive/%{_source0_release_tag}/%{name}-%{version}.tar.gz

# UCI description text
# Origins: https://www.shredderchess.com/download/div/uci.zip
Source10:       %{name}-uci-interface.txt
# manpage document originates from some past Unbuntu build
Source11:       %{name}.6

# polyglot support
# This file originated from this URL, but the URL no longer points to anything: https://raw.githubusercontent.com/mpurland/stockfish/master/polyglot.ini
Source20:       %{name}-polyglot.ini

# Building with our CMakefile.txt fails for OpenSUSE for some reason. I don't
# know why. Works fine for Fedora and CentOS. So, we elect to fall back to the
# upstream build process. Leave this as 0.
%define buildviacmake 0

%if %{buildviacmake}
# FIXME cmake, https://github.com/official-stockfish/Stockfish/issues/272
Source30:       %{name}-CMakeLists.txt
%endif

# Neural Network datafile
%define nnuedatafile nn-3475407dc199.nnue
# Sourced from https://tests.stockfishchess.org/api/nn/%%{nnuedatafile}
# But we split it up into chunks ( split -n 6 nn-3475407dc199.nnue nn-3475407dc199.nnue- )
# So that we can make github happy with files smaller than 10MB.
Source40:       %{nnuedatafile}-aa
Source41:       %{nnuedatafile}-ab
Source42:       %{nnuedatafile}-ac
Source43:       %{nnuedatafile}-ad
Source44:       %{nnuedatafile}-ae
Source45:       %{nnuedatafile}-af

BuildRequires:  gcc
BuildRequires:  gcc-c++
%if %{buildviacmake}
BuildRequires:  cmake
%endif

Suggests:       polyglot-chess


%description
Stockfish is a free UCI chess engine derived from Glaurung 2.1. It is not a
complete chess program, but requires a UCI-compatible graphical user interface
(GUI) (e.g. PyChess, XBoard with PolyGlot, Scid, Cute Chess, eboard, Arena,
Sigma Chess, Shredder, Chess Partner or Fritz) in order to be used comfortably.
Read the documentation for your GUI of choice for information about how to use
Stockfish with it.


%prep
%setup -q -T -b 0 -n %{_source0_tree}
cp -t. -p %{SOURCE10} %{SOURCE11}

# strip MS-like end-of-line encodings (carriage returns)
sed -i 's,\r$,,' %{name}-uci-interface.txt

# polyglot to match upstream installed binary and disable log
sed -e 's,\(EngineDir = \).*,\1%{_bindir},' \
 -e 's,\(EngineCommand = \).*,\1%{name},' \
 -e 's,\(LogFile = \).*,\1~/,' -e 's,\(LogFile = \).*,\1false,' \
 %{SOURCE20} > polyglot.ini
# strip MS-like end-of-line encodings (carriage returns)
sed -i 's,\r$,,' polyglot.ini

cat %{SOURCE40} %{SOURCE41} %{SOURCE42} %{SOURCE43} %{SOURCE44} %{SOURCE45} > ./src/%{nnuedatafile}
%if %{buildviacmake}
  # Note: _target_platform and _vpath_builddir = x86_64-redhat-linux-gnu
  mkdir -p ./%{_target_platform}/
  mv ./src/%{nnuedatafile} ./%{_target_platform}/
  %if 0%{?fedora:1}
    # brute forcing in order to enable builds on Fedora Rawhide -- this is ugly
    mkdir -p ./redhat-linux-build/
    ln ./%{_target_platform}/%{nnuedatafile} ./redhat-linux-build/
  %endif

  # prep cmake with Fedora compiler flags
  cp -p %{SOURCE30} ./src/CMakeLists.txt
  rm ./src/Makefile
%endif


%build
%if %{buildviacmake}
  CXXFLAGS="%{optflags}" %cmake
  %cmake_build
%else
  cd src
  make net
  CXXFLAGS="%{optflags}" make build ARCH=x86-64-modern
  cd -
%endif


%install
mkdir -p %{buildroot}%{_bindir}
%if ! %{buildviacmake}
  install -m 755 -p %{_vpath_srcdir}/%{name} %{buildroot}%{_bindir}
%else
  # Note: _target_platform and _vpath_builddir = x86_64-redhat-linux-gnu
  install -m 755 -p %{_vpath_builddir}/%{name} %{buildroot}%{_bindir}
%endif
mkdir -p %{buildroot}%{_datadir}/man/man6
cp -p %{name}.6 %{buildroot}%{_datadir}/man/man6
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
cp -p polyglot.ini %{buildroot}%{_sysconfdir}/%{name}


%check
# taken from official Makefile
%if %{runchecks}
  %if ! %{buildviacmake}
    ./%{_vpath_srcdir}/%{name} bench 16 1 1000 default time
  %else
    ./%{_vpath_builddir}/%{name} bench 16 1 1000 default time
  %endif
%endif


%files
%license Copying.txt
%doc AUTHORS %{name}-uci-interface.txt README.md Top*.txt
%{_datadir}/man/man*/%{name}*
%{_bindir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/polyglot.ini


%changelog
* Mon Aug 9 2021 Todd Warner <t0dd@protonmail.com> 14-1.taw
* Mon Aug 9 2021 Todd Warner <t0dd@protonmail.com> 14-0.1.testing.taw
- build from upstream sf_14
- removed source URL references that are no longer valid
- Readme.md is now README.md in this version
- If srpm-supplied CMakeLists.txt has problems, I added a fallback to  
  upstream directed build process. Created a logic branch "buildviacmake"  
  so we can switch between them. OpenSUSE builds needs the fallback.
- Version 14 comes with a neural-net datafile called nn-3475407dc199.nnue (it  
  is frequently updated). This version is 46MB in size. Therefore, I split the  
  data file into 6 chunks so that we can store this thing in github without  
  hassle. We recombine it (via cat) upon build.

* Wed Aug 26 2020 Jeff Law <law@redhat.com> - 11-4
- Do not force C++11 mode

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 02 2020 Raphael Groner <projects.rg@smart.ms> - 11-1
- new version

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Raphael Groner <projects.rg@smart.ms> - 10-1
- new version

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Raphael Groner <projects.rg@smart.ms> - 9-1
- new version

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 10 2017 Raphael Groner <projects.rg@smart.ms> - 8-1
- new version

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7-3.20160225gite1a7d13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7-2.20160225gite1a7d13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Mar 05 2016 Raphael Groner <projects.rg@smart.ms> - 7-1.20160225gite1a7d13
- bump to show official upstream release of sf_7

* Sat Mar 05 2016 Raphael Groner <projects.rg@smart.ms> - 7-0.11.20160225gite1a7d13
- new upstream snapshot

* Wed Feb 03 2016 Raphael Groner <projects.rg@smart.ms> - 7-0.10.20160118gitaedebe3
- new upstream snapshot

* Tue Dec 15 2015 Raphael Groner <projects.rg@smart.ms> - 7-0.9.20151105git76ed0ab
- new upstream snapshot

* Fri Nov 13 2015 Raphael Groner <projects.rg@smart.ms> - 7-0.8.20151105git76ed0ab
- new upstream snapshot

* Sun Oct 11 2015 Raphael Groner <projects.rg@smart.ms> - 7-0.7.20151007git55b46ff
- new upstream snapshot

* Wed Aug 19 2015 Raphael Groner <projects.rg@smart.ms> - 7-0.6.20150817git69a1a80
- new upstream tarball as of 20150817

* Wed Jul 22 2015 Raphael Groner <projects.rg@smart.ms> - 7-0.5.20150716git4095ff0
- new snapshot of upstream

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7-0.4.20150506git2e86d1f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 08 2015 Raphael Groner <projects.rg@smart.ms> - 7-0.3.20150506git2e86d1f
- latest snapshot from upstream

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 7-0.2.20150302gitcb2111f
- Rebuilt for GCC 5 C++11 ABI change

* Mon Mar 02 2015 Raphael Groner <projects.rg@smart.ms> - 7-0.1.20150302gitcb2111f
- prepare next major version bump with latest upstream commit
- merged c++11 branch (upstream)
- disable spinlocks (upstream)
- favour fishtest (upstream)

* Mon Mar 02 2015 Raphael Groner <projects.rg@smart.ms> - 6-4.20150228git1e6d21d
- fix ownership of etc/
- add Suggests: polyglot-chess (rhbz#1197333)
- latest commit from upstream
- merged c++11 branch (upstream)
- disable spinlocks (upstream)
- favour fishtest (upstream)

* Sun Mar 01 2015 Raphael Groner <projects.rg@smart.ms> - 6-3.20150228git1e6d21d
- implement cmake
- harden gcc5
- latest commit from upstream

* Sat Feb 28 2015 Raphael Groner <projects.rg (AT) smart.ms> - 6-2.20150226git8a2c413
- switch to official github sources (as mentioned at homepage)
- provide polyglot support
- disable debuginfo

* Wed Feb 25 2015 Raphael Groner <projects.rg (AT) smart.ms> - 6-1.20150131gitb331768
- bump to version 6 and switch to commits

* Tue Sep 10 2013 Dhiru Kholia <dhiru@openwall.com> - 4-2
- fixed prep section and book path, removed dos2unix call, confirm to FHS
- preserve timestamps for resources, use ExclusiveArch, preserve debug symbols

* Tue Sep 10 2013 Dhiru Kholia <dhiru@openwall.com> - 4-1
- initial version based on stockfish.spec from mageia
