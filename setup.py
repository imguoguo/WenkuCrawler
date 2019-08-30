from setuptools import setup, find_packages

setup(
    name="WenkuCrawler",
    version="1.0",
    keywords=["百度文库", "文库", "wenku", "BaiduWenku", "WenkuCrawler"],
    description="爬取百度文库中的文档并下载下来！",
    license="MIT Licence",

    url="https://qwq.trade",
    author="Guoguo",
    author_email="i@qwq.trade",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests", "bs4", "selenium", "lxml"],

    scripts=[],
    entry_points={}
)