%define _optprefix /opt/ablestack/qemu

Name:           qemu-ablestack
Version:        %{?_version}%{!?_version:9.1.0}
Release:        %{?_release}%{!?_release:1}%{?dist}
Summary:        Multi-Version QEMU for ABLESTACK FT/HCI

License:        GPLv2
URL:            https://www.qemu.org
Source0:        https://download.qemu.org/qemu-%{version}.tar.xz

BuildRequires:  gcc, make, ninja-build, python3-pip, python3-tomli
BuildRequires:  glib2-devel, pixman-devel, zlib-devel, libfdt-devel
BuildRequires:  libaio-devel, liburing-devel, libcap-ng-devel, libseccomp-devel
BuildRequires:  libusb1-devel, nettle-devel, gnutls-devel, cyrus-sasl-devel
BuildRequires:  swtpm-devel, libcacard-devel, mesa-libGL-devel, usbredir-devel, libepoxy-devel

%description
ABLESTACK Custom QEMU. Support for COLO FT, io_uring, and vhost-vdpa.

%prep
%autosetup -n qemu-%{version}

%build
# QEMU 10.x부터는 일부 옵션 명칭이 변경될 수 있으나 기본 틀은 유지됩니다.
./configure --target-list=x86_64-softmmu \
    --prefix=%{_optprefix} \
    --interp-prefix=%{_optprefix}/gnemul/ \
    --enable-kvm \
    --enable-replication \
    --enable-colo-proxy \
    --enable-linux-io-uring \
    --enable-system \
    --enable-modules \
    --enable-cap-ng \
    --enable-attr \
    --enable-seccomp \
    --enable-libusb \
    --enable-usb-redir \
    --enable-tpm \
    --enable-vhost-net \
    --enable-vhost-user \
    --enable-vhost-vdpa \
    --enable-vnc \
    --enable-vnc-sasl \
    --enable-smartcard \
    --enable-guest-agent \
    --enable-opengl \
    --disable-werror \
    --audio-drv-list= \
    --disable-debug-info \
    --disable-spice \
    --disable-virglrenderer

make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}/usr/local/bin
ln -sf %{_optprefix}/bin/qemu-system-x86_64 %{buildroot}/usr/local/bin/ablestack-qemu

%files
%{_optprefix}/*
/usr/local/bin/ablestack-qemu

%changelog
* Sat Feb 21 2026 AbleCloud Admin <admin@ablecloud.io>
- Matrix Build for Rocky 9.6/10.1 and QEMU 9.1/10.2
