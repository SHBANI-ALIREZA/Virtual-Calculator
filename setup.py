import setuptools

setuptools.setup(
    include_package_data=True,
    name='VirtualCalculator',
    version='0.0.1',
    description='VirtualCalculator module',
    url='https://github.com/SHBANI-ALIREZA/Virtual-Calculator/blob/master/main.py',
    author='SHBANI-ALIREZA',
    author_email='alirezashbani99@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=['opencv-python', 'cvzone', 'numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Os Independent",
    ],
)