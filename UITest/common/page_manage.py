class PageManage:
    """
    页面管理类
    """
    _pages = {}

    def __init__(self, package):
        self.package = package
        self.__get_pages()
        self.__get_name_pages()

    @property
    def pages(self):
        return self._pages.copy()

    def __get_pages(self):
        modules = import_submodules(self.package)
        for module_name, module_class in modules.items():
            if hasattr(module_class, module_name):
                self._pages[module_name] = getattr(module_class, module_name)

    def __get_name_pages(self):
        for _, page_class in self.pages.items():
            if hasattr(page_class, f"_{page_class.__name__}__page_name"):
                self._pages[getattr(page_class, f"_{page_class.__name__}__page_name")] = page_class

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

    :param recursive:
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

