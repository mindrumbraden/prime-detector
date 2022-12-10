# %%

import requests
import zipfile
import warnings
import os

# %%


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    warnings.warn("""
                  A file called 'primes.txt' should be created. The user
                  should verify that the non-whitespace characters in
                  'primes.txt' only consist of the primes beginning with 2
                  (in case the URL (or its zip file) has changed since
                  the creation of this python script).

                  The quantity and type of whitespace characters should
                  not matter.
                  """)
    URL = "https://www.utm.edu/staff/caldwell/primes/millions/primes1.zip"
    response = requests.get(URL)
    with open("primes.zip", "wb") as handle:
        handle.write(response.content)
    response.close()
    with zipfile.ZipFile("primes.zip") as my_zip:
        my_zip.extract("primes1.txt")
    with open("primes1.txt", "r") as handle:
        prime_lines = handle.readlines()[2:]
    with open("primes.txt", "w") as handle:
        handle.write("".join(prime_lines))
    os.remove("primes.zip")
    os.remove("primes1.txt")
    return(0)

# %%


if __name__ == "__main__":
    main()

# %%
