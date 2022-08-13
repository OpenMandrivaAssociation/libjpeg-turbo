# (tpg) workaround for debuginfo generation
%define _unpackaged_files_terminate_build 0

# (tpg) reduce bloat by excluding cmake requires on devel packages
%global __requires_exclude ^cmake.*$

%define major 8
%define majorturbo 0
%define libname %mklibname jpeg %{major}
%define devname %mklibname -d jpeg
%define static %mklibname -s -d jpeg
%define turbo %mklibname turbojpeg %{majorturbo}

%define major62 62
%define libname62 %mklibname jpeg %{major62}

%global optflags %{optflags} -O3

# libjpeg-turbo is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif
%define lib32name libjpeg%{major}
%define dev32name libjpeg-devel
%define turbo32 libturbojpeg%{majorturbo}
%define static32 libjpeg-static-devel

%ifarch %{riscv}
%bcond_with pgo
%bcond_with java
%else
# Disable PGO when not using clang and/or when
# bootstrapping (avoids a few dependencies)
%bcond_without pgo
%bcond_without java
%endif

Summary:	A MMX/SSE2 accelerated library for manipulating JPEG image files
Name:		libjpeg-turbo
Epoch:		1
Version:	2.1.4
Release:	1
License:	wxWidgets Library License
Group:		System/Libraries
Url:		https://libjpeg-turbo.org/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
# These two allow automatic lossless rotation of JPEG images from a digital
# camera which have orientation markings in the EXIF data. After rotation
# the orientation markings are reset to avoid duplicate rotation when
# applying these programs again.
Source2:	http://jpegclub.org/jpegexiforient.c
Source3:	http://jpegclub.org/exifautotran.txt
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	nasm
%if %{with java}
BuildRequires:	jdk-current
BuildRequires:	java-gui-current
%endif
%if %{with pgo}
# Pull in some JPEG files so we can generate PGO data
BuildRequires:	desktop-common-data
BuildRequires:	breeze
BuildRequires:	distro-release-theme
BuildRequires:	plasma-workspace-wallpapers-autumn
BuildRequires:	plasma-workspace-wallpapers-bythewater
BuildRequires:	plasma-workspace-wallpapers-canopee
BuildRequires:	plasma-workspace-wallpapers-cascade
BuildRequires:	plasma-workspace-wallpapers-coldripple
BuildRequires:	plasma-workspace-wallpapers-colorfulcups
BuildRequires:	plasma-workspace-wallpapers-darkesthour
BuildRequires:	plasma-workspace-wallpapers-eveningglow
BuildRequires:	plasma-workspace-wallpapers-fallenleaf
BuildRequires:	plasma-workspace-wallpapers-flyingkonqui
BuildRequires:	plasma-workspace-wallpapers-grey
BuildRequires:	plasma-workspace-wallpapers-kite
BuildRequires:	plasma-workspace-wallpapers-kokkini
BuildRequires:	plasma-workspace-wallpapers-onestandsout
BuildRequires:	plasma-workspace-wallpapers-opal
BuildRequires:	plasma-workspace-wallpapers-pastelhills
BuildRequires:	plasma-workspace-wallpapers-path
BuildRequires:	plasma-workspace-wallpapers-summer_1am
%endif

%description
This package contains a library of functions for manipulating JPEG images.
It is a high-speed, libjpeg-compatible version for x86 and x86-64
processors which uses SIMD instructions (MMX, SSE2, etc.) to accelerate
baseline JPEG compression and decompression. It is generally 2-4x as fast
as the unmodified version of libjpeg, all else being equal.

%package -n %{libname}
Summary:	A library for manipulating JPEG image format files
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libjpeg.

%package -n %{libname62}
Summary:	A library for manipulating JPEG image format files
Group:		System/Libraries

%description -n %{libname62}
This package contains the library needed to run programs dynamically
linked with libjpeg.

%package -n %{turbo}
Summary:	TurboJPEG library
Group:		System/Libraries

%description -n %{turbo}
This package contains the library needed to run programs dynamically
linked with libturbojpeg.

%package -n %{devname}
Summary:	Development tools for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{turbo} = %{EVRD}
Provides:	jpeg-devel = %{EVRD}
Conflicts:	jpeg6-devel
Conflicts:	%{_lib}turbojpeg < 1:1.3.0
Obsoletes:	%{_lib}turbojpeg < 1:1.3.0
Obsoletes:	%{mklibname jpeg -d} < %{EVRD}
Obsoletes:	%{mklibname jpeg 62 -d} < 6b-45

