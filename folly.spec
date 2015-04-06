# TODO
# - add testing
#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	Library of C++11 components designed with practicality and efficiency in mind
Name:		folly
Version:	0.26.0
Release:	1
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/facebook/folly/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c76a3fd2e86215d523a9fe18ba9087a1
URL:		https://github.com/facebook/folly/blob/master/folly/docs/Overview.md
BuildRequires:	boost-devel >= 1.20.0
BuildRequires:	double-conversion-devel
BuildRequires:	double-conversion-static
BuildRequires:	gflags-devel
BuildRequires:	glog-devel
BuildRequires:	gtest-devel >= 1.6.0
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.583
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# missing -lopenssl -ldl linking
%define		skip_post_check_so	libfolly.so.26.0.0

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
%doc README LICENSE
%attr(755,root,root) %{_libdir}/libfolly.so.*.*.*
%ghost %{_libdir}/libfolly.so.26
%attr(755,root,root) %{_libdir}/libfollybenchmark.so.*.*.*
%ghost %{_libdir}/libfollybenchmark.so.26

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
