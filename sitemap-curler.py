import webbrowser
import subprocess
import os.path
import pathlib
import requests

# DOWNLOAD SITEMAP.XML FROM USER SPECIFIED URL
url = input("Please enter full URL to sitemap: ")

response = requests.get(url)
with open("sitemap.xml", "wb") as file:
    file.write(response.content)


# OPEN SITEMAP.XML
f = open("sitemap.xml", "r")
content = f.read()

print("\nFound {} characters in sitemap".format(len(content)))
print("Crawling...\n")


# MAIN URL CRAWL FUNCTION
linkRepo = []

for i in range(0, len(content)):
    if content[i : i + 5] == "<loc>":
        startOfLink = i + 5

        for j in range(0, len(content)):
            if content[i + j : i + j + 6] == "</loc>":
                endOfLink = i + j
                break
        link = content[startOfLink:endOfLink]
        linkRepo.append(link)

for i in range(0, len(linkRepo)):
    print(i + 1, linkRepo[i])

print("\nFinished crawling. Found {} links.".format(len(linkRepo)))


# OPTIONAL FOLLOW UP #1: SAVE URLS TO FILE
followUpSaveToFile = input("\nDo you want to save the links to a file? (y/n) ")

if followUpSaveToFile == "y":
    linkFileName = input("""\nPlease specify filename (e.g. "links.txt"): """)

    print("Writing file {}...".format(linkFileName))

    with open(linkFileName, "w") as filehandle:
        for listitem in linkRepo:
            filehandle.write("%s\n" % listitem)

    openFile = os.path.join(pathlib.Path(__file__).parent.absolute(), linkFileName)
    subprocess.call(["open", openFile])

    print("Finished writing file.")


# OPTIONAL FOLLOW UP #2: OPEN URLS (ALL OR RANGE) IN BROWSER
followUpOpenInBrowser = input("\nDo you want to open the links in your browser? (y/n) ")
ynRange = input("\nAll of them? (y/n) ")


def rangeSpec():
    rangeSpec.rangeFrom = int(input("\nSpecify range - From? "))
    rangeSpec.rangeTo = int(input("\nSpecify range - To? "))

    return rangeSpec.rangeFrom, rangeSpec.rangeTo


rangeSpec()

# RANGE VALIDATION
if rangeSpec.rangeFrom < 0 or rangeSpec.rangeTo < 0:
    print("\nError: Please enter positive ranges")
    rangeSpec()
elif rangeSpec.rangeTo - rangeSpec.rangeTo < 0:
    print('\nError: "From" is greater than "To"')
    rangeSpec()


if followUpOpenInBrowser == "y":
    print("Opening windows...")

    if ynRange == "y":
        for i in range(0, len(linkRepo)):
            webbrowser.open(linkRepo[i], new=2)

    else:
        for i in range(rangeSpec.rangeFrom - 1, rangeSpec.rangeTo):
            webbrowser.open(linkRepo[i], new=2)

    print("Finished opening windows.")


print("\nProgram finished.\n")

f.close()
