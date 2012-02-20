%define major	8
%define libname	%mklibname jpeg %{major}
%define devname	%mklibname -d jpeg
%define	turbo	%mklibname turbojpeg

%define	major62	62
%define	libname62 %mklibname jpeg %{major62}

Summary:	A MMX/SSE2 accelerated library for manipulating JPEG image files
Name:		libjpeg-turbo
Version:	1.2.0
Release:	1
Epoch:		1
License:	wxWidgets Library License
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
BuildRequires:	autoconf automake libtool >= 1.4
%ifarch %{ix86} x86_64
BuildRequires:	nasm
%endif

%description
This package contains a library of functions for manipulating JPEG images.
It is a high-speed, libjpeg-compatible version for x86 and x86-64
processors which uses SIMD instructions (MMX, SSE2, etc.) to accelerate
baseline JPEG compression and decompression. It is generally 2-4x as fast
as the unmodified version of libjpeg, all else being equal.

Install the libjpeg-turbo package if you need to manipulate JPEG files.
You should also install the jpeg-progs package.

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
linked with libjpeg-turbo.

%package -n	%{turbo}
Summary:	TurboJPEG library
Group:		System/Libraries

%description -n %{libname62}
This package contains the library needed to run programs dynamically
linked with libturbojpeg.

%description -n %{libname62}
This package contains the library needed to run programs dynamically
linked with libjpeg.

%package -n	%{devname}
Summary:	Development tools for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{libname} >= %{EVRD}
Provides:	jpeg-devel = %{EVRD}
Provides:	libjpeg-devel = %{EVRD}
Provides:	jpeg%{major}-devel = %{EVRD}
Conflicts:	jpeg6-devel
Obsoletes:	%{mklibname jpeg 62 -d} < 6b-45

%description -n	%{devname}
The libjpeg-turbo devel package includes the header files necessary for 
developing programs which will manipulate JPEG files using the
libjpeg library.

If you are going to develop programs which will manipulate JPEG images,
you should install this package. You'll also need to have the
libjpeg package installed.

%package -n	jpeg-progs
Summary:	Programs for manipulating JPEG format image files
Group:		Graphics
%rename		libjpeg-progs
%rename		jpeg6-progs

%description -n	jpeg-progs
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

%prep
%setup -q
%patch0 -p0

cp %{SOURCE2} jpegexiforient.c
cp %{SOURCE3} exifautotran

%build
autoreconf -fi
mkdir -p jpeg8
pushd jpeg8
CONFIGURE_TOP=.. \
CFLAGS="%{optflags} -O3 -funroll-loops -ffast-math" \
%configure2_5x	--disable-silent-rules \
		--enable-shared \
		--disable-static \
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
make install-libLTLIBRARIES DESTDIR=%{buildroot} -C jpeg62
%makeinstall_std -C jpeg8

install -m755 jpegexiforient -D %{buildroot}%{_bindir}/jpegexiforient
install -m755 exifautotran -D %{buildroot}%{_bindir}/exifautotran

#(neoclust) Provide jpegint.h because it is needed by certain software
install -m644 jpegint.h -D %{buildroot}%{_includedir}/jpegint.h

# Fix perms
chmod -x README-turbo.txt

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

rm -f %{buildroot}%{_docdir}/*

%files -n %{libname}
%doc change.log ChangeLog.txt README README-turbo.txt
%{_libdir}/libjpeg.so.%{major}*

%files -n %{libname62}
%{_libdir}/libjpeg.so.%{major62}*

%files -n %{turbo}
%{_libdir}/libturbojpeg.so

%files -n %{devname}
%doc coderules.txt example.c jconfig.txt libjpeg.txt structure.txt filelist.txt
%{_libdir}/libjpeg.so
%{_includedir}/*.h

%files -n jpeg-progs
%doc usage.txt wizard.txt
%{_bindir}/*
%{_mandir}/man1/*
