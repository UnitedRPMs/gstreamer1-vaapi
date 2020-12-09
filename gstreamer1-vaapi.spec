%global gitdate 20191204
%global commit0 153325f39ab6b94fd9f607cd33986132a00459ea
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:           gstreamer1-vaapi
Version:        1.18.2
Release:        7%{?gver}%{dist}
Summary:        GStreamer plugins to use VA API video acceleration

License:        LGPLv2+
URL:            https://cgit.freedesktop.org/gstreamer/gstreamer-vaapi
Source0: 	https://github.com/GStreamer/gstreamer-vaapi/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  glib2-devel >= 2.32
BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}
BuildRequires:  gstreamer1-plugins-bad-free-devel >= %{version}
BuildRequires:  libva-devel >= 1.1.0
BuildRequires:  libdrm-devel
BuildRequires:  libudev-devel
BuildRequires:  libGL-devel
BuildRequires:  pkgconfig(egl)
BuildRequires:  libvpx-devel
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:	git
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	gcc-c++
BuildRequires:	meson
BuildRequires:	cmake
BuildRequires:	pkgconfig(gtk+-3.0)

# documentation
BuildRequires:  gtk-doc
BuildRequires:  python-devel
#

%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-client)  >= 1
BuildRequires:  pkgconfig(wayland-scanner) >= 1
BuildRequires:  pkgconfig(wayland-cursor)  >= 1
BuildRequires:  pkgconfig(wayland-egl)     >= 1
BuildRequires:  pkgconfig(wayland-server)  >= 1
%endif

