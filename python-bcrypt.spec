%global module bcrypt

Summary:	Modern password hashing for your software and your servers
Name:		python-bcrypt
Version:	3.2.2
Release:	1
#crypt_blowfish code is in Public domain and all other code in ASL 2.0
License:	ASL 2.0 and Public Domain and BSD
Group:		Development/Python
URL:		https://github.com/pyca/bcrypt
Source0:	https://pypi.python.org/packages/source/b/%{module}/%{module}-%{version}.tar.gz

BuildRequires:  pkgconfig(python)
BuildRequires:	python3dist(cffi)
BuildRequires:  python3dist(six)
BuildRequires:	python3dist(setuptools)

%description
A good password hashing for your software and your servers written in Python.

%files
%license LICENSE
%doc README.rst
%{python_sitearch}/%{module}/
%{python_sitearch}/%{module}-%{version}-py%{pyver}.egg-info/

#----------------------------------------------------------------------------


%prep
%autosetup -p1 -n %{module}-%{version}

%build
%py_build

%install
%py_install

%check
%{__python3} setup.py test

