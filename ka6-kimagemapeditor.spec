#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.04.0
%define		qtver		6.8.0
%define		kframever	6.13.0
%define		kaname		kimagemapeditor
Summary:	An HTML image map editor
Name:		ka6-%{kaname}
Version:	25.04.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	b95836fe86fdfea8beb534a6908c440a
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-kguiaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An HTML image map editor.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/{sr,zh_CN}

# not supported by glibc yet
%{__rm} -rf $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun


%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc AUTHORS INSTALL NEWS README TODO
%attr(755,root,root) %{_bindir}/kimagemapeditor
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/parts/kimagemapeditorpart.so
%{_desktopdir}/org.kde.kimagemapeditor.desktop
%{_iconsdir}/hicolor/*x*/apps/*.png
%{_iconsdir}/hicolor/*x*/actions/*.png
%{_iconsdir}/hicolor/scalable/apps/kimagemapeditor.svg*
%{_datadir}/kimagemapeditor
%{_datadir}/metainfo/org.kde.kimagemapeditor.appdata.xml
%{_datadir}/qlogging-categories6/kimagemapeditor.categories
