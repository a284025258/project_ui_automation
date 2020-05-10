class PageManage:
    """
    页面管理类
    """
    @classmethod
    def get_page(cls, page_name):
        from pkgutil import walk_packages

        r = "../pages"
        modules = {}
        for _, name, __ in walk_packages(path=[r], prefix='', onerror=None):
            m = _.find_module(r + '.' + name).load_module(r + '.' + name)
            modules[name] = m
        c = {}
        for i in modules.values():
            c.update({k: v for k, v in i.__dict__.items() if k.endswith("Page") and type(v) == type})

        try:
            return c[page_name]
        except KeyError:
            raise ValueError(f"没有这个页面{page_name}")


if __name__ == '__main__':
    pass
