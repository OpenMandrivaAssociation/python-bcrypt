%{!?_licensedir: %global license %%doc}
%global with_python3 1


%global modname bcrypt
%global sum     Modern password hashing for your software and your servers

Name:               python-bcrypt
Version:            3.1.4
Release:            6%{?dist}
Summary:            %{sum}

#crypt_blowfish code is in Public domain and all other code in ASL 2.0
License:            ASL 2.0 and Public Domain and BSD
URL:                http://pypi.python.org/pypi/bcrypt
Source0:            https://files.pythonhosted.org/packages/source/b/%{modname}/%{modname}-%{version}.tar.gz

BuildRequires:      python2-devel
BuildRequires:      python2-setuptools
BuildRequires:      python2-six
#BuildRequires:      python2-pytest
BuildRequires:      python2-cffi

%if 0%{?with_python3}
BuildRequires:      python3-devel
BuildRequires:      python-setuptools
BuildRequires:      python-cffi
BuildRequires:      python-six
#BuildRequires:      python-pytest
%endif

%description
%{sum}.


%package -n python2-%{modname}
Summary:            %{sum}
%{?python_provide:%python_provide python2-%{modname}}

Requires:           python2-six
%if (0%{?fedora} && 0%{?fedora} <= 27) || (0%{?rhel} && 0%{?rhel} <= 7)
Requires:           python-cffi
%else
Requires:           python2-cffi
%endif
Provides:           py-bcrypt = 0.4-11
Obsoletes:          py-bcrypt < 0.4-11

%description -n python2-%{modname}
%{sum}.


%if 0%{?with_python3}
%package -n python3-%{modname}
Summary:            %{sum}
%{?python_provide:%python_provide python3-%{modname}}

Requires:           python3-six
Requires:           python3-cffi
Conflicts:          python3-py-bcritp
Provides:           python3-py-bcrypt = 0.4-11
Obsoletes:          python3-py-bcrypt < 0.4-11

%description -n python3-%{modname}
%{sum}.
%endif


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


%files -n python2-%{modname}
%doc README.rst
%license LICENSE
%{python2_sitearch}/%{modname}/
%{python2_sitearch}/%{modname}-%{version}*

%if 0%{?with_python3}
%files -n python3-%{modname}
%doc README.rst
%license LICENSE
%{python3_sitearch}/%{modname}/
%{python3_sitearch}/%{modname}-%{version}*
%endif