%description -n %{devname}
The libjpeg-turbo devel package includes the header files necessary for
developing programs which will manipulate JPEG files using the
libjpeg library.

%package -n %{static}
Summary:	Static libraries for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	jpeg-static-devel = %{EVRD}
Conflicts:	jpeg6-static-devel
Obsoletes:	%{mklibname jpeg -d -s} < %{EVRD}
Obsoletes:	%{mklibname jpeg 62 -d -s} < 6b-45
Obsoletes:	%{mklibname jpeg 7 -d -s} < 7-3

%description -n %{static}
The libjpeg static devel package includes the static libraries
necessary for developing programs which will manipulate JPEG files using
the libjpeg library.

%package -n jpeg-progs
Summary:	Programs for manipulating JPEG format image files
Group:		Graphics
%rename		libjpeg-progs
%rename		jpeg6-progs

%description -n jpeg-progs
This package contains simple client programs for accessing the
libjpeg functions.  The library client programs include cjpeg, djpeg,
jpegtran, rdjpgcom, wrjpgcom and jpegexiforient, coupled with the script
exifautotran. Cjpeg compresses an image file into JPEG format. Djpeg
decompresses a JPEG file into a regular image file. Jpegtran can perform
various useful transformations on JPEG files: it can make lossless
cropping of JPEG files and lossless pasting of one JPEG into another
(dropping). Rdjpgcom displays any text comments included in a JPEG file.
Wrjpgcom inserts text comments into a JPEG file. Jpegexiforient allow
automatic lossless rotation of JPEG images from a digital camera which
have orientation markings in the EXIF data.

%if %{with java}
%package -n java-turbojpeg
Summary:	Java bindings to the turbojpeg library
Requires:	%{turbo} = %{EVRD}
Group:		Development/Java

%description -n java-turbojpeg
Java bindings to the turbojpeg library.
%endif

%if %{with compat32}
%package -n %{lib32name}
Summary:	A library for manipulating JPEG image format files (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package contains the library needed to run programs dynamically
linked with libjpeg.

%package -n %{turbo32}
Summary:	TurboJPEG library (32-bit)
Group:		System/Libraries

%description -n %{turbo32}
This package contains the library needed to run programs dynamically
linked with libturbojpeg.

%package -n %{dev32name}
Summary:	Development tools for programs which will use the libjpeg library (32-bit)
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}
Requires:	%{turbo32} = %{EVRD}

%description -n %{dev32name}
The libjpeg-turbo devel package includes the header files necessary for
developing programs which will manipulate JPEG files using the
libjpeg library.

%package -n %{static32}
Summary:	Static libraries for programs which will use the libjpeg library (32-bit)
Group:		Development/C
Requires:	%{dev32name} = %{EVRD}

%description -n %{static32}
The libjpeg static devel package includes the static libraries
necessary for developing programs which will manipulate JPEG files using
the libjpeg library.
%endif

%prep
%autosetup -p1
cp %{SOURCE2} jpegexiforient.c
cp %{SOURCE3} exifautotran

%if %{with java}
. %{_sysconfdir}/profile.d/90java.sh
%endif

%if %{with compat32}
export CFLAGS="%(echo %{optflags} | sed -e 's,-m64,,g') -m32"
export LDFLAGS="%(echo %{ldflags} | sed -e 's,-m64,,g') -m32"
%cmake32 -G Ninja \
	-DWITH_JAVA:BOOL=OFF \
	-DWITH_JPEG7:BOOL=ON \
	-DWITH_JPEG8:BOOL=ON
unset CFLAGS
unset LDFLAGS
cd ..
%endif

