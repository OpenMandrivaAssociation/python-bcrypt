%{!?_licensedir: %global license %%doc}
%global with_python3 1


%global modname bcrypt
%global sum     Modern password hashing for your software and your servers

Name:               python-bcrypt
Version:	3.2.0
Release:	2
Summary:            %{sum}

#crypt_blowfish code is in Public domain and all other code in ASL 2.0
License:            ASL 2.0 and Public Domain and BSD
URL:                http://pypi.python.org/pypi/bcrypt
Source0:	https://files.pythonhosted.org/packages/d8/ba/21c475ead997ee21502d30f76fd93ad8d5858d19a3fad7cd153de698c4dd/bcrypt-3.2.0.tar.gz

Requires:           python-six
Requires:           python-cffi

BuildRequires:      python2-devel
BuildRequires:      python2-setuptools
BuildRequires:      python-six
BuildRequires:      python-cffi

%if 0%{?with_python3}
BuildRequires:      python3-devel
BuildRequires:      python-setuptools
BuildRequires:      python-cffi
BuildRequires:      python-six
%endif

%description
%{sum}.

%package -n python2-%{modname}
Summary:            %{sum}
%{?python_provide:%python_provide python2-%{modname}}

Requires:           python-six
Requires:           python-cffi
Provides:           py-bcrypt = 0.4-11
Obsoletes:          py-bcrypt < 0.4-11

%description -n python2-%{modname}
%{sum}.

%prep
%autosetup -n %{modname}-%{version}

%build
%{__python2} setup.py build

%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

# Better safe than sorry
find %{buildroot}%{python2_sitearch} -name '*.so' -exec chmod 755 {} ';'

%if 0%{?with_python3}
find %{buildroot}%{python3_sitearch} -name '*.so' -exec chmod 755 {} ';'
%endif

%check
# Tests can't run on epel7 due to an old pytest
%if (0%{?rhel} && 0%{?rhel} > 7)
%{__python2} setup.py test
%endif

%if 0%{?with_python3}
%{__python3} setup.py test
%endif

%files
%doc README.rst
%license LICENSE
%{python_sitearch}/%{modname}/
%{python_sitearch}/%{modname}-%{version}*

%files -n python2-%{modname}
%doc README.rst
%license LICENSE
%{python2_sitearch}/%{modname}/
%{python2_sitearch}/%{modname}-%{version}*
