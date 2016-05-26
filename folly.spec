#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_with	tests		# build with tests

Summary:	Library of C++11 components designed with practicality and efficiency in mind
Name:		folly
Version:	0.57.0
Release:	1
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/facebook/folly/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	226d9dc1b12819c9a53735dc6fa8cc8a
Patch0:		gcc5.patch
URL:		https://github.com/facebook/folly
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.20.0
BuildRequires:	double-conversion-devel
BuildRequires:	gflags-devel
BuildRequires:	glog-devel
%{?with_tests:BuildRequires:	gtest-devel >= 1.6.0}
BuildRequires:	libevent-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	m4
BuildRequires:	openssl-devel
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.583
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		sover	%(echo %{version} | cut -d. -f2)

# missing openssl linking
%define		skip_post_check_so	libfolly.so.%{sover}.0.0

%description
Folly (acronymed loosely after Facebook Open Source Library) is a
library of C++11 components designed with practicality and efficiency
in mind. It complements (as opposed to competing against) offerings
such as Boost and of course std. In fact, we embark on defining our
own component only when something we need is either not available, or
does not meet the needed performance profile.

Performance concerns permeate much of Folly, sometimes leading to
designs that are more idiosyncratic than they would otherwise be (see
e.g. PackedSyncPtr.h, SmallLocks.h). Good performance at large scale
is a unifying theme in all of Folly.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q
%patch0 -p1

#ln -s %{_usrsrc}/gtest folly/test/gtest-1.7.0

%build
cd folly
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}
%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C folly install \
	DESTDIR=$RPM_BUILD_ROOT

# these aren't supposed to be installed!
#rm $RPM_BUILD_ROOT%{_libdir}/libgtest*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_libdir}/libfolly.so.*.*.*
%ghost %{_libdir}/libfolly.so.%{sover}
%attr(755,root,root) %{_libdir}/libfollybenchmark.so.*.*.*
%ghost %{_libdir}/libfollybenchmark.so.%{sover}

%files devel
%defattr(644,root,root,755)
%{_libdir}/libfolly.so
%{_libdir}/libfollybenchmark.so
%{_libdir}/libfolly.la
%{_libdir}/libfollybenchmark.la
%{_includedir}/folly

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfolly.a
%{_libdir}/libfollybenchmark.a
%endif
