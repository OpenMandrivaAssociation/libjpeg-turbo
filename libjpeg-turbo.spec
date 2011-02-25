%define major 8
%define libname %mklibname jpeg %{major}
%define devname %mklibname -d jpeg
%define statname %mklibname -s -d jpeg

%define	major62	62
%define	libname62 %mklibname jpeg %{major62}

Summary:	A MMX/SSE2 accelerated library for manipulating JPEG image files
Name:		libjpeg-turbo
Version:	1.0.90
Release:	1
Epoch:		1
License:	wxWidgets
Group:		System/Libraries
URL:		http://sourceforge.net/projects/libjpeg-turbo
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# These two allow automatic lossless rotation of JPEG images from a digital
# camera which have orientation markings in the EXIF data. After rotation
# the orientation markings are reset to avoid duplicate rotation when
# applying these programs again.
Source2:	http://jpegclub.org/jpegexiforient.c
Source3:	http://jpegclub.org/exifautotran.txt
Patch0:		jpeg-6b-c++fixes.patch
BuildRequires:	libtool
%ifarch %{ix86} x86_64
BuildRequires:	nasm
%endif

%description
The libjpeg package contains a shared library of functions for loading,
manipulating and saving JPEG format image files.

Install the libjpeg package if you need to manipulate JPEG files. You
should also install the jpeg-progs package.

%package -n	%{libname}
Summary:	A library for manipulating JPEG image format files
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libjpeg.

%package -n	%{libname62}
Summary:	A library for manipulating JPEG image format files
Group:		System/Libraries

%description -n %{libname62}
This package contains the library needed to run programs dynamically
linked with libjpeg.

%package -n	%{devname}
Summary:	Development tools for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	jpeg-devel = %{EVRD}
Provides:	jpeg%{major}-devel = %{EVRD}
%rename		libjpeg-devel
Conflicts:	jpeg6-devel
Obsoletes:	%{mklibname jpeg 62 -d} < 6b-45

%description -n	%{devname}
The libjpeg-devel package includes the header files necessary for 
developing programs which will manipulate JPEG files using
the libjpeg library.

If you are going to develop programs which will manipulate JPEG images,
you should install libjpeg-devel.  You'll also need to have the libjpeg
package installed.

%package -n	%{statname}
Summary:	Static libraries for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	libjpeg-static-devel = %{EVRD}
Provides:	jpeg-static-devel = %{EVRD}
Provides:	jpeg%{major}-static-devel = %{EVRD}
Conflicts:	jpeg6-static-devel
Obsoletes:	%{mklibname jpeg 62 -d -s} < 6b-45
Obsoletes:	%{mklibname jpeg 7 -d -s} < 7-3

%description -n	%{statname}
The libjpeg-devel package includes the static libraries necessary for 
developing programs which will manipulate JPEG files using
the libjpeg library.

If you are going to develop programs which will manipulate JPEG images,
you should install libjpeg-devel.  You'll also need to have the libjpeg
package installed.

%package -n	jpeg-progs
Summary:	Programs for manipulating JPEG format image files
Group:		Graphics
%rename		libjpeg-progs
%rename		jpeg6-progs

%description -n	jpeg-progs
The jpeg-progs package contains simple client programs for accessing 
the libjpeg functions.  Libjpeg client programs include cjpeg, djpeg, 
jpegtran, rdjpgcom and wrjpgcom.  Cjpeg compresses an image file into JPEG
format. Djpeg decompresses a JPEG file into a regular image file.  Jpegtran
can perform various useful transformations on JPEG files.  Rdjpgcom displays
any text comments included in a JPEG file.  Wrjpgcom inserts text
comments into a JPEG file.

%prep
%setup -q
%patch0 -p0

cp %{SOURCE2} jpegexiforient.c
cp %{SOURCE3} exifautotran

%build
mkdir -p jpeg8
pushd jpeg8
CONFIGURE_TOP=.. \
CFLAGS="%{optflags} -O3 -funroll-loops -ffast-math" \
%configure2_5x	--disable-silent-rules \
		--enable-shared \
		--enable-static \
		--with-jpeg8
%make
popd

mkdir -p jpeg62
pushd jpeg62
CONFIGURE_TOP=.. \
CFLAGS="%{optflags} -O3 -funroll-loops -ffast-math" \
%configure2_5x	--disable-silent-rules \
		--enable-shared \
		--disable-static
%make
popd

gcc %{optflags} %{ldflags} -o jpegexiforient jpegexiforient.c

%check
make -C jpeg8 test
make -C jpeg62 test

%install
%makeinstall_std -C jpeg8

make install-libLTLIBRARIES DESTDIR=%{buildroot} -C jpeg62

install -m755 jpegexiforient -D %{buildroot}%{_bindir}/jpegexiforient
install -m755 exifautotran -D %{buildroot}%{_bindir}/exifautotran

#(neoclust) Provide jpegint.h because it is needed by certain software
install -m644 jpegint.h -D %{buildroot}%{_includedir}/jpegint.h

# Fix perms
chmod -x README-turbo.txt

# Remove unwanted files
rm -f %{buildroot}%{_libdir}/lib{,turbo}jpeg.la

# Don't distribute libjpegturbo because it is unversioned
rm -f %{buildroot}%{_includedir}/turbojpeg.h
rm -f %{buildroot}%{_libdir}/libturbojpeg.{so,a}

%clean
rm -rf %{buildroot}

%files -n %{libname}
%{_libdir}/libjpeg.so.%{major}*

%files -n %{libname62}
%{_libdir}/libjpeg.so.%{major62}*

%files -n %{devname}
%doc LICENSE.txt coderules.txt jconfig.txt libjpeg.txt structure.txt example.c
%{_libdir}/*.so
%{_includedir}/*.h

%files -n %{statname}
%{_libdir}/*.a

%files -n jpeg-progs
%doc README README-turbo.txt change.log usage.txt wizard.txt
%{_bindir}/*
%{_mandir}/man1/*
