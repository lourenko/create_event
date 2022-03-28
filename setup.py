from setuptools import setup

setup(
    name="create_event",
    version="1.0",
    #py_modules=["create_event"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        create_event=create:new_event
    """,
)
