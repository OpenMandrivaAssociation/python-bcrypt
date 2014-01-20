%define tarname py-bcrypt

Summary:	Python implementation of Blowfish password hashing algorithm
Name:		python-bcrypt
Version:	0.4
Release:	1
Source0:	http://py-bcrypt.googlecode.com/files/py-bcrypt-%{version}.tar.gz
License:	BSD
Group:		Development/Python
Url:		http://www.mindrot.org/py-bcrypt.html
BuildRequires:	python-devel, python-nose

%description
py-bcrypt is an implementation the OpenBSD Blowfish password hashing
algorithm, as described in "A Future-Adaptable Password Scheme" by
Niels Provos and David Mazieres.

This system hashes passwords using a version of Bruce Schneier's
Blowfish block cipher with modifications designed to raise the cost of
off-line password cracking. The computation cost of the algorithm is
parametised, so it can be increased as computers get faster.

%prep
%setup -q -n %{tarname}-%{version}

%build
%__python setup.py build

%install
PYTHONDONTWRITEBYTECODE= %__python setup.py install --root=%{buildroot} --record=FILE_LIST

%check
pushd test
export PYTHONPATH=`dir -d ../build/lib.linux*`
nosetests
popd

%clean

%files -f FILE_LIST
%doc  LICENSE README TODO


%changelog
* Tue Nov 09 2010 Lev Givon <lev@mandriva.org> 0.2-1mdv2011.0
+ Revision: 595443
- import python-bcrypt



