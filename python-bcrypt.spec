%undefine _debugsource_packages
%global module bcrypt
%define oname bcrypt

# disable tests for abf, complete successfully locally
%bcond_with tests

# NOTE To update also run create_vendored_crate_archive.sh to create a vendor
# NOTE archive of the rust crates and update the Source1: line and _abf.yml file
# NOTE Upload the _bcrypt-version-vendor.tar.gz to the file store.

Summary:	Modern password hashing for your software and your servers
Name:		python-bcrypt
Version:	5.0.0
Release:	3
# crypt_blowfish code is in Public domain and all other code in Apache 2.0,
# rust vendor crates mixture of Apache-2.0, MIT, Unlicence -
# see generated LICENSE.dependencies in built rpm for full list.
License:	Apache-2.0 AND Public Domain AND BSD-3-Clause AND MIT AND (Apache-2.0 OR MIT) AND (Unlicense OR MIT)
Group:		Development/Python
URL:		https://github.com/pyca/bcrypt
Source0:	https://pypi.python.org/packages/source/b/%{oname}/%{oname}-%{version}.tar.gz
Source1:	_%{oname}-%{version}-vendor.tar.xz

BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(cffi)
BuildRequires:	python%{pyver}dist(six)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(setuptools-rust)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	cargo
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
%endif

%description
A good password hashing for your software and your servers written in Python.

%prep
%autosetup -n %{module}-%{version} -p1 -a1
# Crates are already vendored. rust-packaging pulls python-rust2rpm, which
# still requires Python 3.14.
rm -f Cargo.toml.orig src/_bcrypt/Cargo.toml.orig
mkdir -p .cargo
cat > .cargo/config.toml << 'EOF'
[net]
offline = true

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

# remove remote url github badge clutter from README.rst
sed -i '4,9d;' README.rst

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
# pyo3 0.26 abi3 falls back to the 3.14 stable ABI on a 3.15 interpreter.
export PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1
export CARGO_NET_OFFLINE=true
# Cargo.toml sets lto = "thin". Combined with the distro
# -C linker-plugin-lto, rustc aborts in LLVM on __rust_alloc.
export CARGO_PROFILE_RELEASE_LTO=off
export CARGO_HOME=$PWD/.cargo
%py_build

cd src/_bcrypt
cargo tree --locked --offline --edges no-build,no-dev,no-proc-macro \
	--prefix none --format '{l}: {p}' \
	| sed -e "s: ($(pwd)[^)]*)::g" -e 's: / :/:g' -e 's:/: OR :g' \
	| sort -u > ../../LICENSE.dependencies


%install
%py_install

%if %{with tests}
%check
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
pip install -e .
%{__python} -m pytest -vvv -nauto tests/
%endif

%files
%license LICENSE LICENSE.dependencies
%doc README.rst
%{python_sitearch}/%{module}/
%{python_sitearch}/%{module}-%{version}*-info
