#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (not included in release tarball)
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-service_identify.spec)

Summary:	Service identity verification for pyOpenSSL & cryptography
Summary(pl.UTF-8):	Weryfikacja tożsamości usługi dla modułów pyOpenSSL i cryptography
Name:		python-service_identity
Version:	21.1.0
Release:	6
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/service_identity/
Source0:	https://files.pythonhosted.org/packages/source/s/service-identity/service-identity-%{version}.tar.gz
# Source0-md5:	5e5c195d8fcedc72f9068be2ad9b5a13
Patch0:		service-identity-intersphinx.patch
URL:		https://pypi.org/project/service_identity/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-attrs >= 16.0.0
BuildRequires:	python-cryptography
BuildRequires:	python-ipaddress
BuildRequires:	python-pyasn1
BuildRequires:	python-pyasn1_modules
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-attrs >= 16.0.0
BuildRequires:	python3-cryptography
BuildRequires:	python3-pyasn1
BuildRequires:	python3-pyasn1_modules
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Use this package if:
- you use pyOpenSSL and don't want to be MITM'ed or
- if you want to verify that a PyCA cryptography certificate is valid
  for a certain hostname or IP address.

%description -l pl.UTF-8
Ten moduł jest przydatny jeśli:
- używamy pyOpenSSL i chcemy uniknąć ataku MITM, lub też
- chcemy zweryfikować, że certyfikat PyCA cryptography jest poprawny
  dla określonej nazwy hosta lub adresu IP.

%package -n python3-service_identity
Summary:	Service identity verification for pyOpenSSL & cryptography
Summary(pl.UTF-8):	Weryfikacja tożsamości usługi dla modułów pyOpenSSL i cryptography
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-service_identity
Use this package if:
- you use pyOpenSSL and don't want to be MITM'ed or
- if you want to verify that a PyCA cryptography certificate is valid
  for a certain hostname or IP address.

%description -n python3-service_identity -l pl.UTF-8
Ten moduł jest przydatny jeśli:
- używamy pyOpenSSL i chcemy uniknąć ataku MITM, lub też
- chcemy zweryfikować, że certyfikat PyCA cryptography jest poprawny
  dla określonej nazwy hosta lub adresu IP.

%package apidocs
Summary:	API documentation for Python service_identity module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona service_identity
Group:		Documentation

%description apidocs
API documentation for Python service_identity module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona service_identity.

%prep
%setup -q -n service-identity-%{version}
%patch -P0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst
%{py_sitescriptdir}/service_identity
%{py_sitescriptdir}/service_identity-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-service_identity
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/service_identity
%{py3_sitescriptdir}/service_identity-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
