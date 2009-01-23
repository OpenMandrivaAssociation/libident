%define	major 0
%define libname	%mklibname ident %{major}
%define develname %mklibname -d ident

Summary:	New LibIdent C library
Name:		libident
Version:	0.32
Release:	%mkrel 1
Group:		System/Libraries
License:	Public Domain
URL:		http://www.remlab.net/libident/
Source0:	http://www.remlab.net/files/libident/libident-%{version}.tar.bz2
Source1:	xinetd.identtest
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
LibIdent is a small C library for interfacing with RFC 1413 Identification
protocol servers, which are used for identifying users. LibIdent supports both
IPv4 and IPv6 addresses transparently.

It is meant to be used by daemons to try to authenticate users using the Ident
protocol. For this to work, users need to have an Ident server running on the
system from which they are connected.

%package -n	%{libname}
Summary:	New LibIdent C library
Group:		System/Libraries

%description -n	%{libname}
LibIdent is a small C library for interfacing with RFC 1413 Identification
protocol servers, which are used for identifying users. LibIdent supports both
IPv4 and IPv6 addresses transparently.

It is meant to be used by daemons to try to authenticate users using the Ident
protocol. For this to work, users need to have an Ident server running on the
system from which they are connected.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	ident-devel = %{version}-%{release}
Requires:	%{libname} >= %{version}-%{release}

%description -n	%{develname}
LibIdent is a small C library for interfacing with RFC 1413 Identification
protocol servers, which are used for identifying users. LibIdent supports both
IPv4 and IPv6 addresses transparently.

It is meant to be used by daemons to try to authenticate users using the Ident
protocol. For this to work, users need to have an Ident server running on the
system from which they are connected.

This package contains libraries and header files for developing applications
that use %{name}.

%package	tools
Summary:	A small daemon that can be used to test Ident servers
Group:		System/Servers

%description	tools
in.identtestd is a small daemon (to be started from inetd) that does an ident
lookup on you if you telnet into it. Can be used to verify that your Ident
server is working correctly.

%prep

%setup -q
for f in ident.3 README ChangeLog AUTHORS NEWS COPYING; do
	iconv -f ISO-8859-1 -t UTF-8 $f -o $f.new && mv $f.new $f
done

%build
autoreconf -fis
%serverbuild

# to prevent nasty ipv6 surprises
export CFLAGS="$CFLAGS -D_GNU_SOURCE"

%configure2_5x \
    --disable-static \
    --enable-testers

%make

%install
rm -rf %{buildroot}

%makeinstall_std

find %{buildroot} -name '*.la' -exec rm -f {} ';'
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xinetd.d/identtestd

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post tools
if [ -x %{_sbindir}/xinetd ]; then
    /sbin/service xinetd condreload > /dev/null 2>&1 || :
fi

%postun tools
if [ $1 = 0 ]; then
    if [ -x %{_sbindir}/xinetd ]; then
	/sbin/service xinetd condreload > /dev/null 2>&1 || :
    fi
fi

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root,-)
%doc COPYING README AUTHORS ChangeLog NEWS
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/man3/ident.3*

%files tools
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/xinetd.d/identtestd
%{_sbindir}/in.identtestd
%{_mandir}/man8/in.identtestd.8*