# We can't provide encoders or decoders unless we know what VA-API drivers
# are on the system. Just filter them out, so they're not suggested by
# PackageKit et al.
%global __provides_exclude gstreamer1\\(decoder|gstreamer1\\(encoder

%description
A collection of GStreamer plugins to let you make use of VA API video
acceleration from GStreamer applications.

Includes elements for video decoding, display, encoding and post-processing
using VA API (subject to hardware limitations).

%package        devel-docs
Summary:        Developer documentation for GStreamer VA API video acceleration plugins
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

Provides:       gstreamer1-vaapi-devel = %{version}-%{release}
Obsoletes:      gstreamer1-vaapi-devel < 0.6.1-3

%description	devel-docs
The %{name}-devel-docs package contains developer documentation
for the GStreamer VA API video acceleration plugins

%prep
%autosetup -n gstreamer-vaapi-%{commit0} 
rm -rf common && git clone git://anongit.freedesktop.org/gstreamer/common  

%build


%meson \
    -D package-name="gst-plugins-bad 1.0 unitedrpms rpm" \
    -D package-origin="https://unitedrpms.github.io" \
    -D doc=disabled -D sidplay=disabled

%meson_build 


%install
%meson_install 

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB NEWS README
%{_libdir}/gstreamer-1.0/*.so

%files devel-docs
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB NEWS README


%changelog

* Mon Dec 07 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.2-7.git153325f
- Updated to 1.18.2-7.git153325f

* Thu Oct 29 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.1-7.gitf9e925a
- Updated to 1.18.1-7.gitf9e925a

* Mon Sep 28 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.18.0-7.gitde6fb60
- Updated to 1.18.0-7.gitde6fb60

* Sun Sep 06 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.17.90-7.git0320e7a
- Updated to 1.17.90-7.git0320e7a

* Wed Dec 04 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.2-7.git20d8691
- Updated to 1.16.2-7.git20d8691

* Fri Apr 19 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.1-7.gitb6a3bef
- Updated to 1.16.1-7.gitb6a3bef

* Fri Apr 19 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.16.0-7.git2c34807
- Updated to 1.16.0-7.git2c34807

* Wed Feb 27 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.15.2-7.git3fa74d7
- Updated to 1.15.2-7.git3fa74d7

* Fri Jan 18 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.15.1-7.gitd158e78
- Updated to 1.15.1-7.gitd158e78

* Wed Oct 03 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.4-7.git8b1b1f4
- Updated to 1.14.4-7.git8b1b1f4

* Mon Sep 17 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.3-7.git295859a
- Updated to 1.14.3-7.git295859a

* Fri Jul 20 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.2-7.gitbc395f9
- Updated to 1.14.2-7.gitbc395f9

* Mon May 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.1-7.git6f879bb
- Updated to 1.14.1-7.git6f879bb

* Wed Mar 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.14.0-7.git67ebe1f
- Updated to 1.14.0-7.git67ebe1f

* Sun Mar 04 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 1.13.90-7.gitf6f981e  
- Updated to 1.13.90-7.gitf6f981e

* Tue Jan 16 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.4-8.gite540e08
- Rebuilt for libva 2.0

* Fri Dec 08 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.4-7-gite540e08
- Updated to 1.12.4-7-gite540e08

* Mon Sep 18 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.3-7-git8d2884e
- Updated to 1.12.3-7.git8d2884e

* Thu Jul 20 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.2-2.git3df7d3d
- Updated to 1.12.2-2.git3df7d3d

* Sat Jun 24 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 1.12.1-2.gitd005456
- Updated to 1.12.1-2.gitd005456

* Tue Jun 20 2017 Taymans <wtaymans@redhat.com> - 1.12.1-1
- Update to 1.12.1

* Wed May 10 2017 Taymans <wtaymans@redhat.com> - 1.12.0-1
- Update to 1.12.0

* Fri Apr 28 2017 Taymans <wtaymans@redhat.com> - 1.11.91-1
- Update to 1.11.91

* Tue Apr 11 2017 Taymans <wtaymans@redhat.com> - 1.11.90-1
- Update to 1.11.90

* Fri Feb 24 2017 Taymans <wtaymans@redhat.com> - 1.11.2-1
- Update to 1.11.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 13 2017 Taymans <wtaymans@redhat.com> - 1.11.1-1
- Update to 1.11.1

* Mon Dec 05 2016 Taymans <wtaymans@redhat.com> - 1.10.2-1
- Update to 1.10.2

* Mon Nov 28 2016 Taymans <wtaymans@redhat.com> - 1.10.1-1
- Update to 1.10.1

* Thu Nov 03 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Sat Oct 01 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.90-1
- Update to 1.9.90

* Thu Sep 01 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.2-1
- Update to 1.9.2

* Thu Jul 07 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.1-1
- Update to 1.9.1

* Thu Jun 09 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.2-1
- Update to 1.8.2

* Mon Apr 25 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Fri Apr 08 2016 Egor Zaharov <nexfwall@gmail.com> - 1.8.0-1
- Updated to 1.8.0
- Update URL to follow project, because they moved to freedesktop

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 30 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.6.1-1
- Update to 0.6.1

* Sat Jul 18 2015 Francesco Frassinelli <fraph24@gmail.com> - 0.6.0-1
- Update to 0.6.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr  7 2015 Simon Farnsworth <simon.farnsworth@onelan.co.uk> - 0.5.10-3
- Update URL to follow project after gitorious shutdown

* Sun Feb 15 2015 Simon Farnsworth <simon.farnsworth@onelan.co.uk> - 0.5.10-2
- Fix FTBFS on s390x due to header file not matching implementation

* Tue Feb  3 2015 Simon Farnsworth <simon@farnz.org.uk> - 0.5.10-1
- Update to 0.5.10 release
- Filter out encoder and decoder Provides

* Tue Nov 04 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.5.9-3
- Rebuilt for vaapi 0.36

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug  1 2014 Simon Farnsworth <simon.farnsworth@onelan.co.uk> - 0.5.9-1
- Update to 0.5.9 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr  9 2014 Simon Farnsworth <simon.farnsworth@onelan.co.uk> - 0.5.8-4
- Provide Wayland support now that libva includes it

* Fri Feb  7 2014 Simon Farnsworth <simon@farnz.org.uk> - 0.5.8-3
- Fix typo in spec file - Patch1 and %patch0 don't go together

* Fri Feb  7 2014 Simon Farnsworth <simon@farnz.org.uk> - 0.5.8-2
- Fix vaapipostproc crash in live pipelines

* Wed Feb  5 2014 Simon Farnsworth <simon@farnz.org.uk> - 0.5.8-1
- initial release
