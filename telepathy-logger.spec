Summary:	Logging service for Telepathy
Name:		telepathy-logger
Version:	0.1.1
Release:	2
License:	LGPL
Group:		Libraries
Source0:	http://telepathy.freedesktop.org/releases/telepathy-logger/%{name}-%{version}.tar.bz2
# Source0-md5:	76b69c52a53aec8a8d1b5a0f02484a8c
Patch0:		configure.patch
URL:		http://telepathy.freedesktop.org/wiki/Logger
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.8
BuildRequires:	dbus-devel >= 1.1.0
BuildRequires:	dbus-glib-devel >= 0.82
BuildRequires:	glib2-devel >= 1:2.0.0
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils > 0.17.3
BuildRequires:	gtk-doc-automake >= 1.10
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
BuildRequires:	telepathy-glib-devel
Requires:	%{name} = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides Gadu-Gadu functionality for Telepathy.

%description -l pl.UTF-8
Ten pakiet udostępnia funkcjonalność Gadu-Gadu dla Telepathy.

%package apidocs
Summary:	telepathy-logger library API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
telepathy-logger library API documentation.

%package libs
Summary:	telepathy-logger shared libraries
Group:		Libraries

%description libs
telepathy-logger shared libraries.

%package devel
Summary:	Header files for telepathy-logger library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.0.0

%description devel
Header files for telepathy-logger library.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-static \
	--with-html-dir=%{_gtkdocdir}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install telepathy-logger.schemas

%preun
%gconf_schema_uninstall telepathy-logger.schemas

%post libs	-p /sbin/ldconfig
%postun libs	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%attr(755,root,root) %{_bindir}/telepathy-logger
%{_sysconfdir}/gconf/schemas/telepathy-logger.schemas
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Logger.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Logger.service
%{_datadir}/telepathy/clients/TelepathyLogger.client

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/telepathy-logger

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtelepathy-logger.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libtelepathy-logger.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtelepathy-logger.so
%{_includedir}/telepathy-logger
%{_pkgconfigdir}/telepathy-logger.pc
