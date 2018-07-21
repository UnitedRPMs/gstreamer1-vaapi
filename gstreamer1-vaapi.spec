%global gitdate 20180720
%global commit0 bc395f954d1ac7c6b4009930422636f04f0781ad
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:           gstreamer1-vaapi
Version:        1.14.2
Release:        7%{?gver}%{dist}
Summary:        GStreamer plugins to use VA API video acceleration

License:        LGPLv2+
URL:            https://cgit.freedesktop.org/gstreamer/gstreamer-vaapi
Source0: 	https://github.com/GStreamer/gstreamer-vaapi/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  glib2-devel >= 2.32
BuildRequires:  gstreamer1-devel >= 1.4.0
BuildRequires:  gstreamer1-plugins-base-devel >= 1.4.0
BuildRequires:  gstreamer1-plugins-bad-free-devel >= 1.4.0
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

NOCONFIGURE=1 ./autogen.sh

# Wayland support in libva isn't present - gstreamer-vaapi can't support Wayland without it
# https://bugzilla.redhat.com/show_bug.cgi?id=1051862
%configure \
    --with-package-name="GStreamer VAAPI Plugin (Fedora Linux)" \
    --with-package-origin="https://unitedrpms.github.io" \
    --enable-experimental --disable-static \
    --enable-static=no \
%{?_without_wayland:--disable-wayland} \
           --disable-builtin-libvpx

  # https://bugzilla.gnome.org/show_bug.cgi?id=655517
  sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%check
%__make check

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
