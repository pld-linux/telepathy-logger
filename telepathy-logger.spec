#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	Logging service for Telepathy
Summary(pl.UTF-8):	Usługa logowania dla Telepathy
Name:		telepathy-logger
Version:	0.8.2
Release:	4
License:	LGPL v2.1+
Group:		Applications
Source0:	https://telepathy.freedesktop.org/releases/telepathy-logger/%{name}-%{version}.tar.bz2
# Source0-md5:	c2f6a31c76cbdf8790500cf4f872ba71
URL:		https://telepathy.freedesktop.org/components/telepathy-logger/
BuildRequires:	autoconf >= 2.66
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel >= 1.1.0
BuildRequires:	dbus-glib-devel >= 0.82
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils > 0.17.3
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	gtk-doc-automake >= 1.10
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool >= 2:2
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.5
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	sqlite3-devel
BuildRequires:	telepathy-glib-devel >= 0.19.2
BuildRequires:	xorg-lib-libICE-devel
Requires(post,postun):	glib2 >= 1:2.28.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus >= 1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides logging service for Telepathy.

%description -l pl.UTF-8
Ten pakiet udostępnia usługę logowania dla Telepathy.

%package libs
Summary:	telepathy-logger shared library
Summary(pl.UTF-8):	Biblioteka telepathy-logger
Group:		Libraries
Requires:	dbus-glib >= 0.82
Requires:	dbus-libs >= 1.1.0
Requires:	glib2 >= 1:2.28.0
Requires:	telepathy-glib >= 0.19.2

%description libs
telepathy-logger shared library.

%description libs -l pl.UTF-8
Biblioteka telepathy-logger.

%package devel
Summary:	Header files for telepathy-logger library
Summary(pl.UTF-8):	Pliki nagłówkowe dla biblioteki telepathy-logger
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-glib-devel >= 0.82
Requires:	glib2-devel >= 1:2.28.0
Requires:	libxml2-devel
Requires:	telepathy-glib-devel >= 0.19.2

%description devel
Header files for telepathy-logger library.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla biblioteki telepathy-logger.

%package static
Summary:	Static telepathy-logger library
Summary(pl.UTF-8):	Statyczna biblioteka telepathy-logger
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static telepathy-logger library.

%description static -l pl.UTF-8
Statyczna biblioteka telepathy-logger.

%package apidocs
Summary:	telepathy-logger library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki telepathy-logger
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
telepathy-logger library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki telepathy-logger.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%attr(755,root,root) %{_libexecdir}/telepathy-logger
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Logger.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Logger.service
%{_datadir}/glib-2.0/schemas/org.freedesktop.Telepathy.Logger.gschema.xml
%{_datadir}/telepathy/clients/Logger.client

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtelepathy-logger.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtelepathy-logger.so.3
%{_libdir}/girepository-1.0/TelepathyLogger-0.2.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtelepathy-logger.so
%{_includedir}/telepathy-logger-0.2
%{_pkgconfigdir}/telepathy-logger-0.2.pc
%{_datadir}/gir-1.0/TelepathyLogger-0.2.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtelepathy-logger.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/telepathy-logger
