class PageManage:
    """
    页面管理类
    """

    def __init__(self, package):
        self.package = package
        self.pages = self._pages()

    def _pages(self):
        modules = import_submodules(self.package)
        pages = {}
        for k, v in modules.items():
            if hasattr(v, k):
                pages[k] = getattr(v, k)

        return pages

    def __call__(self, page_name):
        try:
            return self.pages[page_name]
        except KeyError:
            raise ValueError(f"没有这个页面{page_name}")


def import_submodules(package, recursive=True):
    """
    Import all submodules of a module, recursively,
    including subpackages.

    From http://stackoverflow.com/questions/3365740/how-to-import-all-submodules

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    import importlib
    import pkgutil
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for _loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


pm = PageManage("UITest.pages")

if __name__ == '__main__':
    print(pm.pages)