buildit() {
    NAME="$1"
    shift

%if %{with pgo}
    mkdir -p "$NAME-pgo"
    cd "$NAME-pgo"
# (tpg) 2021-11-21
# LLVM Profile Warning: Unable to track new values:
# Running out of static counters.
# Consider using option -mllvm -vp-counters-per-site=<n> to allocate more value profile counters at compile time.
%global __cc %{__cc} -mllvm -vp-counters-per-site=8
%global __cxx %{__cxx} -mllvm -vp-counters-per-site=8

    CFLAGS="%{optflags} -fprofile-generate" \
    CXXFLAGS="%{optflags} -fprofile-generate" \
    LDFLAGS="%{build_ldflags} -fprofile-generate" \
    %cmake "$@" \
	-G Ninja \
	../..
    %ninja_build
    cd ..
    find /usr/share/wallpapers -iname "*.jpg" |while read r; do
	# default."jpg" is actually a symlink to default.png, let's not freak out...
	echo $r |grep -q default.jpg && continue
	LD_LIBRARY_PATH="$(pwd)/build" ./build/djpeg -dct int $r >testimage.pnm
	LD_LIBRARY_PATH="$(pwd)/build" ./build/djpeg -dct fast $r >testimage.pnm
	LD_LIBRARY_PATH="$(pwd)/build" ./build/cjpeg testimage.pnm >testimage.jpg
	LD_LIBRARY_PATH="$(pwd)/build" ./build/cjpeg -optimize testimage.pnm >testimage.jpg
	LD_LIBRARY_PATH="$(pwd)/build" ./build/cjpeg -progressive testimage.pnm >testimage.jpg
	rm -f testimage.pnm testimage.jpg
    done

    LD_LIBRARY_PATH="$(pwd)/build" ./build/tjbench ../testimages/testimgint.jpg
    llvm-profdata merge --output=%{name}-llvm.profdata $(find . -name "*.profraw" -type f)
    PROFDATA="$(realpath %{name}-llvm.profdata)"
    rm -rf *.profraw
    cd ..
%endif

    mkdir -p "$NAME"
    cd "$NAME"
%if %{with pgo}
    CFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
    CXXFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
    LDFLAGS="%{build_ldflags} -fprofile-use=$PROFDATA" \
%endif
    %cmake "$@" \
	-G Ninja \
	../..
    %ninja_build
    cd ../..
}

buildit jpeg8 \
%if %{with java}
    -DWITH_JAVA:BOOL=ON \
%endif
    -DWITH_JPEG7:BOOL=ON \
    -DWITH_JPEG8:BOOL=ON

buildit jpeg62 \
    -DWITH_JPEG7:BOOL=OFF \
    -DWITH_JPEG8:BOOL=OFF

%{__cc} %{optflags} %{build_ldflags} -o jpegexiforient jpegexiforient.c

#%check
#make -C jpeg8 test
#make -C jpeg62 test

%install
%if %{with compat32}
%ninja_install -C build32
%endif

cd jpeg62
%ninja_install -C build

cd ../jpeg8
%ninja_install -C build
cd ..

install -m755 jpegexiforient -D %{buildroot}%{_bindir}/jpegexiforient
install -m755 exifautotran -D %{buildroot}%{_bindir}/exifautotran

#(neoclust) Provide jpegint.h because it is needed by certain software
install -m644 jpegint.h -D %{buildroot}%{_includedir}/jpegint.h

%files -n %{libname}
%{_libdir}/libjpeg.so.%{major}*

%files -n %{libname62}
%{_libdir}/libjpeg.so.%{major62}*

%files -n %{turbo}
%{_libdir}/libturbojpeg.so.%{majorturbo}*

%files -n %{devname}
%doc coderules.txt jconfig.txt libjpeg.txt structure.txt usage.txt wizard.txt
%doc %{_docdir}/%{name}
%{_libdir}/libjpeg.so
%{_libdir}/libturbojpeg.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h
%{_libdir}/cmake/%{name}/*.cmake

%files -n %{static}
%{_libdir}/libjpeg.a
%{_libdir}/libturbojpeg.a

%files -n jpeg-progs
%{_bindir}/*
%doc %{_mandir}/man1/*

%if %{with java}
%files -n java-turbojpeg
%{_datadir}/java/turbojpeg.jar
%endif

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libjpeg.so.%{major}*

%files -n %{turbo32}
%{_prefix}/lib/libturbojpeg.so.%{majorturbo}*

%files -n %{dev32name}
%{_prefix}/lib/libjpeg.so
%{_prefix}/lib/libturbojpeg.so
%{_prefix}/lib/pkgconfig/*.pc
%{_includedir}/*.h
%{_prefix}/lib/cmake/%{name}/*.cmake

%files -n %{static32}
%{_prefix}/lib/libjpeg.a
%{_prefix}/lib/libturbojpeg.a
%endif
