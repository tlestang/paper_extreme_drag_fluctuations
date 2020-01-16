from setuptools import setup, Extension


def main():
    setup(
        name="simulate",
        version="1.0.0",
        description="Python interface for simulate function",
        author="Thibault Lestang",
        author_email="thibault.lestang@cs.ox.ac.uk",
        ext_modules=[
            Extension(
                "simulate",
                sources=["simulate.cpp"],
                include_dirs=["/home/tlestang/projects/pipeLBM/src"],
                library_dirs=["/home/tlestang/projects/pipeLBM/src"],
                libraries=["pipeLBM"],
                language="c++",
            )
        ],
    )


if __name__ == "__main__":
    main()
